from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ModuleSpec(BaseModel):
    """Specification for a single module to be created"""

    name: str = Field(
        ..., description="Name of the module (e.g., 'user_management.py')"
    )
    class_name: str = Field(..., description="Main class name in the module")
    purpose: str = Field(..., description="What this module does")
    dependencies: List[str] = Field(
        default_factory=list, description="Other modules this depends on"
    )
    interfaces: List[str] = Field(
        default_factory=list, description="Key methods/interfaces this module provides"
    )
    priority: int = Field(1, description="Creation priority (1=highest)")


class SystemArchitecture(BaseModel):
    """Overall system architecture specification"""

    system_name: str = Field(..., description="Name of the overall system")
    description: str = Field(..., description="What the system does")
    modules: List[ModuleSpec] = Field(..., description="List of modules to create")
    assembly_instructions: str = Field(
        ..., description="How modules should be integrated"
    )


class ModuleCreationState(BaseModel):
    """State tracking for module creation process"""

    architecture: SystemArchitecture
    completed_modules: List[str] = Field(default_factory=list)
    in_progress_modules: List[str] = Field(default_factory=list)
    pending_modules: List[str] = Field(default_factory=list)

    def get_next_module(self) -> Optional[ModuleSpec]:
        """Get the next module to create based on dependencies and priority"""
        available_modules = [
            module
            for module in self.architecture.modules
            if module.name not in self.completed_modules
            and module.name not in self.in_progress_modules
            and all(dep in self.completed_modules for dep in module.dependencies)
        ]

        if not available_modules:
            return None

        # Sort by priority (lower number = higher priority)
        return min(available_modules, key=lambda m: m.priority)

    def mark_module_in_progress(self, module_name: str):
        """Mark a module as being worked on"""
        if module_name in self.pending_modules:
            self.pending_modules.remove(module_name)
        if module_name not in self.in_progress_modules:
            self.in_progress_modules.append(module_name)

    def mark_module_completed(self, module_name: str):
        """Mark a module as completed"""
        if module_name in self.in_progress_modules:
            self.in_progress_modules.remove(module_name)
        if module_name not in self.completed_modules:
            self.completed_modules.append(module_name)

    def is_system_complete(self) -> bool:
        """Check if all modules are completed"""
        return len(self.completed_modules) == len(self.architecture.modules)
