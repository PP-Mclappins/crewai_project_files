import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"]='openhermes'
os.environ["OPENAI_API_KEY"] ='NA'
os.environ["SERPER_API_KEY"] ="Insert Serper API Key"
# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] =''

search_tool = SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Marketing Director for a renowned landscaping company',
  goal='Uncover cutting-edge Marketing ideas for the company',
  backstory="""You work at a world class landscaping company.
  Your expertise lies in identifying emerging trends in gardening and residential landscaping.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation=False,
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
  role='Blog Content Strategist',
  goal='Craft compelling content on landscaping trends',
  backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
  You transform complex concepts into compelling narratives. 
  You enjoy the outdoors and have an appreciation for beautiful residential and commercial landscaping projects""",
  verbose=True,
  allow_delegation=False,
)

# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest trends in landscaping in spring 2024.
  Identify key trends and ideas. Choose a single subject to cover from the list of latest trends.
  search for more information on that topic as necessary to write an engaging article.""",
  expected_output="Full report in bullet points",
  agent=researcher
)

task2 = Task(
  description="""Using the insights provided, develop an engaging blog
  post that highlights the most significant landscaping trends.
  Your post should be informative yet accessible, catering to a modern audience.
  Make it sound cool, avoid complex words so it doesn't sound like AI. It should be created for a company blog.""",
  expected_output="Full blog post of at least 4 paragraphs",
  agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)