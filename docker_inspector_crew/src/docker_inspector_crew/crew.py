import warnings
import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_anthropic import ChatAnthropic

from docker_inspector_crew.tools.docker_tool import (
    InspectContainerTool,
    ListContainersTool,
    ListImagesTool,
    PruneDanglingImagesTool,
    PruneStoppedContainersTool,
    RemoveContainerTool,
    RemoveImageTool,
)

warnings.filterwarnings("ignore")


@CrewBase
class DockerInspectorCrew:
    """Crew that audits Docker containers on the local machine and reports duplicates."""

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("ANTHROPIC_API_KEY is not set")

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    list_containers_tool = ListContainersTool()
    list_images_tool = ListImagesTool()
    inspect_container_tool = InspectContainerTool()
    remove_container_tool = RemoveContainerTool()
    prune_containers_tool = PruneStoppedContainersTool()
    prune_images_tool = PruneDanglingImagesTool()
    remove_image_tool = RemoveImageTool()
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.2)

    @agent
    def docker_collector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["docker_collector_agent"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                self.list_containers_tool,
                self.list_images_tool,
                self.inspect_container_tool,
            ],
        )

    @agent
    def duplicate_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["duplicate_analyzer_agent"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                self.list_containers_tool,
                self.list_images_tool,
            ],
        )

    @task
    def container_inventory_task(self) -> Task:
        return Task(
            config=self.tasks_config["container_inventory_task"],
            agent=self.docker_collector_agent(),
        )

    @agent
    def docker_cleanup_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["docker_cleanup_agent"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                self.list_containers_tool,
                self.remove_container_tool,
                self.prune_containers_tool,
                self.prune_images_tool,
                self.remove_image_tool,
            ],
        )

    @task
    def duplicate_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["duplicate_analysis_task"],
            agent=self.duplicate_analyzer_agent(),
            context=[self.container_inventory_task()],
        )

    @task
    def cleanup_task(self) -> Task:
        return Task(
            config=self.tasks_config["cleanup_task"],
            agent=self.docker_cleanup_agent(),
            context=[self.duplicate_analysis_task()],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=2,
            process=Process.sequential,
        )
