#!/usr/bin/env python
import sys
import warnings
import os
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from engineering_team.flow import EngineeringFlow
from engineering_team.config import config

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_requirements():
    """Get requirements from req.txt file or interactive input"""
    
    # Check for command line argument for interactive mode
    parser = argparse.ArgumentParser(description='Engineering Team AI Agent - Create any software system')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode to input requirements')
    
    args = parser.parse_args()
    
    if args.interactive:
        print("🤖 Engineering Team AI Agent")
        print("=" * 50)
        print("Enter your software requirements (type 'END' on a new line when finished):")
        print()
        
        lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        
        requirements = '\n'.join(lines).strip()
        if not requirements:
            print("No requirements provided. Exiting.")
            sys.exit(1)
        return requirements
    
    # Default: read from req.txt file
    if config.requirements_file.exists():
        with open(config.requirements_file, 'r') as f:
            return f.read().strip()
    else:
        print(f"Error: {config.requirements_file} not found. Use --interactive or create req.txt file.")
        sys.exit(1)



def get_dynamic_file_descriptions(output_dir: Path, result: dict) -> dict:
    """Generate file descriptions based on actual generated content and architecture"""
    descriptions = {}
    
    # Extract from architecture data if available
    if isinstance(result, dict) and 'modules' in result:
        modules = result.get('modules', {})
        for module_name, module_data in modules.items():
            if isinstance(module_data, dict) and 'interface' in module_data:
                interface = module_data['interface']
                if isinstance(interface, dict) and 'classes' in interface:
                    classes = list(interface['classes'].keys())
                    if classes:
                        class_name = classes[0]
                        descriptions[module_name] = f"📦 {class_name} module"
                else:
                    descriptions[module_name] = "📦 Generated module"
    
    # Standard file patterns and naming conventions
    for file_path in output_dir.glob('*.py'):
        file_name = file_path.name
        
        if file_name not in descriptions:
            # Read first few lines to get class/function names for better descriptions
            try:
                with open(file_path, 'r') as f:
                    content = f.read(500)  # Read first 500 chars for analysis
                    
                if 'class' in content:
                    # Extract class name for better description
                    import re
                    class_match = re.search(r'class\s+(\w+)', content)
                    if class_match:
                        class_name = class_match.group(1)
                        descriptions[file_name] = f"📦 {class_name} implementation"
                    else:
                        descriptions[file_name] = "📦 Class-based module"
                elif 'def ' in content and 'gradio' in content.lower():
                    descriptions[file_name] = "🖥️  User interface module"
                elif 'def ' in content:
                    descriptions[file_name] = "⚙️  Function-based module"
                else:
                    descriptions[file_name] = "📄 Generated module"
                    
            except Exception:
                # Truly dynamic fallback - convert filename to user-friendly description
                clean_name = file_name.replace('.py', '').replace('_', ' ').title()
                descriptions[file_name] = f'📄 {clean_name} module'
    
    return descriptions

def display_completion_summary(result, requirements):
    """
    Display a clean, user-friendly completion summary instead of blob output
    """
    print()
    print("🎉 Engineering Flow Completed Successfully!")
    print("=" * 60)
    
    # Extract key information from result
    if isinstance(result, dict):
        architecture = result.get('architecture')
        modules = result.get('modules', {})
        integration_issues = result.get('integration_issues', [])
        
        if architecture:
            print(f"📊 System Built: {architecture.system_name}")
            print(f"📝 Description: {architecture.description}")
            print(f"🔧 Modules Created: {len(modules)}")
    
    # List generated files with dynamic descriptions
    output_dir = config.output_path
    if output_dir.exists():
        print()
        print("📁 Generated Files:")
        print("-" * 40)
        
        # Get dynamic file descriptions based on actual content
        file_descriptions = get_dynamic_file_descriptions(output_dir, result)
        
        # Show Python files
        for file_path in sorted(output_dir.glob('*.py')):
            file_size = file_path.stat().st_size
            description = file_descriptions.get(file_path.name, '📄 Generated module')
            print(f"  {description}")
            print(f"     └─ {file_path.name} ({file_size:,} bytes)")
        
        # Show documentation files
        doc_files = {
            'README.md': '📖 Project documentation and setup guide',
            '.env.example': '⚙️  Environment variables template',
            'requirements.txt': '📦 Python dependencies list',
            'flow_results.json': '🔍 Detailed generation results (for debugging)'
        }
        
        for doc_file, description in doc_files.items():
            file_path = output_dir / doc_file
            if file_path.exists():
                file_size = file_path.stat().st_size
                print(f"  {description}")
                print(f"     └─ {doc_file} ({file_size:,} bytes)")
    
    # Show integration status
    if isinstance(result, dict):
        integration_issues = result.get('integration_issues', [])
        if integration_issues:
            print()
            print("⚠️  Integration Issues Found:")
            for issue in integration_issues:
                print(f"   - {issue}")
        else:
            print()
            print("✅ All integration validations passed")
    
    # Next steps
    print()
    print("🚀 Next Steps:")
    print("-" * 20)
    print("1. Read the README.md for detailed setup instructions")
    print("2. Navigate to the output directory: cd output")
    print("3. Configure environment variables (copy .env.example to .env)")
    print("4. Install dependencies: pip install -r requirements.txt")
    print("5. Run the application: python app.py")
    print("6. Open your browser to the displayed URL")
    print("7. Run tests: python test_system.py")
    
    print()
    print("💡 Your system is ready to use!")
    print("=" * 60)
    print()
    print("🔧 Agent Improvements Applied:")
    print("✅ Requirements.txt excludes local modules (only external packages)")
    print("✅ UI architecture optimized for framework-specific patterns")
    print("✅ Documentation automatically generated and scanned")

