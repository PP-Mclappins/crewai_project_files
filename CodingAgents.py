import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
#from crewai_tools import WebsiteSearchTool
from crewai_tools import SerperDevTool

os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
#os.environ["OPENAI_MODEL_NAME"]=''
os.environ["OPENAI_API_KEY"] ='NA'
os.environ["SERPER_API_KEY"] ="975db30ce86884909090830a678ed2b901ffd7d7"
# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] =''

#tool = WebsiteSearchTool(website='https://github.com/joaomdmoura/crewai')
search_tool = SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
    llm = ChatOpenAI(
    model = "mistral",
    base_url = "http://localhost:11434/v1"),
   role='Senior python programmer',
   goal='write effective and usable scripts in python',
   backstory="""you're a senior programmer with a long history in the python programming language
  you are proficient in writing code using various tools provided in the crewai toolkit""",
  # llm ='codegemma',
  verbose=True,
  allow_delegation=True,
  #tool = WebsiteSearchTool(website='https://github.com/joaomdmoura/crewai')
  tools=[search_tool]
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic or others (https://docs.crewai.com/how-to/LLM-Connections/)
  #
  # import os
  # os.environ['OPENAI_MODEL_NAME'] = 'gpt-3.5-turbo'
  #
  # OR
  #
  # from langchain_openai import ChatOpenAI
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)
writer = Agent(
    llm = ChatOpenAI(
    model = "mistral",
    base_url = "http://localhost:11434/v1"),
  role='Programming consultant',
  goal='Craft concise and accurate code',
  backstory="""you are a seasoned programmer who uses python and its tools to accomplish extraordinary tasks in the machine learning field""",
  verbose=True,
  allow_delegation=True,
  #tool = WebsiteSearchTool(website='https://github.com/joaomdmoura/crewai')
  tools=[search_tool]
)
reviewer = Agent(
    llm = ChatOpenAI(
    model = "codegemma",
    base_url = "http://localhost:11434/v1"),
  role='Senior code analyst',
  goal='Review and correct code, produce accurate and efficient code',
  backstory="""you are a seasoned code reviewer you use any tool at your disposal to craft efficient, accurate, and concise code. You excel at finding and correcting errors in python code""",
  verbose=True,
  allow_delegation=False,
  #tool = WebsiteSearchTool(website='https://github.com/joaomdmoura/crewai')
  tools=[search_tool]
)
# Create tasks for your agents
task1 = Task(
  description="""Create a game of pinball using python""",
  expected_output="Fully comprehensive report with no details left behind.",
  agent=researcher,
)

task2 = Task(
  description="""refine the previous agents script and ensure that its accurate and functionable""",
  expected_output="Comprehensive and accurate script with as few mistakes as possible",
  agent=writer,
)
task3 = Task(
  description="""Review the script provided and analyze it for errors and possible syntax issues. Correct them where possible.""",
  expected_output="Comprehensive and accurate scripts with as few mistakes as possible, as well as a brief summary of any errors that you weren't able to resolve.",
  agent=reviewer,
)  
# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer, reviewer],
  tasks=[task1, task2, task3],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)