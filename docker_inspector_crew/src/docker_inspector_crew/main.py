#!/usr/bin/env python
"""Entry point for the Docker Inspector Crew."""
from docker_inspector_crew.crew import DockerInspectorCrew


def run():
    """Run the Docker Inspector Crew and print the duplicate report."""
    result = DockerInspectorCrew().crew().kickoff()
    print("\n" + "=" * 60)
    print("DOCKER DUPLICATE REPORT")
    print("=" * 60)
    print(result)
    return result