def scan_environment_variables(output_dir: Path) -> dict:
    """Scan all Python files for environment variables and create .env template"""
    env_vars = {}
    import re
    
    # Pattern to match os.getenv() calls
    getenv_pattern = r"os\.getenv\s*\(\s*['\"]([^'\"]+)['\"](?:\s*,\s*(?:default\s*=\s*)?['\"]([^'\"]*)['\"])?\s*\)"
    
    for py_file in output_dir.glob('*.py'):
        try:
            with open(py_file, 'r') as f:
                content = f.read()
                
            matches = re.findall(getenv_pattern, content)
            for match in matches:
                var_name = match[0]
                default_value = match[1] if len(match) > 1 else ''
                
                # Try to infer description from variable name
                description = generate_env_description(var_name)
                
                env_vars[var_name] = {
                    'default': default_value,
                    'description': description,
                    'found_in': py_file.name
                }
                
        except Exception as e:
            print(f"⚠️  Could not scan {py_file.name}: {e}")
    
    return env_vars

def generate_env_description(var_name: str) -> str:
    """Generate human-readable description from environment variable name"""
    var_lower = var_name.lower()
    
    if 'api_key' in var_lower:
        return "API key for external service integration"
    elif 'secret' in var_lower:
        return "Secret key for authentication"
    elif 'token' in var_lower:
        return "Authentication token"
    elif 'url' in var_lower or 'endpoint' in var_lower:
        return "Service endpoint URL"
    elif 'database' in var_lower or 'db' in var_lower:
        return "Database connection string"
    elif 'email' in var_lower:
        return "Email service configuration"
    elif 'port' in var_lower:
        return "Service port number"
    elif 'host' in var_lower:
        return "Service host address"
    else:
        return f"Configuration value for {var_name.replace('_', ' ').lower()}"

def create_env_template(env_vars: dict, output_dir: Path):
    """Create .env.example file with all discovered environment variables"""
    if not env_vars:
        return
    
    env_content = """# Environment Variables Configuration
# Copy this file to .env and fill in your actual values
# DO NOT commit .env to version control

"""
    
    for var_name, var_info in sorted(env_vars.items()):
        env_content += f"# {var_info['description']}\n"
        env_content += f"# Found in: {var_info['found_in']}\n"
        
        if var_info['default']:
            env_content += f"{var_name}={var_info['default']}\n"
        else:
            env_content += f"{var_name}=your_value_here\n"
        env_content += "\n"
    
    try:
        env_file = output_dir / '.env.example'
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"📄 Environment template created: {env_file}")
    except Exception as e:
        print(f"⚠️  Could not create .env.example: {e}")

def analyze_imports_and_create_requirements(output_dir: Path):
    """Analyze Python imports and create requirements.txt"""
    imports = set()
    import re
    
    # Standard library modules (don't include in requirements)
    stdlib_modules = {
        'os', 'sys', 'json', 'datetime', 'pathlib', 'typing', 'ast', 're', 
        'math', 'statistics', 'collections', 'itertools', 'functools', 'unittest',
        'time', 'random', 'copy', 'logging', 'argparse', 'glob', 'subprocess'
    }
    
    # Get local module names (files in output directory)
    local_modules = {f.stem for f in output_dir.glob('*.py')}
    
    for py_file in output_dir.glob('*.py'):
        try:
            with open(py_file, 'r') as f:
                content = f.read()
            
            # Find import statements
            import_matches = re.findall(r'^\s*(?:from\s+(\w+)|import\s+(\w+))', content, re.MULTILINE)
            for match in import_matches:
                module = match[0] or match[1]
                # Only include if it's not stdlib, not local module, and not a .py file
                if (module and 
                    module not in stdlib_modules and 
                    module not in local_modules and 
                    not module.endswith('.py')):
                    imports.add(module)
                    
        except Exception as e:
            print(f"⚠️  Could not analyze imports in {py_file.name}: {e}")
    
    # Create requirements.txt
    if imports:
        requirements_content = "# Python package requirements\n"
        
        # Map common import names to package names with versions
        package_mapping = {
            'gradio': 'gradio>=4.0.0',
            'numpy': 'numpy>=1.21.0',
            'pandas': 'pandas>=1.3.0',
            'requests': 'requests>=2.28.0',
            'flask': 'Flask>=2.0.0',
            'fastapi': 'fastapi>=0.68.0',
            'streamlit': 'streamlit>=1.0.0',
            'pytest': 'pytest>=7.0.0',
            'django': 'Django>=4.0.0',
            'sqlalchemy': 'SQLAlchemy>=1.4.0'
        }
        
        for imp in sorted(imports):
            package_name = package_mapping.get(imp, imp)
            requirements_content += f"{package_name}\n"
        
        try:
            req_file = output_dir / 'requirements.txt'
            with open(req_file, 'w') as f:
                f.write(requirements_content)
            print(f"📄 Requirements file created: {req_file}")
        except Exception as e:
            print(f"⚠️  Could not create requirements.txt: {e}")

