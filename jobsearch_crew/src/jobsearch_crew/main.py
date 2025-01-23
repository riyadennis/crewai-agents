#!/usr/bin/env python
from jobsearch_crew.crew import JobsearchCrewCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    personalWriteUp =  """Riya Dennis is a seasoned back-end engineer based in London with twelve years 
                            of comprehensive development experience. My expertise lies in development within 
                            fully agile environments, particularly adept at microservices architecture. 
                            I am all about fostering a collaborative spirit, empowering and mentoring teams 
                            to navigate a complex and demanding technological landscape to deliver product
                            excellence and performance that surpass user expectations. """
    inputs = {
        'job_posting_url': 'https://www.sumup.com/careers/positions/london-united-kingdom/engineering/senior-backend-engineer-go-consumer-tribe-/7814508002/',
        'github_url': 'https://github.com/riyadennis',
        'personal_writeup': personalWriteUp,
    }
    JobsearchCrewCrew().crew().kickoff(inputs=inputs)