from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task



@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True
        )
    
    @agent
    def module_integrator(self) -> Agent:
        return Agent(
            config=self.agents_config['module_integrator'],
            verbose=True
        )


    @crew
    def crew(self) -> Crew:
        """Creates the engineering crew (agents only, tasks are dynamic in flow)"""
        return Crew(
            agents=self.agents,
            tasks=[],  # Tasks are created dynamically in flow.py
            process=Process.sequential,
            verbose=True,
        )