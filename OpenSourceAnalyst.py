import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from crewai_tools import ScrapeWebsiteTool


os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] ='mistral'
os.environ["OPENAI_API_KEY"] ='NA'
os.environ["SERPER_API_KEY"]="Insert API Key"
# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] =''

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool(website_url='https://www.synopsys.com/blogs/software-security/open-source-trends-ossra-report.html')
# Define your agents with roles and goals
researcher = Agent(
  role='Opensource software enthusiast',
  goal='Find the latest security threats in the opensource landscape',
  backstory="""you are a renowned open source developer and researcher your expertise lies in identifying emerging trends.
  You have a knack for identifying new security threats emerging in the open source landscape and finding out how they work and what they do""",
  verbose=True,
  allow_delegation=True,
  tools=[search_tool, scrape_tool],
  max_rpm=100
  
)
writer = Agent(
    
  role='Opensource technology writer',
  goal='Craft understandable and direct literature on open source software security',
  backstory="""You work at a leading cyber security firm whose goal is to make opensource software safer""",
  verbose=True,
  allow_delegation=True,
  tools=[search_tool, scrape_tool]
)

# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive search and analysis of the latest trends in opensource software vulnerabilities in 2024.
  Identify key trends, breakthrough technologies, potential industry impacts, and exploits being leveraged in the wild""",
  expected_output="Fully analysis with links to the information",
  agent=researcher,
  tools=[search_tool, scrape_tool],
  human_input=True
)

task2 = Task(
  description="""Using the insights provided, develop an engaging article that highlights the most significant trends.
  The article should be informative yet accessible, catering to a tech-savvy audience.
  Make it sound cool, Make sure that it's detailed and understandable""",
  expected_output="Full report in long article form",
  agent=writer,
  tools=[search_tool, scrape_tool],
  context=[task1],
  human_input=True
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