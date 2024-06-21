from __future__ import annotations
from abc import ABC, abstractmethod
import json

class Archetype(ABC):
    @abstractmethod
    def set_openai_api_key(self):
        pass

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