def cleanup_ui_files(output_dir: Path):
    """
    FINAL SAFETY: Remove any UI files that somehow slipped through all defenses
    """
    ui_patterns = ['ui.py', 'interface.py', 'frontend.py', 'web.py', 'gui.py', 'user_interface.py']
    cleaned_files = []
    
    for pattern in ui_patterns:
        ui_files = list(output_dir.glob(pattern))
        for ui_file in ui_files:
            try:
                ui_file.unlink()
                cleaned_files.append(ui_file.name)
                print(f"🧹 CLEANED: Removed forbidden UI file: {ui_file.name}")
            except Exception as e:
                print(f"⚠️  Could not remove {ui_file.name}: {e}")
    
    # Also check system_integration.py for UI imports and clean them
    integration_file = output_dir / 'system_integration.py'
    if integration_file.exists():
        try:
            with open(integration_file, 'r') as f:
                content = f.read()
            
            # Remove UI imports
            ui_import_patterns = [
                r'from ui import.*\n',
                r'import ui.*\n',
                r'from .*interface import.*\n',
                r'from .*frontend import.*\n',
                r'from .*gui import.*\n'
            ]
            
            modified = False
            for pattern in ui_import_patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, '', content)
                    modified = True
            
            # Remove UI object instantiation
            ui_instantiation_patterns = [
                r'self\.ui = UI\(.*\)\s*\n',
                r'ui = UI\(.*\)\s*\n',
                r'self\.ui\..*\n'
            ]
            
            for pattern in ui_instantiation_patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, '', content)
                    modified = True
            
            if modified:
                with open(integration_file, 'w') as f:
                    f.write(content)
                print(f"🧹 CLEANED: Removed UI references from {integration_file.name}")
                
        except Exception as e:
            print(f"⚠️  Could not clean integration file: {e}")
    
    if cleaned_files:
        print(f"🚫 UI ENFORCEMENT: Removed {len(cleaned_files)} forbidden UI files")
        print("✅ Gradio-only architecture maintained")

def save_detailed_results(result, requirements):
    """
    Save detailed results to JSON file for debugging/reference
    """
    try:
        # Create a serializable version of the result
        detailed_results = {
            'timestamp': datetime.now().isoformat(),
            'requirements': requirements,
            'result_summary': str(result)[:1000] + '...' if len(str(result)) > 1000 else str(result)
        }
        
        with open(config.output_path / 'flow_results.json', 'w') as f:
            json.dump(detailed_results, f, indent=2, default=str)
        
        print("💾 Detailed results saved to output/flow_results.json")
    except Exception as e:
        print(f"⚠️  Could not save detailed results: {e}")

def run():
    """
    Run the engineering flow to create a multi-service system.
    """
    # Validate configuration first
    validation_issues = config.validate_environment()
    if validation_issues:
        print("⚠️  Configuration Issues:")
        for issue in validation_issues:
            print(f"   - {issue}")
        print()
    
    # Get requirements dynamically
    requirements = get_requirements()
    
    print("🤖 Engineering Team AI Agent")
    print("=" * 50)
    print("📋 Requirements received:")
    print("-" * 30)
    print(requirements[:500] + "..." if len(requirements) > 500 else requirements)
    print("-" * 30)
    print()
    
    # Create and run the flow with dynamic requirements
    flow = EngineeringFlow(requirements=requirements)
    result = flow.kickoff()
    
    # Generate additional documentation files
    output_dir = config.output_path
    if output_dir.exists():
        print("\n📄 Generating documentation files...")
        
        # CRITICAL: Clean up any UI files that slipped through
        cleanup_ui_files(output_dir)
        
        # Scan for environment variables and create .env template
        env_vars = scan_environment_variables(output_dir)
        if env_vars:
            create_env_template(env_vars, output_dir)
            print(f"📄 Found {len(env_vars)} environment variables")
        
        # Analyze imports and create requirements.txt (improved to exclude local modules)
        analyze_imports_and_create_requirements(output_dir)
    
    # Display clean completion summary instead of blob
    display_completion_summary(result, requirements)
    
    # Save detailed results for reference
    save_detailed_results(result, requirements)
    
    # Don't return the complex result object to avoid printing blob
    return "Flow completed successfully"


if __name__ == "__main__":
    run()