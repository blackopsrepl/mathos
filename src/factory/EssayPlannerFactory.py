from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

from operator import itemgetter

from src.factory.ArchetypeFactory import Archetype, ArchetypeFactory
import src.prompt_templates as prompt_templates

class EssayPlanner(Archetype):

    def set_openai_api_key(self):
        self.openai_api_key = ""

    def set_llm(self):
        self.llm_dry_simple = ChatOpenAI(openai_api_key=self.openai_api_key, model_name="gpt-3.5-turbo", temperature=0.30, streaming=True)
        self.llm_dry_complex = self.llm_verbose = ChatOpenAI(openai_api_key=self.openai_api_key, model_name="gpt-4-turbo", temperature=0.30, streaming=True)
        # self.llm_verbose = ChatOpenAI(openai_api_key=self.openai_api_key, model_name="gpt-4-turbo", temperature=0.45, streaming=True)

    def set_prompt_templates(self):
        self.t = prompt_templates.essay_composer

    def set_memory(self):
        self.memory = ConversationBufferMemory(return_messages=True)
        self.memory.load_memory_variables({})
        
    def set_chain(self):
        self.subtasks_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['subtasks_template'] | self.llm_dry_simple | StrOutputParser()
        self.blocks_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['blocks_template'] | self.llm_dry_complex | StrOutputParser()
        self.outline_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['outline_template'] | self.llm_verbose | StrOutputParser()
        self.timeline_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['timeline_template'] | self.llm_dry_simple | StrOutputParser()
        self.analysis_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['analysis_template'] | self.llm_dry_simple | StrOutputParser()
        self.schema_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['schema_template'] | self.llm_dry_complex | StrOutputParser()

    def run_chain(self, user_query, start_date, end_date):
        subtasks = self.subtasks_chain.invoke({"task": user_query})
        blocks = self.blocks_chain.invoke({"subtasks": subtasks})
        outline = self.outline_chain.invoke({"task": user_query, "subtasks": subtasks, "blocks": blocks})
        analysis = self.analysis_chain.invoke({"blocks": blocks})
        timeline = self.timeline_chain.invoke({"outline": outline, "subtasks": subtasks, "blocks": blocks, "analysis": analysis, "start_date": start_date, "end_date": end_date})
        schema = self.schema_chain.invoke({"timeline": timeline, "json_schema": self.set_json_schema})
        return schema

class EssayPlannerFactory(ArchetypeFactory):
    def build(self) -> Archetype:
        self.essay_planner = EssayPlanner()
        self.essay_planner.set_openai_api_key()
        self.essay_planner.set_llm()
        self.essay_planner.set_prompt_templates()
        self.essay_planner.set_memory()
        self.essay_planner.set_chain()
        return self.essay_planner