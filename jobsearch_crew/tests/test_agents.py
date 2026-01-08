import pytest
import os

from unittest.mock import Mock, patch, MagicMock
from crewai import Agent
from jobsearch_crew.crew import JobsearchCrewCrew


class TestJobsearchCrewAgents:
    """Test suite for JobsearchCrew agents"""

    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    @pytest.fixture
    def crew_instance(self):
        """Create a crew instance for testing"""
        os.environ['OPENAI_API_KEY'] = 'test'
        instance = JobsearchCrewCrew()
        return instance

 
    def test_researcher_agent_creation(self, mock_mdx_attr, mock_file_attr, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that researcher agent is created with correct configuration"""
        # Mock the tools
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        mock_file_attr.return_value = Mock()
        mock_mdx_attr.return_value = Mock()
        
        # Mock the agents config
        crew_instance.agents_config = {
            'researcher': {
                'role': 'Tech Job Researcher',
                'goal': 'Amazing analysis on job posting',
                'backstory': 'Job researcher with prowess in extracting information'
            }
        }
        
        agent = crew_instance.researcher()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 2  # Only search and scrape tools
        assert agent.verbose is True

    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    def test_profiler_agent_creation(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that profiler agent is created with correct configuration"""
        # Mock the tools
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        crew_instance.read_resume = Mock()
        crew_instance.semantic_search_resume = Mock()
        
        crew_instance.agents_config = {
            'profiler': {
                'role': 'Personal Profiler for Engineers',
                'goal': 'Research on job applicants',
                'backstory': 'Equipped with analytical prowess'
            }
        }
        
        agent = crew_instance.profiler()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 4  # All tools: search, scrape, file read, mdx search
        assert agent.verbose is True

    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    def test_resume_strategist_agent_creation(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that resume strategist agent is created with correct configuration"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        crew_instance.read_resume = Mock()
        crew_instance.semantic_search_resume = Mock()
        
        crew_instance.agents_config = {
            'resume_strategist': {
                'role': 'Resume Strategist for Engineers',
                'goal': 'Make resume stand out',
                'backstory': 'Strategic mind and eye for detail'
            }
        }
        
        agent = crew_instance.resume_strategist()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 4  # All tools: search, scrape, file read, mdx search
        assert agent.verbose is True
    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    def test_interview_preparer_agent_creation(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that interview preparer agent is created with correct configuration"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        crew_instance.read_resume = Mock()
        crew_instance.semantic_search_resume = Mock()
        
        crew_instance.agents_config = {
            'interview_preparer': {
                'role': 'Engineering Interview Preparer',
                'goal': 'Create interview questions and talking points',
                'backstory': 'Crucial role in anticipating interview dynamics'
            }
        }
        
        agent = crew_instance.interview_preparer()
        
        assert isinstance(agent, Agent)
        assert len(agent.tools) == 4  # All tools: search, scrape, file read, mdx search
        assert agent.verbose is True
    def test_agent_tool_distribution(self, mock_mdx_attr, mock_file_attr, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that agents have correct tool distribution"""
        mock_search_instance = Mock()
        mock_scrape_instance = Mock()
        mock_file_instance = Mock()
        mock_mdx_instance = Mock()
        
        mock_search_tool.return_value = mock_search_instance
        mock_scrape_tool.return_value = mock_scrape_instance
        mock_file_attr.return_value = mock_file_instance
        mock_mdx_attr.return_value = mock_mdx_instance
        
        crew_instance.agents_config = {
            'researcher': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'profiler': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'resume_strategist': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'interview_preparer': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'}
        }
        
        researcher = crew_instance.researcher()
        profiler = crew_instance.profiler()
        resume_strategist = crew_instance.resume_strategist()
        interview_preparer = crew_instance.interview_preparer()
        
        # Researcher should only have search and scrape tools
        assert len(researcher.tools) == 2
        assert mock_search_instance in researcher.tools
        assert mock_scrape_instance in researcher.tools
        
        # Other agents should have all 4 tools
        for agent in [profiler, resume_strategist, interview_preparer]:
            assert len(agent.tools) == 4
            assert mock_search_instance in agent.tools
            assert mock_scrape_instance in agent.tools
            assert mock_file_instance in agent.tools
            assert mock_mdx_instance in agent.tools

    def test_agents_config_loading(self, crew_instance):
        """Test that agents configuration is properly loaded"""
        assert crew_instance.agents_config == 'config/agents.yaml'

    def test_tools_initialization(self, crew_instance):
        """Test that tools are properly initialized at class level"""
        assert hasattr(crew_instance, 'search_tool')
        assert hasattr(crew_instance, 'scrape_tool')
        assert hasattr(crew_instance, 'read_resume')
        assert hasattr(crew_instance, 'semantic_search_resume')

    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    def test_file_read_tool_configuration(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that FileReadTool is configured with correct file path"""
        assert hasattr(crew_instance, 'read_resume')

    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    def test_mdx_search_tool_configuration(self, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that MDXSearchTool is configured with correct file path"""
        assert hasattr(crew_instance, 'semantic_search_resume')

    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    @patch.object(JobsearchCrewCrew, 'read_resume')
    @patch.object(JobsearchCrewCrew, 'semantic_search_resume')
    def test_agent_verbose_settings(self, mock_mdx_attr, mock_file_attr, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that all agents have verbose mode enabled"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        mock_file_attr.return_value = Mock()
        mock_mdx_attr.return_value = Mock()
        
        crew_instance.agents_config = {
            'researcher': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'profiler': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'resume_strategist': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'},
            'interview_preparer': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'}
        }
        
        agents = [
            crew_instance.researcher(),
            crew_instance.profiler(),
            crew_instance.resume_strategist(),
            crew_instance.interview_preparer()
        ]
        
        # All agents should have verbose mode enabled
        for agent in agents:
            assert agent.verbose is True

    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    @patch.object(JobsearchCrewCrew, 'read_resume')
    @patch.object(JobsearchCrewCrew, 'semantic_search_resume')
    def test_agent_delegation_settings(self, mock_mdx_attr, mock_file_attr, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test that agents have default delegation settings (no explicit setting means default)"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        mock_file_attr.return_value = Mock()
        mock_mdx_attr.return_value = Mock()
        
        crew_instance.agents_config = {
            'researcher': {'role': 'Test', 'goal': 'Test', 'backstory': 'Test'}
        }
        
        agent = crew_instance.researcher()
        
        # Since allow_delegation is not explicitly set, it should use default
        # This test verifies the agent is created successfully without explicit delegation setting
        assert isinstance(agent, Agent)

    @patch('jobsearch_crew.crew.SerperDevTool')
    @patch('jobsearch_crew.crew.ScrapeWebsiteTool')
    @patch.object(JobsearchCrewCrew, 'read_resume')
    @patch.object(JobsearchCrewCrew, 'semantic_search_resume')
    def test_agent_error_handling(self, mock_mdx_attr, mock_file_attr, mock_scrape_tool, mock_search_tool, crew_instance):
        """Test agent creation with missing configuration"""
        mock_search_tool.return_value = Mock()
        mock_scrape_tool.return_value = Mock()
        mock_file_attr.return_value = Mock()
        mock_mdx_attr.return_value = Mock()
        
        # Test with empty config
        crew_instance.agents_config = {}
        
        with pytest.raises(KeyError):
            crew_instance.researcher()

    def test_crew_class_attributes(self, crew_instance):
        """Test that crew class has required attributes"""
        assert crew_instance.agents_config == 'config/agents.yaml'
        assert crew_instance.tasks_config == 'config/tasks.yaml'
        assert hasattr(crew_instance, 'search_tool')
        assert hasattr(crew_instance, 'scrape_tool')
        assert hasattr(crew_instance, 'read_resume')
        assert hasattr(crew_instance, 'semantic_search_resume')