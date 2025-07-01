# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is a CrewAI multi-agent framework repository containing multiple autonomous AI agent projects. Each project lives in its own directory with similar structure:

- `financial_agent/` - Multi-agent trading system with data analysis, strategy development, execution planning, and risk management agents
- `jobsearch_crew/` - Job search automation with ChromaDB for resume optimization
- `project_planning_crew/` - Project planning crew with Trello integration tools
- `sales_pipeline_crew/` - Sales pipeline management crew

Each crew follows the standard CrewAI project structure:
- `src/{crew_name}/` - Main source code
  - `crew.py` - Crew definition with agents and tasks decorated with @agent/@task/@crew
  - `main.py` - Entry point with run() function
  - `config/` - YAML configuration files for agents and tasks
  - `tools/` - Custom tools directory
- `pyproject.toml` - Poetry configuration with dependencies and scripts
- Individual README.md files per project

## Development Commands

### Environment Setup
```bash
python3 -m venv crewai 
source crewai/bin/activate
pip install -r requirements.txt
pip install setuptools --force-reinstall
```

### Creating New Crews
```bash
crewai create agent-name
```

### Running Individual Crews
Each crew has its own Poetry script defined in pyproject.toml:
```bash
# Examples:
financial_agent  # Runs financial_agent.main:run
jobsearch_crew   # Runs jobsearch_crew.main:run
```

Or run directly with Poetry from within each project directory:
```bash
cd financial_agent/
poetry run financial_agent
```

## Architecture Notes

### CrewAI Framework Patterns
- All crews inherit from `@CrewBase` class
- Agents are defined with `@agent` decorator and configured via YAML
- Tasks use `@task` decorator and reference agents
- Crews use `@crew` decorator to assemble agents and tasks
- Standard tools: `SerperDevTool` (search), `ScrapeWebsiteTool` (web scraping)

### Configuration System
- Agent configurations stored in `config/agents.yaml` with role, goal, and backstory
- Task configurations in `config/tasks.yaml` 
- Main execution parameters passed via inputs dictionary in main.py

### Dependencies
- Core: `crewai==0.28.8` with tools extras
- Common tools: `crewai_tools`, `langchain_community`
- LLM: Uses OpenAI GPT models (configured in crew.py)
- Database: ChromaDB for vector storage (jobsearch_crew)

### Custom Tools Development
- Custom tools go in `tools/` directory
- Import pattern: `from {crew_name}.tools.custom_tool import MyCustomTool`
- Examples: Trello board/card fetchers in project_planning_crew