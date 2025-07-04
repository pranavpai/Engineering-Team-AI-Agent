"""
Engineering Team AI Agent Package

A multi-agent system powered by CrewAI that generates complete software systems from requirements.
"""

from .flow import EngineeringFlow
from .models import SystemArchitecture, ModuleSpec, ModuleCreationState
from .crew import EngineeringTeam

__version__ = "1.0.0"
__all__ = ["EngineeringFlow", "SystemArchitecture", "ModuleSpec", "ModuleCreationState", "EngineeringTeam"]