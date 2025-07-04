"""
System Assembly Module for Engineering Team AI Agent
Handles system integration, testing, and demo application creation
"""
import os
import re
from typing import Dict, Any, List
from crewai import Task, Crew, Process
from .models import SystemArchitecture
from .crew import EngineeringTeam
from .config import config

class SystemAssembler:
    """Handles system assembly, integration, testing, and demo creation"""
    
    def __init__(self, crew: EngineeringTeam, module_interfaces: Dict[str, Any]):
        self.crew = crew
        self.module_interfaces = module_interfaces
    
    def assemble_system(self, architecture: SystemArchitecture, modules: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assemble the complete system with integration, tests, and demo
        """
        print(f"🔗 Assembling system...")
        
        # Create system integration with retry logic
        integration_result = self._create_system_integration_with_retry(architecture, modules)
        
        # Create comprehensive tests
        test_result = self._create_system_tests(architecture, modules)
        
        # Create demo application
        demo_result = self._create_demo_application(architecture, modules)
        
        # Create comprehensive README documentation
        readme_result = self._create_readme_documentation(architecture, modules)
        
        # NOW validate integration dependencies AFTER all files are created
        integration_issues = self._validate_integration_dependencies(modules)
        if integration_issues:
            print(f"⚠️  Integration validation issues:")
            for issue in integration_issues:
                print(f"   - {issue}")
        else:
            print(f"✅ Integration dependency validation passed")
        
        print(f"✅ System assembly complete!")
        
        return {
            'architecture': architecture,
            'modules': modules,
            'integration': integration_result,
            'tests': test_result,
            'demo': demo_result,
            'readme': readme_result,
            'integration_issues': integration_issues
        }
    
    def _create_system_integration_with_retry(self, architecture: SystemArchitecture, modules: Dict[str, Any], max_retries: int = 1) -> str:
        """Create system integration with retry logic for validation failures"""
        
        for attempt in range(max_retries + 1):
            print(f"🔄 System integration attempt {attempt + 1}/{max_retries + 1}")
            
            # Generate integration code
            if attempt == 0:
                integration_result = self._create_system_integration(architecture, modules)
            else:
                integration_result = self._retry_integration_with_feedback(architecture, modules, previous_result, validation_issues)
            
            # Validate the integration code quality
            validation_issues = self._validate_generated_code_quality(integration_result, "system_integration.py", architecture)
            
            if not validation_issues:
                print(f"✅ System integration validation passed on attempt {attempt + 1}")
                return integration_result
            else:
                print(f"⚠️  Integration validation issues (attempt {attempt + 1}):")
                for issue in validation_issues:
                    print(f"   - {issue}")
                
                if attempt < max_retries:
                    print(f"🔁 Retrying system integration with error feedback...")
                    previous_result = integration_result
                else:
                    print(f"❌ Integration validation failed after {max_retries + 1} attempts")
        
        return integration_result
    
    def _create_system_integration(self, architecture: SystemArchitecture, modules: Dict[str, Any]) -> str:
        """Create system integration code"""
        
        # Generate interface summary for the integrator
        interfaces_summary = self._get_available_interfaces_summary()
        
        # Build dynamic module imports and initialization for integration
        module_imports = []
        module_initializations = []
        integration_methods = []
        
        for module_spec in architecture.modules:
            class_name = module_spec.class_name
            module_file = module_spec.name.replace('.py', '')
            module_imports.append(f"from {module_file} import {class_name}")
            
            # Build initialization code with dependencies
            var_name = f"self.{class_name.lower().replace('engine', '_engine').replace('system', '_system')}"
            if module_spec.dependencies:
                deps = []
                for dep in module_spec.dependencies:
                    dep_class = next((m.class_name for m in architecture.modules if m.name == dep), None)
                    if dep_class:
                        dep_var = f"self.{dep_class.lower().replace('engine', '_engine').replace('system', '_system')}"
                        deps.append(dep_var)
                
                if deps:
                    init_code = f"{var_name} = {class_name}({', '.join(deps)})"
                else:
                    init_code = f"{var_name} = {class_name}()"
            else:
                init_code = f"{var_name} = {class_name}()"
            
            module_initializations.append(init_code)
            
            # Generate integration methods for each interface
            for method in module_spec.interfaces:
                integration_methods.append(f"""
    def {method}(self, *args, **kwargs):
        \"\"\"Delegate {method} to {class_name}\"\"\"
        try:
            return {var_name}.{method}(*args, **kwargs)
        except Exception as e:
            print(f"Error in {method}: {{e}}")
            return None""")
        
        integration_class_name = f"{architecture.system_name.replace(' ', '').replace('-', '')}Integration"
        
        integration_task = Task(
            description=f"""
            Create a system integration module for {architecture.system_name}.
            
            SYSTEM INFORMATION:
            Name: {architecture.system_name}
            Description: {architecture.description}
            Modules: {', '.join(modules.keys())}
            Assembly Instructions: {architecture.assembly_instructions}
            
            DYNAMIC MODULE IMPORTS (use exactly these):
            {chr(10).join(module_imports)}
            
            DYNAMIC MODULE INITIALIZATION:
            {chr(10).join(module_initializations)}
            
            AVAILABLE MODULE INTERFACES:
            {interfaces_summary}
            
            INTEGRATION CLASS REQUIREMENTS:
            1. Create class {integration_class_name}
            2. Initialize all modules in __init__ method with proper error handling
            3. Handle module dependencies according to assembly instructions
            4. Create delegated methods for key functionality
            5. Provide unified interface to the entire system
            6. Include comprehensive error handling
            7. Add cleanup methods if needed
            
            IMPLEMENTATION STRUCTURE:
            - Import statements for all modules
            - Integration class definition
            - Constructor with module initialization
            - Delegated methods for core functionality
            - Error handling and logging
            - Cleanup methods
            
            OUTPUT: Raw Python code only (no markdown, no code blocks)
            """,
            expected_output=f"System integration Python code for {architecture.system_name}",
            agent=self.crew.module_integrator()
        )
        
        mini_crew = Crew(
            agents=[self.crew.module_integrator()],
            tasks=[integration_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = mini_crew.kickoff()
        
        # Save integration file
        integration_path = config.get_module_path("system_integration.py")
        with open(integration_path, 'w') as f:
            f.write(str(result))
        
        print(f"🔗 System integration module created")
        return str(result)
    
    def _create_system_tests(self, architecture: SystemArchitecture, modules: Dict[str, Any]) -> str:
        """Create comprehensive system tests"""
        
        interfaces_summary = self._get_available_interfaces_summary()
        
        test_task = Task(
            description=f"""
            Create comprehensive system tests for {architecture.system_name}.
            
            SYSTEM INFORMATION:
            System: {architecture.system_name}
            Description: {architecture.description}
            Modules: {', '.join(modules.keys())}
            
            AVAILABLE INTERFACES FOR TESTING:
            {interfaces_summary}
            
            TEST REQUIREMENTS:
            1. Import unittest and all system modules
            2. Create test class TestSystemIntegration
            3. Test each module individually and in integration
            4. Test all major interfaces and methods
            5. Include edge cases and error handling tests
            6. Test module dependencies and data flow
            7. Include setup and teardown methods
            8. Add performance and stress tests where applicable
            
            TEST STRUCTURE:
            - Import statements
            - Test class definition
            - setUp method for test initialization
            - Individual module tests
            - Integration tests
            - Edge case tests
            - Performance tests
            - tearDown method
            
            OUTPUT: Raw Python test code only (no markdown, no code blocks)
            """,
            expected_output=f"Comprehensive test suite for {architecture.system_name}",
            agent=self.crew.test_engineer()
        )
        
        mini_crew = Crew(
            agents=[self.crew.test_engineer()],
            tasks=[test_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = mini_crew.kickoff()
        
        # Save test file
        test_path = config.get_module_path("test_system.py")
        with open(test_path, 'w') as f:
            f.write(str(result))
        
        print(f"🧪 System tests created")
        return str(result)
    
    def _create_demo_application(self, architecture: SystemArchitecture, modules: Dict[str, Any]) -> str:
        """Create demo application using Gradio"""
        
        interfaces_summary = self._get_available_interfaces_summary()
        
        demo_task = Task(
            description=f"""
            Create a comprehensive Gradio demo application for {architecture.system_name}.
            
            SYSTEM INFORMATION:
            System: {architecture.system_name}
            Description: {architecture.description}
            
            AVAILABLE MODULE INTERFACES:
            {interfaces_summary}
            
            GRADIO DEMO REQUIREMENTS:
            1. Import gradio, os, sys, pathlib, and all system modules
            2. Create intuitive UI for all major system functionality
            3. Use tabs to organize different features/modules
            4. Include proper error handling and user feedback
            5. Show real-time status and results
            6. Make the interface user-friendly and professional
            7. Include help text and examples where helpful
            8. Handle file uploads/downloads if applicable
            9. Use appropriate Gradio components for each function
            10. Include system information and credits
            
            GRADIO STRUCTURE:
            - Import statements
            - Module initialization
            - Helper functions for UI operations
            - Tab-based interface design
            - Launch configuration
            
            IMPORTANT: Only use Gradio components and functionality. Do not create or import any UI modules.
            This must be a standalone Gradio application in app.py.
            
            OUTPUT: Raw Python Gradio application code only (no markdown, no code blocks)
            """,
            expected_output=f"Complete Gradio demo application for {architecture.system_name}",
            agent=self.crew.frontend_engineer()
        )
        
        mini_crew = Crew(
            agents=[self.crew.frontend_engineer()],
            tasks=[demo_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = mini_crew.kickoff()
        
        # Save demo file
        demo_path = config.get_module_path("app.py")
        with open(demo_path, 'w') as f:
            f.write(str(result))
        
        print(f"🖥️  Gradio demo application created")
        return str(result)
    
    def _create_readme_documentation(self, architecture: SystemArchitecture, modules: Dict[str, Any]) -> str:
        """Create comprehensive README documentation"""
        
        module_list = list(modules.keys())
        interfaces_summary = self._get_available_interfaces_summary()
        
        readme_task = Task(
            description=f"""
            Create comprehensive README.md documentation for {architecture.system_name}.
            
            SYSTEM INFORMATION:
            System: {architecture.system_name}
            Description: {architecture.description}
            Modules: {', '.join(module_list)}
            
            MODULE INTERFACES:
            {interfaces_summary}
            
            README STRUCTURE:
            1. # {architecture.system_name}
            2. ## Description
            3. ## Features (based on module capabilities)
            4. ## Installation
            5. ## Environment Variables (if any detected)
            6. ## Usage
            7. ## File Structure (describe each module)
            8. ## Testing
            9. ## API Reference (document key classes and methods)
            10. ## Troubleshooting
            11. ## Contributing
            
            CONTENT REQUIREMENTS:
            - Clear, professional documentation
            - Practical usage examples
            - Setup instructions for dependencies
            - Environment variable configuration
            - Module descriptions and purposes
            - API documentation with examples
            - Common troubleshooting scenarios
            - Professional formatting with proper headers
            
            OUTPUT: Complete README.md content only (no code blocks around the entire content)
            """,
            expected_output=f"Comprehensive README.md for {architecture.system_name}",
            agent=self.crew.engineering_lead()
        )
        
        mini_crew = Crew(
            agents=[self.crew.engineering_lead()],
            tasks=[readme_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = mini_crew.kickoff()
        
        # Save README file
        readme_path = config.output_path / "README.md"
        with open(readme_path, 'w') as f:
            f.write(str(result))
        
        print(f"📖 README documentation created")
        return str(result)
    
    def _get_available_interfaces_summary(self) -> str:
        """Generate summary of all available module interfaces"""
        if not self.module_interfaces:
            return "No interfaces available yet"
        
        summary = []
        for module_name, interface in self.module_interfaces.items():
            module_summary = f"\\nModule: {module_name}\\n"
            
            for class_name, methods in interface['classes'].items():
                module_summary += f"  Class {class_name}:\\n"
                for method in methods:
                    module_summary += f"    - {method}\\n"
            
            for func in interface['functions']:
                module_summary += f"  Function: {func}\\n"
            
            summary.append(module_summary)
        
        return "".join(summary)
    
    def _validate_integration_dependencies(self, modules: Dict[str, Any]) -> List[str]:
        """Validate integration dependencies and module structure"""
        issues = []
        
        # Check for basic module structure (this is the meaningful validation)
        for module_name, module_data in modules.items():
            if 'interface' not in module_data:
                issues.append(f"Module {module_name} missing interface data")
            elif not module_data['interface']['classes']:
                issues.append(f"Module {module_name} has no classes defined")
        
        # Verify that generated files have meaningful content (not just existence)
        expected_files = ['system_integration.py', 'app.py', 'test_system.py']
        for file_name in expected_files:
            file_path = config.get_module_path(file_name)
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read().strip()
                    if len(content) < 50:  # File is too small to be meaningful
                        issues.append(f"Generated file {file_name} appears to be empty or too small")
                except Exception as e:
                    issues.append(f"Could not read generated file {file_name}: {e}")
            # Note: We don't report missing files anymore since they're created by this same process
        
        return issues
    
    def _validate_generated_code_quality(self, code: str, filename: str, architecture: SystemArchitecture) -> List[str]:
        """Validate the quality of generated code"""
        issues = []
        
        # Check for basic Python syntax issues
        if not code.strip():
            issues.append(f"{filename} is empty")
            return issues
        
        # Check for imports (especially 'import os' if environment variables are used)
        if 'os.getenv' in code and 'import os' not in code:
            issues.append(f"{filename} uses os.getenv but doesn't import os")
        
        # Check for basic class structure
        if filename == "system_integration.py":
            expected_class = f"{architecture.system_name.replace(' ', '').replace('-', '')}Integration"
            if f"class {expected_class}" not in code:
                issues.append(f"{filename} missing expected integration class: {expected_class}")
        
        return issues
    
    def _retry_integration_with_feedback(self, architecture: SystemArchitecture, modules: Dict[str, Any], 
                                       previous_result: str, validation_issues: List[str]) -> str:
        """Retry integration creation with error feedback"""
        
        interfaces_summary = self._get_available_interfaces_summary()
        
        retry_task = Task(
            description=f"""
            Fix the validation issues in the system integration code.
            
            ORIGINAL INTEGRATION CODE THAT FAILED:
            {previous_result}
            
            VALIDATION ERRORS FOUND:
            {chr(10).join([f"- {issue}" for issue in validation_issues])}
            
            SYSTEM INFORMATION:
            Name: {architecture.system_name}
            Description: {architecture.description}
            Available Interfaces: {interfaces_summary}
            
            ERROR CORRECTION INSTRUCTIONS:
            1. Fix the specific validation errors listed above
            2. Ensure all required imports are present (especially 'import os' if using os.getenv)
            3. Maintain the integration functionality
            4. Keep proper error handling and module initialization
            5. Ensure all module imports and initializations work correctly
            
            OUTPUT: Corrected Python integration code only (no markdown, no code blocks)
            """,
            expected_output=f"Corrected system integration code for {architecture.system_name}",
            agent=self.crew.module_integrator()
        )
        
        mini_crew = Crew(
            agents=[self.crew.module_integrator()],
            tasks=[retry_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = mini_crew.kickoff()
        
        # Save the corrected integration file
        integration_path = config.get_module_path("system_integration.py")
        with open(integration_path, 'w') as f:
            f.write(str(result))
        
        return str(result)