from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  SerperDevTool
)

# Uncomment the following line to use an example of a custom tool
# from jobsearch_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class JobsearchCrewCrew():
	"""JobsearchCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	search_tool = SerperDevTool()
	scrape_tool = ScrapeWebsiteTool()
	read_resume = FileReadTool(file_path='./resume/riyadennis.md')
	semantic_search_resume = MDXSearchTool(mdx='./resume/riyadennis.md')

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[self.scrape_tool, self.search_tool],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def profiler(self) -> Agent:
		return Agent(
			config=self.agents_config['profiler'],
			tools=[self.scrape_tool, self.search_tool, 
		  	self.read_resume, self.semantic_search_resume],
			verbose=True
		)
	
	@agent
	def resume_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['resume_strategist'],
			tools=[self.scrape_tool, self.search_tool, 
		  	self.read_resume, self.semantic_search_resume],
			verbose=True
		)
	
	@agent
	def interview_preparer(self) -> Agent:
		return Agent(
			config=self.agents_config['interview_preparer'],
			tools=[self.scrape_tool, self.search_tool, 
		  	self.read_resume, self.semantic_search_resume],
			verbose=True
		)	

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher(),
			async_execution=True
		)

	@task
	def profile_task(self) -> Task:
		return Task(
			config=self.tasks_config['profile_task'],
			agent=self.profiler(),
			async_execution=True
		)

	@task
	def resume_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['resume_strategy_task'],
			agent=self.resume_strategist(),
			output_file="tailored_resume.md",
			# context=[self.research_task, self.profile_task]
		)
	
	@task
	def interview_preparation_task(self) -> Task:
		return Task(
			config=self.tasks_config['interview_preparation_task'],
			agent=self.interview_preparer(),
			output_file="interview_materials.md",
			# context=[self.research_task, self.profile_task, self.resume_strategy_task]
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the JobsearchCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)