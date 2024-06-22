from __future__ import annotations
from abc import ABC, abstractmethod
import json
from src.backend.constants import openai_api_key as apikey

class Archetype(ABC):
    
    def set_openai_api_key(self):
        self.openai_api_key = apikey

    @abstractmethod
    def set_llm(self):
        pass

    @abstractmethod
    def set_prompt_templates(self):
        pass
    
    @abstractmethod
    def set_memory(self):
        pass

    @abstractmethod
    def set_chain(self, prompt_templates):
        pass

    def set_json_schema(self):
        self.json_schema = json.load(open('schema.json'))

    @abstractmethod
    def run_chain(self, query):
        pass

class ArchetypeFactory(ABC):
    @abstractmethod
    def build(self):
        pass

    def produce(self) -> Archetype:
        product = self.build()
        return product