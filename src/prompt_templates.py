from langchain.prompts import PromptTemplate
essay_composer = {
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

thesis_eng = {
    'executive_loop': '\n\nHelp {user_name} prioritize tasks based on time constraints and motivation factors.\n\n',
    'subtopics_template': PromptTemplate(input_variables=['topic'], template="\n\nHello, you are Clio, my personal ADHD Coach and Cognitive Life Integrated Operator.\nYou help with time management, learning and motivation. I need to plan a high school essay about {topic}.\nI need to find subtopics to research.\nFormat: neat markdown bullet list. \n\n"),
    'axes_template': PromptTemplate(input_variables=['subtopics'], template="\n\ndivide the subtopics: \n{subtopics}\ninto 3 axes: history, ethical implications, practical applications.\nFrom there, provide a structured list of subtopics for each axis. Expand on each subtopic with a short summary. \nFormat: neat markdown bullet list. \n\n"),
    'outline_template': PromptTemplate(input_variables=['input'], template="\n\n {input} \n\n"),
    'timeline_template': PromptTemplate(input_variables=['input'], template="\n\n {input} \n\n"),
    'four_cs_template': PromptTemplate(input_variables=['timeline'], template="for each task in the timeline {timeline}, suggest ideas to gamify it with the most appropriate C strategy:\n(Captivate), (Create), (Compete), (Complete).\nFormat: neat markdown bullet list.\n\n"),
    'analysis_template': PromptTemplate(input_variables=['topic'], template="\n\n {topic} \n\n")
}