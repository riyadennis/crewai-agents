# Warning control
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_openai import ChatOpenAI



# Uncomment the following line to use an example of a custom tool
# from financial_agent.tools.custom_tool import MyCustomTool

@CrewBase
class FinancialAgentCrew():
	"""FinancialAgent crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	search_tool = SerperDevTool()
	scrape_tool = ScrapeWebsiteTool()

	@agent
	def data_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['data_analyst_agent'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			allow_delegation=True,
			tools=[self.scrape_tool, self.search_tool]
		)

	@agent
	def trading_strategy_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['trading_strategy_agent'],
			verbose=True,
			allow_delegation=True,
			tools=[self.scrape_tool, self.search_tool]
		)
		
	@agent
	def execution_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['execution_agent'],
			verbose=True,
			allow_delegation=True,
			tools=[self.scrape_tool, self.search_tool]
		)
	
	@agent
	def risk_management_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['risk_management_agent'],
			verbose=True,
			allow_delegation=True,
			tools=[self.scrape_tool, self.search_tool]
		)
	
	@task
	def strategy_development_task(self) -> Task:
		return Task(
			config=self.tasks_config['strategy_development_task'],
			agent=self.trading_strategy_agent()
		)
	
	@task
	def execution_planning_task(self) -> Task:
		return Task(
			config=self.tasks_config['execution_planning_task'],
			agent=self.execution_agent()
		)
	@task
	def risk_assessment_task(self) -> Task:
		return Task(
			config=self.tasks_config['risk_assessment_task'],
			agent=self.risk_management_agent()
		)
	@task
	def data_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_analysis_task'],
			agent=self.data_analyst_agent()
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the FinancialAgent crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			verbose=2,
			process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			manager_llm=ChatOpenAI(model="gpt-3.5-turbo",  temperature=0.7)
		)