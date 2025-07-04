"""
Module Creation Engine for Engineering Team AI Agent
Handles individual module creation, validation, and retry logic
"""

import os
import ast
import re
from typing import Dict, Any, List
from crewai import Task, Crew, Process
from .models import SystemArchitecture, ModuleSpec, ModuleCreationState
from .crew import EngineeringTeam
from .config import config


class ModuleCreator:
    """Handles module creation with retry logic and validation"""

    def __init__(self, crew: EngineeringTeam):
        self.crew = crew
        self.module_interfaces = {}  # Track extracted interfaces from each module

    def create_modules(
        self, architecture: SystemArchitecture, module_state: ModuleCreationState
    ) -> Dict[str, Any]:
        """
        Create all modules based on the architecture with validation
        """
        print(f"🔧 Starting module creation for {len(architecture.modules)} modules...")

        # CRITICAL: Hard validation - FAIL THE ENTIRE FLOW if UI modules detected
        ui_modules = [
            m
            for m in architecture.modules
            if any(
                term in m.name.lower()
                for term in ["ui", "interface", "frontend", "web", "gui"]
            )
        ]

        if ui_modules:
            error_msg = f"🚫 FLOW TERMINATION: UI modules detected in architecture: {[m.name for m in ui_modules]}"
            print(error_msg)
            print(
                "🚫 This violates our Gradio-only constraint. The flow cannot continue."
            )
            raise ValueError(
                f"UI modules not allowed: {[m.name for m in ui_modules]}. All UI must use Gradio in app.py"
            )

        created_modules = {}

        # Create modules one by one based on dependencies
        while not module_state.is_system_complete():
            next_module = module_state.get_next_module()

            if not next_module:
                print("❌ No more modules can be created (circular dependency?)")
                break

            # ADDITIONAL SAFETY: Double-check each module before creation
            if any(
                term in next_module.name.lower()
                for term in ["ui", "interface", "frontend", "web", "gui"]
            ):
                print(
                    f"🚫 SKIPPING UI MODULE: {next_module.name} (Gradio-only enforcement)"
                )
                module_state.mark_module_completed(next_module.name)
                continue

            print(f"📦 Creating module: {next_module.name}")
            module_state.mark_module_in_progress(next_module.name)

            # Create module-specific tasks with retry logic
            module_result = self._create_single_module_with_retry(
                next_module, architecture
            )
            created_modules[next_module.name] = module_result

            module_state.mark_module_completed(next_module.name)
            print(f"✅ Completed module: {next_module.name}")

        return {
            "architecture": architecture,
            "modules": created_modules,
            "state": module_state,
        }

    def _create_single_module_with_retry(
        self,
        module_spec: ModuleSpec,
        architecture: SystemArchitecture,
        max_retries: int = 2,
    ) -> Dict[str, Any]:
        """Create a single module with retry logic for validation failures"""

        for attempt in range(max_retries + 1):
            print(f"🔄 Attempt {attempt + 1}/{max_retries + 1} for {module_spec.name}")

            # Generate module
            if attempt == 0:
                # First attempt - normal creation
                module_result = self._create_single_module(module_spec, architecture)
            else:
                # Retry with error feedback
                module_result = self._retry_module_with_feedback(
                    module_spec, architecture, previous_result, validation_issues
                )

            # Validate the module interface
            validation_issues = self._validate_module_interface(
                module_spec, module_result["interface"]
            )

            if not validation_issues:
                print(
                    f"✅ {module_spec.name} validation passed on attempt {attempt + 1}"
                )
                return module_result
            else:
                print(
                    f"⚠️  Validation issues found in {module_spec.name} (attempt {attempt + 1}):"
                )
                for issue in validation_issues:
                    print(f"   - {issue}")

                if attempt < max_retries:
                    print(f"🔁 Retrying {module_spec.name} with error feedback...")
                    previous_result = module_result
                else:
                    print(
                        f"❌ Failed to create valid {module_spec.name} after {max_retries + 1} attempts"
                    )

        # Return final result even if validation failed
        return module_result

    def _create_single_module(
        self, module_spec: ModuleSpec, architecture: SystemArchitecture
    ) -> Dict[str, Any]:
        """Create a single module with design and implementation"""

        # Get specific interfaces for dependencies only
        dependency_info = ""
        if module_spec.dependencies:
            specific_interfaces = self._get_specific_interface(module_spec.dependencies)
            dependency_info = f"\\nDEPENDENCY INTERFACES:\\n{specific_interfaces}"

        # Design task with module-specific requirements
        module_requirements = self._get_module_specific_requirements(
            module_spec, architecture
        )

        design_task = Task(
            description=f"""
            Create EXACT technical specification for {module_spec.name} module.
            
            Module: {module_spec.name}
            Class: {module_spec.class_name}
            Purpose: {module_spec.purpose}
            Dependencies: {', '.join(module_spec.dependencies) if module_spec.dependencies else 'None'}
            {dependency_info}
            
            SPECIFIC REQUIREMENTS FOR {module_spec.name.upper()}:
            {module_requirements}
            
            MANDATORY DESIGN ELEMENTS:
            1. Class definition: class {module_spec.class_name}:
            2. Constructor with EXACT parameters as specified
            3. ALL required methods with EXACT signatures from requirements
            4. Environment variable loading (os.getenv) where specified
            5. Real API integration (not mocks) using environment variables
            6. Type hints for ALL parameters and return types
            7. Comprehensive error handling for API failures
            8. Input validation and parsing for string parameters
            
            REQUIRED INTERFACES (must implement exactly):
            {', '.join(module_spec.interfaces)}
            
            OUTPUT: Technical specification with exact method signatures, constructor requirements, and environment variable usage.
            """,
            expected_output=f"Complete technical specification for {module_spec.name} with exact interface compliance",
            agent=self.crew.engineering_lead(),
        )

        # Code task
        code_task = Task(
            description=f"""
            Implement {module_spec.name} module EXACTLY as specified in the design specification.
            
            Module: {module_spec.name}
            Class: {module_spec.class_name}
            Required Methods: {', '.join(module_spec.interfaces)}
            {dependency_info}
            
            SPECIFIC IMPLEMENTATION FOR {module_spec.name.upper()}:
            {module_requirements}
            
            MANDATORY IMPLEMENTATION REQUIREMENTS:
            1. Import required libraries: os, requests, json, typing
            2. Analyze requirements for external service dependencies  
            3. Load credentials via environment variables (os.getenv()) for external services
            4. Implement EXACT constructor signature from design
            5. Implement ALL {len(module_spec.interfaces)} required methods exactly
            6. Use real API calls with proper error handling (not mocks)
            7. Parse and validate all inputs appropriately
            8. Return correctly typed outputs as specified
            9. Handle network errors and API failures gracefully
            10. Include comprehensive docstrings for each method
            11. Validate inputs and handle edge cases
            
            CRITICAL CHECKLIST:
            ✓ Class {module_spec.class_name} with correct constructor
            ✓ Environment variables loaded with os.getenv()
            ✓ All {len(module_spec.interfaces)} required methods implemented
            ✓ Real API integration (no print statements for external calls)
            ✓ Proper error handling for API failures
            ✓ Input validation and JSON parsing where needed
            ✓ Type hints on all methods and parameters
            
            OUTPUT: Raw Python code only (no markdown, no code blocks, no backticks)
            """,
            expected_output=f"Complete Python implementation of {module_spec.name} with real API integration",
            agent=self.crew.backend_engineer(),
            context=[design_task],
        )

        # Execute tasks
        mini_crew = Crew(
            agents=[self.crew.engineering_lead(), self.crew.backend_engineer()],
            tasks=[design_task, code_task],
            process=Process.sequential,
            verbose=True,
        )

        result = mini_crew.kickoff()

        # Save the module file
        module_path = config.get_module_path(module_spec.name)
        with open(module_path, "w") as f:
            f.write(str(result))

        # Extract and store the module interface
        module_interface = self._extract_module_interface(module_spec.name, str(result))
        self.module_interfaces[module_spec.name] = module_interface

        print(
            f"📋 Extracted interface for {module_spec.name}: {len(module_interface['classes'])} classes, {len(module_interface['functions'])} functions"
        )

        # Module creation completed (validation handled by retry wrapper)
        print(f"📦 {module_spec.name} module generated")

        return {
            "design": design_task.output,
            "code": result,
            "file_path": str(module_path),
            "interface": module_interface,
            "validation_issues": [],  # Validation handled by retry wrapper
        }

    def _retry_module_with_feedback(
        self,
        module_spec: ModuleSpec,
        architecture: SystemArchitecture,
        previous_result: Dict[str, Any],
        validation_issues: List[str],
    ) -> Dict[str, Any]:
        """Retry module creation with error feedback"""

        # Get dependency info
        dependency_info = ""
        if module_spec.dependencies:
            specific_interfaces = self._get_specific_interface(module_spec.dependencies)
            dependency_info = f"\\nDEPENDENCY INTERFACES:\\n{specific_interfaces}"

        # Get module requirements
        module_requirements = self._get_module_specific_requirements(
            module_spec, architecture
        )

        # Create error feedback task
        retry_task = Task(
            description=f"""
            Fix the validation issues in {module_spec.name} module implementation.
            
            MODULE SPECIFICATION:
            - Module: {module_spec.name}
            - Class: {module_spec.class_name}
            - Purpose: {module_spec.purpose}
            - Required Methods: {', '.join(module_spec.interfaces)}
            {dependency_info}
            
            ORIGINAL CODE THAT FAILED VALIDATION:
            {previous_result['code']}
            
            VALIDATION ERRORS FOUND:
            {chr(10).join([f"- {issue}" for issue in validation_issues])}
            
            MODULE REQUIREMENTS:
            {module_requirements}
            
            ERROR CORRECTION INSTRUCTIONS:
            1. Analyze each validation error listed above
            2. Fix the specific issues while maintaining working functionality
            3. Ensure ALL required methods from interfaces are implemented: {', '.join(module_spec.interfaces)}
            4. Ensure the main class is named exactly: {module_spec.class_name}
            5. Keep all working code and only fix the identified problems
            6. Maintain proper type hints and error handling
            7. Ensure environment variables are loaded correctly if needed
            
            CRITICAL FIXES NEEDED:
            - Add any missing required methods
            - Fix class naming issues
            - Ensure constructor (__init__) exists
            - Fix any import or dependency issues
            
            OUTPUT: Corrected Python code only (no markdown, no code blocks, no backticks)
            """,
            expected_output=f"Corrected Python implementation of {module_spec.name} with validation issues fixed",
            agent=self.crew.backend_engineer(),
        )

        # Execute the retry task
        mini_crew = Crew(
            agents=[self.crew.backend_engineer()],
            tasks=[retry_task],
            process=Process.sequential,
            verbose=True,
        )

        result = mini_crew.kickoff()

        # Save the corrected module file
        module_path = config.get_module_path(module_spec.name)
        with open(module_path, "w") as f:
            f.write(str(result))

        # Extract and store the module interface
        module_interface = self._extract_module_interface(module_spec.name, str(result))
        self.module_interfaces[module_spec.name] = module_interface

        print(
            f"🔧 Re-extracted interface for {module_spec.name}: {len(module_interface['classes'])} classes, {len(module_interface['functions'])} functions"
        )

        return {
            "design": previous_result.get("design", "Retry attempt - no design phase"),
            "code": result,
            "file_path": str(module_path),
            "interface": module_interface,
            "validation_issues": [],  # Will be validated by retry wrapper
        }

    def _get_specific_interface(self, dependencies: List[str]) -> str:
        """Get interface details for specific dependencies"""
        interface_details = []
        for dep in dependencies:
            if dep in self.module_interfaces:
                interface = self.module_interfaces[dep]
                dep_details = f"Module: {dep}\\n"

                for class_name, methods in interface["classes"].items():
                    dep_details += f"  Class {class_name}:\\n"
                    for method in methods:
                        dep_details += f"    - {method}\\n"

                for func in interface["functions"]:
                    dep_details += f"  Function: {func}\\n"

                interface_details.append(dep_details)
            else:
                interface_details.append(f"Module: {dep} (interface not yet available)")

        return "\\n".join(interface_details)

    def _get_module_specific_requirements(
        self, module_spec: ModuleSpec, architecture: SystemArchitecture
    ) -> str:
        """Generate module-specific requirements based on the system context"""
        return f"""
        Based on the {architecture.system_name} system requirements:
        
        1. This module ({module_spec.name}) is responsible for: {module_spec.purpose}
        2. It must implement these interfaces: {', '.join(module_spec.interfaces)}
        3. Dependencies: {', '.join(module_spec.dependencies) if module_spec.dependencies else 'None'}
        4. Priority level: {module_spec.priority}
        
        The module should integrate seamlessly with the overall system architecture.
        Use environment variables for any external service credentials.
        Implement proper error handling and input validation.
        """

    def _extract_module_interface(self, module_name: str, code: str) -> Dict[str, Any]:
        """Extract class and function interfaces from module code using AST"""
        try:
            tree = ast.parse(code)

            classes = {}
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_methods = []
                    for item in node.body:
                        if isinstance(
                            item, ast.FunctionDef
                        ) and not item.name.startswith("_"):
                            # Extract method signature
                            args = [
                                arg.arg for arg in item.args.args[1:]
                            ]  # Skip 'self'
                            method_sig = f"{item.name}({', '.join(args)})"
                            class_methods.append(method_sig)
                    classes[node.name] = class_methods

                elif isinstance(node, ast.FunctionDef) and not node.name.startswith(
                    "_"
                ):
                    # Top-level function
                    args = [arg.arg for arg in node.args.args]
                    func_sig = f"{node.name}({', '.join(args)})"
                    functions.append(func_sig)

            return {"classes": classes, "functions": functions}

        except Exception as e:
            print(f"⚠️  Could not parse {module_name}: {e}")
            return {"classes": {}, "functions": []}

    def _validate_module_interface(
        self, module_spec: ModuleSpec, interface: Dict[str, Any]
    ) -> List[str]:
        """Validate that the module implements required interfaces"""
        issues = []

        # Check if main class exists
        if module_spec.class_name not in interface["classes"]:
            issues.append(f"Main class '{module_spec.class_name}' not found")
        else:
            # Check if required methods are implemented
            class_methods = interface["classes"][module_spec.class_name]
            implemented_methods = [method.split("(")[0] for method in class_methods]

            for required_method in module_spec.interfaces:
                if required_method not in implemented_methods:
                    issues.append(
                        f"Required method '{required_method}' not implemented in {module_spec.class_name}"
                    )

        return issues
