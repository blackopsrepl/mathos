from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

from operator import itemgetter

from src.backend.factory.ArchetypeFactory import Archetype, ArchetypeFactory
import src.backend.prompt_templates as prompt_templates

class EssayPlanner(Archetype):

    def set_openai_api_key(self):
        # TODO: isolate secrets colletcion
        self.openai_api_key = ""

    def set_llm(self):
        self.llm_cool = ChatOpenAI(openai_api_key=self.openai_api_key, model_name="gpt-3.5-turbo", temperature=0, streaming=True)
        self.llm_hot = ChatOpenAI(openai_api_key=self.openai_api_key, model_name="gpt-4o", temperature=0.20, streaming=True)

    def set_prompt_templates(self):
        self.t = prompt_templates.essay_composer

    def set_memory(self):
        self.memory = ConversationBufferMemory(return_messages=True)
        self.memory.load_memory_variables({})
        
    def set_chain(self):
        self.subtopics_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['subtopics_template'] | self.llm_cool | StrOutputParser()
        self.axes_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['axes_template'] | self.llm_cool | StrOutputParser()
        self.outline_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['outline_template'] | self.llm_hot | StrOutputParser()

    def run_chain(self, user_query, start_date, end_date):
        subtopics = self.subtopics_chain.invoke({"task": user_query})
        axes = self.axes_chain.invoke({"subtasks": subtopics})
        outline = self.outline_chain.invoke({"topic": user_query, "subtopics": subtopics, "axes": axes})
        return outline

class EssayPlannerFactory(ArchetypeFactory):
    def build(self) -> Archetype:
        self.essay_planner = EssayPlanner()
        self.essay_planner.set_openai_api_key()
        self.essay_planner.set_llm()
        self.essay_planner.set_prompt_templates()
        self.essay_planner.set_memory()
        self.essay_planner.set_chain()
        return self.essay_planner