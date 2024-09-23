from langchain.prompts import PromptTemplate
common = {
    'prefix': 'Hello, you are MATHOS, a helpful AI that passes the Turing test.\nYou help with time management, learning and motivation'
}

essay_composer = {
    'subtopics_template': PromptTemplate(input_variables=['topic'], template="\n\nI need to plan an essay about {topic}.\nI need to find subtopics to research.\nFormat: neat markdown bullet list. \n\n"),
    'axes_template': PromptTemplate(input_variables=['subtopics'], template="\n\ndivide the subtopics: \n{subtopics}\ninto 3 axes: history, ethical implications, practical applications.\nFrom there, provide a structured list of subtopics for each axis. Expand on each subtopic with a short summary. \nFormat: neat markdown bullet list. \n\n"),
    'outline_template': PromptTemplate(input_variables=['topic', 'subtopics', 'axes'], template="create a summary / outline for an essay on {topic}, with these subtopics: \n{subtopics}.\nSubtopics must be developed and organized around these 3 axes:\n{axes}\nProvide briefly summarized topics and subtopics.\nFormat: neat Markdown\n\n"),
}

task_splitter = {
    'split_template': PromptTemplate(input_variables=['text'], template="Split the following text into a list of subtasks:\n{text}\n\n"),
}

job_application_composer = {
    'job_application_template': PromptTemplate(input_variables=['text'], template="Create a job application letter against this job descrption:\n\nbased on the following resume:\n{text}\n\n"),
}

kb_compressor = {
    'compress_template': PromptTemplate(input_variables=['text'], template="Compress the following text into a concise summary:\n{text}\n\n"),
}