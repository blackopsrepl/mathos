from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

from operator import itemgetter

from src.backend.factory.ArchetypeFactory import Archetype, ArchetypeFactory
import src.backend.prompt_templates as prompt_templates

class KBCompressor(Archetype):

    def set_llm(self):
        self.llm_cool = ChatOpenAI(openai_api_key=self.openai_api_key, model_name="gpt-3.5-turbo", temperature=0, streaming=True)
        self.llm_hot = ChatOpenAI(openai_api_key=self.openai_api_key, model_name="gpt-4o", temperature=0.20, streaming=True)

    def set_prompt_templates(self):
        self.t = prompt_templates.essay_composer

    def set_memory(self):
        self.memory = ConversationBufferMemory(return_messages=True)
        self.memory.load_memory_variables({})
        
    def set_chain(self):
        self.extract_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['subtopics_template'] | self.llm_cool | StrOutputParser()
        self.summarize_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['subtopics_template'] | self.llm_cool | StrOutputParser()
        self.incremental_chain = RunnablePassthrough.assign(memory=RunnableLambda(self.memory.load_memory_variables) | itemgetter("history")) | self.t['subtopics_template'] | self.llm_cool | StrOutputParser()

    def run_chain(self, List):
        # takes list of md files as input
        pass

class KBCompressorFactory(ArchetypeFactory):
    def build(self) -> Archetype:
        self.kb_compressor = KBCompressor()
        self.essay_planner.set_openai_api_key()
        self.essay_planner.set_llm()
        self.essay_planner.set_prompt_templates()
        self.essay_planner.set_memory()
        self.essay_planner.set_chain()
        return self.essay_planner