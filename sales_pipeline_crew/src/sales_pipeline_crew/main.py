#!/usr/bin/env python
"""Main entry point for the Sales Pipeline Crew.

This module provides the main execution function for running the Sales Pipeline Crew,
which conducts comprehensive research on specified topics and generates detailed
analytical reports.
"""
from sales_pipeline_crew.crew import SalesPipelineCrewCrew


def run():
    """Execute the Sales Pipeline Crew workflow.
    
    This function initializes and runs the complete Sales Pipeline Crew workflow
    for topic-based research and reporting. The crew will:
    
    1. Conduct comprehensive research on the specified topic
    2. Analyze gathered information and insights
    3. Generate a detailed markdown report with findings
    
    The workflow processes the following input:
    - topic: The subject matter for research and analysis
    
    Default Configuration:
    - Topic: 'AI LLMs' (Large Language Models in Artificial Intelligence)
    
    Output generated:
    - report.md: Comprehensive research report on the specified topic
    
    Returns:
        The result of the crew execution containing the research report
        
    Note:
        The topic parameter is automatically interpolated into agent roles
        and goals through template variables in the configuration files.
    """
    # Define the research topic - can be customized for different domains
    inputs = {
        'topic': 'AI LLMs'
    }
    
    result = SalesPipelineCrewCrew().crew().kickoff(inputs=inputs)
    return result