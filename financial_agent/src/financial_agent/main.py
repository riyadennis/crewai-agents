#!/usr/bin/env python
from financial_agent.crew import FinancialAgentCrew

def run():
    financial_trading_inputs = {
        'stock_selection': 'AAPL',
        'initial_capital': '100000',
        'risk_tolerance': 'Medium',
        'trading_strategy_preference': 'Day Trading',
        'news_impact_consideration': True
    }
    result = FinancialAgentCrew().crew().kickoff(inputs=financial_trading_inputs)
