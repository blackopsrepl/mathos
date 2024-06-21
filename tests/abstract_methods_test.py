from typing import Literal
import pytest
import app.factory.ArchetypeFactory
import app.factory.TaskSplitterFactory

@pytest.fixture
def task_splitter():
    factory = app.factory.TaskSplitterFactory.TaskSplitterFactory()
    return factory.build()

@pytest.mark.parametrize("method", [
    'set_openai_api_key',
    'set_llm',
    'set_memory',
    'set_chain',
    'run_chain'
])
def abstract_methods_test(task_splitter: app.factory.TaskSplitterFactory.Archetype, method: Literal['set_openai_api_key'] | Literal['set_llm'] | Literal['set_prompt_templates'] | Literal['set_memory'] | Literal['set_chain'] | Literal['run_chain']):
    with pytest.raises(TypeError):
        getattr(task_splitter, method)()

if __name__ == "__main__":
  pytest.main()