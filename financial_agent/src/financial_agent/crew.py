"""Financial Agent Crew for automated trading analysis and strategy development.

This module defines a multi-agent crew specialized in financial markets analysis,
trading strategy development, execution planning, and risk management.

The crew consists of four specialized agents:
- Data Analyst: Monitors and analyzes market data
- Trading Strategy Agent: Develops and tests trading strategies
- Execution Agent: Plans optimal trade execution
- Risk Management Agent: Evaluates and manages trading risks
"""
# Warning control
import warnings
import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_openai import ChatOpenAI

warnings.filterwarnings('ignore')



# Uncomment the following line to use an example of a custom tool
# from financial_agent.tools.custom_tool import MyCustomTool

@CrewBase
class FinancialAgentCrew():
	"""Financial Agent Crew for automated trading analysis and strategy development.
	
	This crew provides a comprehensive trading analysis system with specialized agents
	for market data analysis, strategy development, execution planning, and risk management.
	The crew operates in a hierarchical structure with a manager LLM coordinating activities.
	
	Attributes:
		agents_config (str): Path to agents configuration file
		tasks_config (str): Path to tasks configuration file
		search_tool (SerperDevTool): Web search tool for market research
		scrape_tool (ScrapeWebsiteTool): Web scraping tool for data collection
		
	Raises:
		ValueError: If OPENAI_API_KEY environment variable is not set
	"""
	if os.getenv('OPENAI_API_KEY') == '':
		raise ValueError("OPENAI_API_KEY is not set")
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	search_tool = SerperDevTool()
	scrape_tool = ScrapeWebsiteTool()

	@agent
	def data_analyst_agent(self) -> Agent:
		"""Create a data analyst agent for market data monitoring and analysis.
		
		This agent specializes in financial markets analysis using statistical modeling
		and machine learning to identify trends and predict market movements.
		
		Returns:
			Agent: Configured data analyst agent with web scraping and search tools
		"""
		return Agent(
			config=self.agents_config['data_analyst_agent'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			allow_delegation=True,
			tools=[self.scrape_tool, self.search_tool]
		)

	@agent
	def trading_strategy_agent(self) -> Agent:
		"""Create a trading strategy development agent.
		
		This agent develops and tests various trading strategies based on insights
		from market data analysis. It evaluates performance to determine the most
		profitable and risk-averse trading approaches.
		
		Returns:
			Agent: Configured trading strategy agent with research tools
		"""
		return Agent(
			config=self.agents_config['trading_strategy_agent'],
			verbose=True,
			allow_delegation=True,
			tools=[self.scrape_tool, self.search_tool]
		)
		
	@agent
	def execution_agent(self) -> Agent:
		"""Create a trade execution planning agent.
		
		This agent specializes in analyzing timing, price, and logistical details
		of potential trades, providing well-founded suggestions for optimal
		trade execution to maximize efficiency and strategy adherence.
		
		Returns:
			Agent: Configured execution agent with market research tools
		"""
		return Agent(
			config=self.agents_config['execution_agent'],
			verbose=True,
			allow_delegation=True,
			tools=[self.scrape_tool, self.search_tool]
		)
	
	@agent
	def risk_management_agent(self) -> Agent:
		"""Create a risk management and assessment agent.
		
		This agent evaluates and provides insights on risks associated with
		potential trading activities. It offers detailed risk analysis and
		suggests safeguards to ensure trading aligns with risk tolerance.
		
		Returns:
			Agent: Configured risk management agent with analysis tools
		"""
		return Agent(
			config=self.agents_config['risk_management_agent'],
			verbose=True,
			allow_delegation=True,
			tools=[self.scrape_tool, self.search_tool]
		)
	
	@task
	def strategy_development_task(self) -> Task:
		"""Create a task for developing trading strategies.
		
		This task involves analyzing market conditions and developing
		comprehensive trading strategies based on data analysis insights.
		
		Returns:
			Task: Configured strategy development task
		"""
		return Task(
			config=self.tasks_config['strategy_development_task'],
			agent=self.trading_strategy_agent()
		)
	
	@task
	def execution_planning_task(self) -> Task:
		"""Create a task for planning trade execution strategies.
		
		This task focuses on determining optimal timing, pricing, and
		logistical approaches for executing approved trading strategies.
		
		Returns:
			Task: Configured execution planning task
		"""
		return Task(
			config=self.tasks_config['execution_planning_task'],
			agent=self.execution_agent()
		)
	@task
	def risk_assessment_task(self) -> Task:
		"""Create a task for comprehensive risk assessment.
		
		This task evaluates potential risks associated with proposed
		trading activities and provides risk mitigation recommendations.
		
		Returns:
			Task: Configured risk assessment task
		"""
		return Task(
			config=self.tasks_config['risk_assessment_task'],
			agent=self.risk_management_agent()
		)
	@task
	def data_analysis_task(self) -> Task:
		"""Create a task for market data analysis.
		
		This task involves monitoring and analyzing real-time market data
		to identify trends, patterns, and trading opportunities.
		
		Returns:
			Task: Configured data analysis task
		"""
		return Task(
			config=self.tasks_config['data_analysis_task'],
			agent=self.data_analyst_agent()
		)
	
	@crew
	def crew(self) -> Crew:
		"""Create and configure the complete Financial Agent Crew.
		
		This method assembles all specialized agents and tasks into a cohesive
		hierarchical crew for comprehensive financial analysis and trading strategy
		development, with a manager LLM coordinating the workflow.
		
		Returns:
			Crew: Configured hierarchical crew with all agents, tasks, and manager LLM
		"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			verbose=2,
			process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			manager_llm=ChatOpenAI(model="gpt-3.5-turbo",  temperature=0.7)
		)