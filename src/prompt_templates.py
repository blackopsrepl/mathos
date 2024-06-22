from langchain.prompts import PromptTemplate
common = {
    'prefix': 'Hello, you are MATHOS, a helpful AI that passes the Turing test.\nYou help with time management, learning and motivation'
}
s
essay_composer = {
    'subtopics_template': PromptTemplate(input_variables=['topic'], template="\n\nI need to plan an essay about {topic}.\nI need to find subtopics to research.\nFormat: neat markdown bullet list. \n\n"),
    'axes_template': PromptTemplate(input_variables=['subtopics'], template="\n\ndivide the subtopics: \n{subtopics}\ninto 3 axes: history, ethical implications, practical applications.\nFrom there, provide a structured list of subtopics for each axis. Expand on each subtopic with a short summary. \nFormat: neat markdown bullet list. \n\n"),
    'outline_template': PromptTemplate(input_variables=['topic', 'subtopics', 'axes'], template="create a summary / outline for an essay on {topic}, with these subtopics: \n{subtopics}.\nSubtopics must be developed and organized around these 3 axes:\n{axes}\nProvide briefly summarized topics and subtopics.\nFormat: neat Markdown\n\n"),
}