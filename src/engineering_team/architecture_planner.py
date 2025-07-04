"""
Architecture Planning Module for Engineering Team AI Agent
Handles system architecture design and validation
"""
import json
import re
from typing import Dict, Any
from crewai import Task, Crew, Process
from .models import SystemArchitecture, ModuleCreationState
from .crew import EngineeringTeam

class ArchitecturePlanner:
    """Handles architecture planning and validation"""
    
    def __init__(self, crew: EngineeringTeam):
        self.crew = crew
    
    def plan_architecture(self, requirements: str) -> SystemArchitecture:
        """
        Create system architecture based on requirements
        """
        print(f"🏗️  Starting architecture planning...")
        
        # Create the architecture planning task with dynamic prompt
        requirements_summary = requirements[:2000] + "..." if len(requirements) > 2000 else requirements
        
        architecture_task = Task(
            description=f"""
            Analyze the following software requirements and design a modular system architecture.
            
            REQUIREMENTS:
            {requirements_summary}
            
            ARCHITECTURE DESIGN INSTRUCTIONS:
            
            1. ANALYZE the requirements to identify:
               - Core functionality needed
               - Data that needs to be managed
               - External integrations required (APIs, databases, third-party services)
               - User interface needs
               - Security and performance requirements
            
            2. DESIGN 3-8 modules that will implement this system:
               - Each module should have a single responsibility
               - Modules should have clean interfaces
               - Consider dependencies between modules
               - Include data storage if needed
               - Include external integrations as separate modules
               
               ABSOLUTE UI RULES (NON-NEGOTIABLE):
               - NEVER create modules named: ui.py, user_interface.py, interface.py, frontend.py, web.py, gui.py
               - ALL user interface code goes directly in app.py using Gradio components
               - This system uses Gradio exclusively - no other UI frameworks allowed
               - Business logic modules ONLY: game logic, data storage, external APIs
               - Any UI-related modules will cause system failure
               - Gradio is the ONLY UI solution - no exceptions
            
            3. FOR EACH MODULE determine:
               - Appropriate file name (snake_case.py)
               - Main class name (PascalCase)
               - Clear purpose description
               - 2-5 key methods that define the interface
               - Dependencies on other modules
               - Priority for implementation (1=first, 2=second, etc.)
            
            4. OUTPUT REQUIREMENTS:
               - Generate appropriate system name based on requirements
               - Create descriptive system description
               - Include assembly instructions for module integration
               - CRITICAL: Only create business logic modules, never UI modules
               - All UI will be handled by app.py with Gradio (created separately)
            
            Output in this EXACT JSON format:
            {{
                "system_name": "Descriptive System Name",
                "description": "Clear description of what the system does",
                "modules": [
                    {{
                        "name": "module_name.py",
                        "class_name": "ClassName",
                        "purpose": "What this module is responsible for",
                        "dependencies": ["other_module.py"],
                        "interfaces": ["method1", "method2", "method3"],
                        "priority": 1
                    }}
                ],
                "assembly_instructions": "How modules should be integrated together, including constructor parameters and dependencies"
            }}
            
            CRITICAL: 
            - Base everything on the actual requirements provided
            - Do not assume specific technologies unless mentioned in requirements
            - Create between 3-8 modules based on complexity
            - Always include appropriate data storage modules
            - Ensure modules have clear, single responsibilities
            """,
            expected_output="JSON system architecture tailored to the specific requirements",
            agent=self.crew.engineering_lead()
        )
        
        # Execute the architecture task
        mini_crew = Crew(
            agents=[self.crew.engineering_lead()],
            tasks=[architecture_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = mini_crew.kickoff()
        
        # Parse and validate the result
        architecture = self._parse_architecture_result(result)
        validated_architecture = self._validate_and_clean_architecture(architecture)
        
        return validated_architecture
    
    def _parse_architecture_result(self, result: Any) -> SystemArchitecture:
        """Parse the architecture result from the AI agent"""
        try:
            if isinstance(result, str):
                # Extract JSON from the result if it's wrapped in other text
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    result = json_match.group()
                arch_data = json.loads(result)
            elif hasattr(result, 'raw'):
                # Handle CrewOutput object
                raw_content = result.raw
                json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
                if json_match:
                    arch_data = json.loads(json_match.group())
                else:
                    arch_data = json.loads(raw_content)
            else:
                # Fallback: convert to string and extract JSON
                raw_content = str(result)
                json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
                if json_match:
                    arch_data = json.loads(json_match.group())
                else:
                    arch_data = json.loads(raw_content)
            
            architecture = SystemArchitecture(**arch_data)
            print(f"✅ Architecture created with {len(architecture.modules)} modules")
            return architecture
            
        except Exception as e:
            print(f"❌ Error parsing architecture: {e}")
            print(f"Raw result: {result}")
            raise
    
    def _validate_and_clean_architecture(self, architecture: SystemArchitecture) -> SystemArchitecture:
        """Validate architecture and remove any UI modules"""
        # CRITICAL VALIDATION: Ensure no UI modules exist
        ui_modules = [m for m in architecture.modules 
                     if any(term in m.name.lower() for term in ['ui', 'interface', 'frontend', 'web', 'gui'])]
        
        if ui_modules:
            print(f"🚫 ARCHITECTURE VIOLATION: UI modules detected: {[m.name for m in ui_modules]}")
            print(f"🔧 Auto-removing UI modules to enforce Gradio-only architecture...")
            
            # Force remove UI modules
            architecture.modules = [m for m in architecture.modules 
                                   if not any(term in m.name.lower() for term in ['ui', 'interface', 'frontend', 'web', 'gui'])]
            
            print(f"✅ Architecture cleaned: {len(architecture.modules)} business logic modules only")
        
        return architecture
    
    def create_module_state(self, architecture: SystemArchitecture) -> ModuleCreationState:
        """Create and initialize the module creation state"""
        return ModuleCreationState(
            architecture=architecture,
            pending_modules=[module.name for module in architecture.modules]
        )