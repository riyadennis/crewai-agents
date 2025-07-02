import pytest
import os
from unittest.mock import Mock, patch
from crewai import Agent
from financial_agent.crew import FinancialAgentCrew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool


class TestFinancialAgentCrewAgents:
    """Test suite for FinancialAgent crew agents"""

    @pytest.fixture
    def crew_instance(self):
        """Create a crew instance for testing"""
        os.environ['OPENAI_API_KEY'] = 'test'
        agent = FinancialAgentCrew()
        # Mock all agent configs
        agent.agents_config = {
            'data_analyst_agent': {
                'role': 'Data Analyst',
                'goal': 'Monitor market data',
                'backstory': 'Financial markets specialist'
            },
            'trading_strategy_agent': {
                'role': 'Trading Strategy Developer',
                'goal': 'Develop trading strategies',
                'backstory': 'Deep understanding of financial markets'
            },
            'execution_agent': {
                'role': 'Trade Advisor',
                'goal': 'Suggest optimal trade execution',
                'backstory': 'Specializes in trade timing and logistics'
            },
            'risk_management_agent': {
                'role': 'Risk Advisor',
                'goal': 'Evaluate trading risks',
                'backstory': 'Deep understanding of risk assessment models'
            }
        }
        return agent

    @patch('financial_agent.crew.SerperDevTool')
    @patch('financial_agent.crew.ScrapeWebsiteTool')
    def test_data_analyst_agent_creation(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that data analyst agent is created with correct configuration"""
        # Mock the tools
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        agent = crew_instance.data_analyst_agent()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 2
        assert agent.allow_delegation is True
        assert agent.verbose is True

    @patch('financial_agent.crew.SerperDevTool')
    @patch('financial_agent.crew.ScrapeWebsiteTool')
    def test_trading_strategy_agent_creation(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that trading strategy agent is created with correct configuration"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        
        agent = crew_instance.trading_strategy_agent()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 2
        assert agent.allow_delegation is True
        assert agent.verbose is True

    @patch('financial_agent.crew.SerperDevTool')
    @patch('financial_agent.crew.ScrapeWebsiteTool')
    def test_execution_agent_creation(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that execution agent is created with correct configuration"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        
        agent = crew_instance.execution_agent()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 2
        assert agent.allow_delegation is True
        assert agent.verbose is True

    @patch('financial_agent.crew.SerperDevTool')
    @patch('financial_agent.crew.ScrapeWebsiteTool')
    def test_risk_management_agent_creation(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that risk management agent is created with correct configuration"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
    
        agent = crew_instance.risk_management_agent()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 2
        assert agent.allow_delegation is True
        assert agent.verbose is True

    @patch('financial_agent.crew.SerperDevTool')
    @patch('financial_agent.crew.ScrapeWebsiteTool')
    def test_all_agents_have_same_tools(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that all agents have the same tools (search and scrape)"""
        search_instance = SerperDevTool()
        scrape_instance = ScrapeWebsiteTool()
        mock_search_tool.return_value = search_instance
        mock_scrape_tool.return_value = scrape_instance
        agents = [
            crew_instance.data_analyst_agent(),
            crew_instance.trading_strategy_agent(),
            crew_instance.execution_agent(),
            crew_instance.risk_management_agent()
        ]
        
        # All agents should have the same 2 tools
        for agent in agents:
            assert len(agent.tools) == 2
            assert search_instance in agent.tools
            assert scrape_instance in agent.tools


    def test_tools_initialization(self, crew_instance):
        """Test that tools are properly initialized at class level"""
        assert hasattr(crew_instance, 'search_tool')
        assert hasattr(crew_instance, 'scrape_tool')

    @patch('financial_agent.crew.SerperDevTool')
    @patch('financial_agent.crew.ScrapeWebsiteTool')
    def test_agent_delegation_settings(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that all agents have delegation enabled"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        agents = [
            crew_instance.data_analyst_agent(),
            crew_instance.trading_strategy_agent(),
            crew_instance.execution_agent(),
            crew_instance.risk_management_agent()
        ]
        
        # All agents should have delegation enabled
        for agent in agents:
            assert agent.allow_delegation is True

    @patch('financial_agent.crew.SerperDevTool')
    @patch('financial_agent.crew.ScrapeWebsiteTool')
    def test_agent_verbose_settings(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that all agents have verbose mode enabled"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        
        agents = [
            crew_instance.data_analyst_agent(),
            crew_instance.trading_strategy_agent(),
            crew_instance.execution_agent(),
            crew_instance.risk_management_agent()
        ]
        
        # All agents should have verbose mode enabled
        for agent in agents:
            assert agent.verbose is True

    @patch('financial_agent.crew.SerperDevTool')
    @patch('financial_agent.crew.ScrapeWebsiteTool')
    def test_agent_error_handling(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test agent creation with missing configuration"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        
        # Test with empty config
        crew_instance.agents_config = {}
        
        with pytest.raises(KeyError):
            crew_instance.data_analyst_agent()

    def test_crew_class_attributes(self, crew_instance):
        """Test that crew class has required attributes"""
        assert 'data_analyst_agent' in crew_instance.agents_config
        assert 'trading_strategy_agent' in crew_instance.agents_config
        assert 'execution_agent' in crew_instance.agents_config
        assert 'risk_management_agent' in crew_instance.agents_config

        assert hasattr(crew_instance, 'search_tool')
        assert hasattr(crew_instance, 'scrape_tool')