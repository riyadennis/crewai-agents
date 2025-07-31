"""Sales Pipeline Crew for data research and reporting.

This module defines a minimal two-agent crew specialized in topic-based research
and report generation. The crew provides a simple but effective structure for
data collection and analysis across various domains.

The crew consists of two specialized agents:
- Researcher: Conducts comprehensive research on specified topics
- Reporting Analyst: Creates detailed reports based on research findings
"""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from sales_pipeline_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class SalesPipelineCrewCrew():
	"""Sales Pipeline Crew for topic-based research and reporting.
	
	This crew provides a streamlined approach to research and report generation
	for any specified topic. It uses template-based configuration that allows
	for flexible topic substitution in agent roles and goals.
	
	Attributes:
		agents_config (str): Path to agents configuration file with topic templates
		tasks_config (str): Path to tasks configuration file
		
	Note:
		Agent configurations use {topic} placeholders that can be interpolated
		at runtime for different research domains.
	"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		"""Create a senior data researcher agent.
		
		This agent specializes in uncovering cutting-edge developments in any
		specified topic. It's designed to find the most relevant information
		and present it in a clear and concise manner.
		
		Returns:
			Agent: Configured researcher agent with no tools by default
			
		Note:
			The agent configuration supports {topic} template variables
			for flexible topic-based research.
		"""
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		"""Create a reporting analyst agent.
		
		This agent is a meticulous analyst with a keen eye for detail, specializing
		in transforming complex data into clear and concise reports that are easy
		to understand and act upon.
		
		Returns:
			Agent: Configured reporting analyst agent with no tools by default
			
		Note:
			The agent configuration supports {topic} template variables
			for flexible topic-based analysis.
		"""
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		"""Create a task for comprehensive topic research.
		
		This task conducts thorough research on the specified topic,
		gathering relevant information and insights for analysis.
		
		Returns:
			Task: Configured research task assigned to the researcher agent
		"""
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def reporting_task(self) -> Task:
		"""Create a task for report generation.
		
		This task creates detailed reports based on research findings,
		outputting the results to a markdown file for easy consumption.
		
		Returns:
			Task: Configured reporting task with markdown file output
		"""
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Create and configure the complete Sales Pipeline Crew.
		
		This method assembles the researcher and reporting analyst into a
		sequential workflow for comprehensive topic research and report generation.
		
		Returns:
			Crew: Configured sequential crew with researcher and analyst agents
		"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)