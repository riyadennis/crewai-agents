from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from project_planning_crew.tools.board_fetcher_tool import BoardDataFetcherTool
from project_planning_crew.tools.card_fetcher_tool import CardDataFetcherTool

# Uncommfrom ent the following line to use an example of a custom tool
# from project_planning_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class ProjectPlanningCrewCrew():
	"""ProjectPlanningCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def data_collector(self) -> Agent:
		return Agent(
			config=self.agents_config['data_collector'],
			tools=[BoardDataFetcherTool(), CardDataFetcherTool()], 
			allow_delegation=False,
			verbose=True
		)

	@agent
	def project_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['project_analyst'],
			allow_delegation=False,
			verbose=True
		)

	@task
	def datacollection_task(self) -> Task:
		return Task(
			config=self.tasks_config['datacollection_task'],
			agent=self.data_collector()
		)

	@task
	def data_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_analysis_task'],
			agent=self.project_analyst(),
			output_file='report.md'
		)
	
	@task
	def report_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['report_generation_task'],
			agent=self.project_analyst(),
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ProjectPlanningCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)