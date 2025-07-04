"""
Engineering Flow Coordinator - Orchestrates the complete system generation process
This is the main flow coordinator that delegates to specialized modules
"""

from typing import Dict, Any
from crewai.flow.flow import Flow, start, listen
from .models import SystemArchitecture, ModuleCreationState
from .crew import EngineeringTeam
from .architecture_planner import ArchitecturePlanner
from .module_creator import ModuleCreator
from .system_assembler import SystemAssembler


class EngineeringFlow(Flow):
    """
    Main Engineering Flow that orchestrates system creation using specialized modules
    """

    def __init__(self, requirements: str = None):
        super().__init__()
        self.crew = EngineeringTeam()
        self.requirements = requirements

        # Initialize specialized modules
        self.architecture_planner = ArchitecturePlanner(self.crew)
        self.module_creator = ModuleCreator(self.crew)
        # system_assembler will be initialized after module creation to pass interfaces

    @start()
    def architecture_planning(self) -> SystemArchitecture:
        """
        PHASE 1: Engineering Lead creates the system architecture
        """
        architecture = self.architecture_planner.plan_architecture(self.requirements)

        # Initialize module state for tracking
        self.module_state = self.architecture_planner.create_module_state(architecture)

        return architecture

    @listen(architecture_planning)
    def create_modules(self, architecture: SystemArchitecture) -> Dict[str, Any]:
        """
        PHASE 2: Create all modules based on the architecture
        """
        return self.module_creator.create_modules(architecture, self.module_state)

    @listen(create_modules)
    def assemble_system(self, modules_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        PHASE 3: Create system integration, tests, and demo
        """
        architecture = modules_data["architecture"]
        modules = modules_data["modules"]

        # Initialize system assembler with module interfaces
        system_assembler = SystemAssembler(
            self.crew, self.module_creator.module_interfaces
        )

        return system_assembler.assemble_system(architecture, modules)
