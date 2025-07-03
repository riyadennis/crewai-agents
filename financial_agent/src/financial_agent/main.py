#!/usr/bin/env python
"""Main entry point for the Financial Agent Crew.

This module provides the main execution function for running the Financial Agent Crew,
which performs comprehensive financial analysis, strategy development, and risk assessment
for automated trading systems.
"""
from financial_agent.crew import FinancialAgentCrew

def run():
    """Execute the Financial Agent Crew workflow.
    
    This function initializes and runs the complete Financial Agent Crew workflow
    with predefined trading parameters. The crew will:
    
    1. Analyze market data for the specified stock (AAPL)
    2. Develop trading strategies based on day trading preferences
    3. Plan execution strategies considering market conditions
    4. Assess risks and provide risk management recommendations
    
    The workflow operates with the following default parameters:
    - Stock: AAPL (Apple Inc.)
    - Initial Capital: $100,000
    - Risk Tolerance: Medium
    - Strategy: Day Trading
    - News Impact: Considered in analysis
    
    Returns:
        The result of the crew execution containing analysis, strategies, and recommendations
        
    Raises:
        ValueError: If OPENAI_API_KEY is not properly configured
        Exception: If any agent fails during execution
    """
    financial_trading_inputs = {
        'stock_selection': 'AAPL',
        'initial_capital': '100000',
        'risk_tolerance': 'Medium',
        'trading_strategy_preference': 'Day Trading',
        'news_impact_consideration': True
    }
    result = FinancialAgentCrew().crew().kickoff(inputs=financial_trading_inputs)
    return result
