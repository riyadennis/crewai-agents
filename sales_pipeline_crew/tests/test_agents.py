import pytest
from unittest.mock import Mock, patch, MagicMock
from crewai import Agent
from sales_pipeline_crew.crew import SalesPipelineCrewCrew


class TestSalesPipelineCrewAgents:
    """Test suite for SalesPipelineCrew agents"""

    @pytest.fixture
    def crew_instance(self):
        """Create a crew instance for testing"""
        return SalesPipelineCrewCrew()

    def test_researcher_agent_creation(self, crew_instance):
        """Test that researcher agent is created with correct configuration"""
        # Mock the agents config
        crew_instance.agents_config = {
            'researcher': {
                'role': '{topic} Senior Data Researcher',
                'goal': 'Uncover cutting-edge developments in {topic}',
                'backstory': 'Seasoned researcher with knack for uncovering latest developments'
            }
        }
        
        agent = crew_instance.researcher()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 0  # No tools assigned by default
        assert agent.verbose is True

    def test_reporting_analyst_agent_creation(self, crew_instance):
        """Test that reporting analyst agent is created with correct configuration"""
        # Mock the agents config
        crew_instance.agents_config = {
            'reporting_analyst': {
                'role': '{topic} Reporting Analyst',
                'goal': 'Create detailed reports based on {topic} data analysis',
                'backstory': 'Meticulous analyst with keen eye for detail'
            }
        }
        
        agent = crew_instance.reporting_analyst()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 0  # No tools assigned by default
        assert agent.verbose is True


    def test_both_agents_no_tools_by_default(self, crew_instance):
        """Test that both agents have no tools assigned by default"""
        crew_instance.agents_config = {
            'researcher': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'reporting_analyst': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'}
        }
        
        researcher = crew_instance.researcher()
        reporting_analyst = crew_instance.reporting_analyst()
        
        # Both agents should have no tools by default
        assert len(researcher.tools) == 0
        assert len(reporting_analyst.tools) == 0

    def test_agent_verbose_settings(self, crew_instance):
        """Test that all agents have verbose mode enabled"""
        crew_instance.agents_config = {
            'researcher': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'reporting_analyst': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'}
        }
        
        researcher = crew_instance.researcher()
        reporting_analyst = crew_instance.reporting_analyst()
        
        # Both agents should have verbose mode enabled
        assert researcher.verbose is True
        assert reporting_analyst.verbose is True

    def test_agent_delegation_settings(self, crew_instance):
        """Test that agents have default delegation settings (no explicit setting means default)"""
        crew_instance.agents_config = {
            'researcher': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'reporting_analyst': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'}
        }
        
        researcher = crew_instance.researcher()
        reporting_analyst = crew_instance.reporting_analyst()
        
        # Since allow_delegation is not explicitly set, it should use default
        # This test verifies the agents are created successfully without explicit delegation setting
        assert isinstance(researcher, Agent)
        assert isinstance(reporting_analyst, Agent)

    def test_agent_error_handling(self, crew_instance):
        """Test agent creation with missing configuration"""
        # Test with empty config
        crew_instance.agents_config = {}
        
        with pytest.raises(KeyError):
            crew_instance.researcher()
        
        with pytest.raises(KeyError):
            crew_instance.reporting_analyst()

    def test_agent_config_template_variables(self, crew_instance):
        """Test that agent configurations support template variables like {topic}"""
        crew_instance.agents_config = {
            'researcher': {
                'role': 'Sales Senior Data Researcher',
                'goal': 'Uncover cutting-edge developments in Sales',
                'backstory': 'Seasoned researcher with knack for uncovering latest developments in Sales'
            },
            'reporting_analyst': {
                'role': 'Sales Reporting Analyst',
                'goal': 'Create detailed reports based on Sales data analysis',
                'backstory': 'Meticulous analyst with keen eye for detail in Sales'
            }
        }
        
        researcher = crew_instance.researcher()
        reporting_analyst = crew_instance.reporting_analyst()
        
        # Agents should be created successfully with template-like configurations
        assert isinstance(researcher, Agent)
        assert isinstance(reporting_analyst, Agent)

    def test_minimal_crew_structure(self, crew_instance):
        """Test that this crew has the minimal structure (2 agents, no tools by default)"""
        crew_instance.agents_config = {
            'researcher': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'reporting_analyst': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'}
        }
        
        # Should have exactly 2 agents
        researcher = crew_instance.researcher()
        reporting_analyst = crew_instance.reporting_analyst()
        
        assert isinstance(researcher, Agent)
        assert isinstance(reporting_analyst, Agent)
        
        # Both should have minimal configuration (no tools, verbose enabled)
        for agent in [researcher, reporting_analyst]:
            assert len(agent.tools) == 0
            assert agent.verbose is True

    def test_agent_creation_independence(self, crew_instance):
        """Test that agents can be created independently"""
        crew_instance.agents_config = {
            'researcher': {'role': 'Test1', 'goal': 'Test1', 'backstory': 'Test1'},
            'reporting_analyst': {'role': 'Test2', 'goal': 'Test2', 'backstory': 'Test2'}
        }
        
        # Should be able to create just one agent without the other
        researcher = crew_instance.researcher()
        assert isinstance(researcher, Agent)
        
        # And create the other independently
        reporting_analyst = crew_instance.reporting_analyst()
        assert isinstance(reporting_analyst, Agent)
        
        # They should be different instances
        assert researcher is not reporting_analyst