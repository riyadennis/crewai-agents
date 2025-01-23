python3 -m venv crewai 
source crewai/bin/activate
pip install -r requirements.txt
pip install setuptools --force-reinstall

crewai create realestate-agent
crewai create jobsearch-crew
