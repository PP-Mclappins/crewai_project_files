import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI #must include this import if defining individual models such as those defined below.
#from crewai_tools import WebsiteSearchTool
from crewai_tools import SerperDevTool

os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
#os.environ["OPENAI_MODEL_NAME"]='Here you can insert a single hosted model like: 'openhermes', Or define each Agent model as configured below'
os.environ["OPENAI_API_KEY"] ='NA'
os.environ["SERPER_API_KEY"] ="***********************" #insert your own api key here, Try it for free @ https://serper.dev

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
#tool = WebsiteSearchTool(website='Define URL here')

search_tool=SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
    llm = ChatOpenAI(
    model = "mistral",
    base_url = "http://localhost:11434/v1"),
   role='Senior python programmer',
   goal='write effective and usable scripts in python',
   backstory="""you're a senior programmer with a long history in powershell
  you are proficient in writing code using various PS modules and you understand how to leverage those tools to write efficient scripts""",
  
  verbose=True,
  allow_delegation=True,
  tools=[search_tool],
  
  
  #tool = WebsiteSearchTool(website='insert URL')
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
  role='Script writing expert',
  goal='Craft concise and accurate code',
  backstory="""you are a seasoned programmer who uses powershell and its tools to accomplish extraordinary tasks in automation""",
  verbose=True,
  allow_delegation=True,
  tools=[search_tool],
)

reviewer = Agent(
    llm = ChatOpenAI(
    model = "codegemma",
    base_url = "http://localhost:11434/v1"),
  role='Senior script analyst',
  goal='Review and correct code, produce accurate and efficient code',
  backstory="""you are a seasoned scripting agent you can craft efficient, accurate, and concise code.
  You excel at finding and correcting errors in scripts""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
)
# Create tasks for your agents
task1 = Task(
  description="""Help me create a power shell script that can sort files in a given directory by their extenion
  and place them into a directory inside of the Documents folder with other files of the same extension,
  if no directory exists the script should create one in the Documents parent directory""",
  expected_output="Full powershell script in text format",
  agent=researcher,
)

task2 = Task(
  description="""iterate over the given script, refine it, and ensure that it's accurate and functionable""",
  expected_output="an improved iteration of the script with a short description of any errors that have been resolved during iteration",
  agent=writer,
)

task3 = Task(
  description="""Review the script provided and analyze it for errors and possible syntax issues. Correct them where possible.""",
  expected_output="Comprehensive and accurate script with as few mistakes as possible, as well as a brief summary of any errors that you weren't able to resolve.",
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