from langchain.prompts import PromptTemplate
common = {
    'prefix': 'Hello, you are MATHOS, a helpful AI that passes the Turing test.\nYou help with time management, learning and motivation'
}

project_composer = {
    # splits task provided by the user into subtasks
    'subtasks_template': PromptTemplate(input_variables=['task'], template="\n\nSei un agent AI per la pianificazione dei progetti. Il tuo compito è spezzare un task nei subtask necessari al suo completamento.\n Il task è il seguente: {task}.\nOutput: Lista di subtask.\n\n"),
    # splits subtasks into blocks TODO: optimize time unit consistency
    'blocks_template': PromptTemplate(input_variables=['subtasks'], template="\n\n1. dividi i subtask:\n{subtasks}\nin blocks.\n2. Fornisci un elenco strutturato di subtask e rispettivi blocks.\nOutput: Lista di block.\n\n"),
    # estimates time to execute each block TODO: optimize time unit consistency
    'analysis_template': PromptTemplate(input_variables=['blocks'], template="\n\nesegui una stima del tempo necessario per eseguire ognuno dei seguenti blocks:\n{blocks}\nOutput: Hashmap con rispettivamente ogni block e la quantità di slot da 30 minuti necessaria a completarlo, espressa come integer.\n\n"),

    # TODO: add number of working hours/day
    # TODO: add max. hours/block

    # task decomposer templates
    'outline_template': PromptTemplate(input_variables=['task', 'subtasks', 'blocks'], template="\n\ncrea un outline per le attività necessarie a svolgere il task:\n{task}\n con questi sottotask:\n{subtasks}.\nI sottotask devono essere organizzati con i rispettivi blocks:\n{blocks}\n\n"),
    'timeline_template': PromptTemplate(input_variables=['outline', 'subtasks', 'blocks', 'analysis', 'start_date', 'end_date'], template="\n\nda questo outline:\n{outline}\ntraccia una timeline esecutiva.\nUsa\n{subtasks}\n come subtask.\n\nI subtask sono a loro volta suddivisi in blocks:\n{blocks}\n, con rispettivo effort stimato in \n{analysis}.\n Data di inizio: {start_date}. Scadenza: {end_date}.\n\n"),
    # TODO: move {start_date} and {end_date} to analysis_template
    
    # provides {json_schema} to llm and fills it with data from analysis_template
    'schema_template': PromptTemplate(input_variables=['json_schema', 'timeline'], template="\n\nformatta i dati:\n{timeline}\n\nseguendo in modo ferreo questo schema JSON:\n{json_schema}\n\nOutput: payload JSON compilato garantendo integrità dei dati; nessun carattere aggiuntivo; corretta formattazione JSON con apici doppi; serializzabile.\n\n")
}

essay_composer = {
    'subtopics_template': PromptTemplate(input_variables=['topic'], template="\n\nI need to plan an essay about {topic}.\nI need to find subtopics to research.\nFormat: neat markdown bullet list. \n\n"),
    'axes_template': PromptTemplate(input_variables=['subtopics'], template="\n\ndivide the subtopics: \n{subtopics}\ninto 3 axes: history, ethical implications, practical applications.\nFrom there, provide a structured list of subtopics for each axis. Expand on each subtopic with a short summary. \nFormat: neat markdown bullet list. \n\n"),
    # TODO: isolate input (multiple input variables!) from PromptTemplate
    'outline_template': PromptTemplate(input_variables=['input'], template="create a summary / outline for a high school essay on {topic}, with these subtopics: \n{subtopics}.\nSubtopics must be developed and organized around these 3 axes:\n{axes}\nProvide briefly summarized topics and subtopics.\nFormat: neat Markdown\n\n"),
    'timeline_template': PromptTemplate(input_variables=['input'], template="\n\nplan a feasible linear timeline for a high school essay on {topic} with this outline:\n{outline}.\nthe essay has to be considered as the main task and it has to be broken down into subtasks.\nthe subtasks have to be organized in a feasible manner in the timeline.\nUse {subtopics} as subtasks.\nProvide an ordered timeline of subtasks for the essay. Start date: {start_date}. Deadline: {end_date}.\nFormat: neat markdown bullet list.\n\n")
}