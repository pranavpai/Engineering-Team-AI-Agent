# Developer Documentation

## Engineering Team AI Agent - Developer Guide

This document provides technical details for developers working on and contributing to the Engineering Team AI Agent codebase.

> **Note**: For user installation and usage, see [README.md](README.md).

## Architecture Overview

### System Design Philosophy

The Engineering Team AI Agent follows a **modular, specialized architecture** where each component has a single, well-defined responsibility:

1. **Orchestration Layer** (`flow.py`) - Coordinates the entire process
2. **Planning Layer** (`architecture_planner.py`) - System design and validation
3. **Creation Layer** (`module_creator.py`) - Code generation with retry logic
4. **Assembly Layer** (`system_assembler.py`) - Integration, testing, and demos
5. **Configuration Layer** (`config.py`) - Centralized settings management

### Data Flow

```
Requirements (req.txt) 
    ↓
EngineeringFlow (flow.py)
    ↓
ArchitecturePlanner → SystemArchitecture
    ↓
ModuleCreator → Dict[modules]
    ↓
SystemAssembler → Complete System
    ↓
Output Directory (generated project)
```

## Module Details

### 1. Configuration Management (`config.py`)

**Purpose**: Centralized configuration and path management

**Key Features**:
- Dynamic path configuration
- Environment validation
- Configurable output directories

**Usage**:
```python
from engineering_team.config import config

# Access configured paths
output_path = config.output_path
module_path = config.get_module_path("example.py")

# Validate environment
issues = config.validate_environment()
```

**Extension Points**:
- Add new configuration options
- Implement additional validation rules
- Support for different environment profiles

### 2. Architecture Planning (`architecture_planner.py`)

**Purpose**: Designs system architecture and enforces constraints

**Key Components**:
- `plan_architecture()` - Main planning method
- `_validate_and_clean_architecture()` - UI module prevention
- `create_module_state()` - Dependency tracking

**Critical Features**:
- **UI Enforcement**: Automatically removes UI modules
- **JSON Parsing**: Robust parsing of AI agent outputs
- **Validation**: Ensures architectural consistency

**Extension Points**:
- Add new architectural patterns
- Implement additional validation rules
- Support for different module types

### 3. Module Creation (`module_creator.py`)

**Purpose**: Creates individual modules with validation and retry logic

**Key Components**:
- `create_modules()` - Main creation orchestrator
- `_create_single_module_with_retry()` - Retry logic implementation
- `_extract_module_interface()` - AST-based interface extraction
- `_validate_module_interface()` - Interface validation

**Critical Features**:
- **Retry Logic**: Automatic error correction with feedback
- **Interface Extraction**: AST parsing for precise interface detection
- **Dependency Management**: Proper module ordering
- **UI Prevention**: Multiple safety checks

**Extension Points**:
- Add new validation rules
- Implement different retry strategies
- Support for additional programming languages

### 4. System Assembly (`system_assembler.py`)

**Purpose**: Creates integration, tests, and demo applications

**Key Components**:
- `assemble_system()` - Main assembly method
- `_create_system_integration()` - Module integration
- `_create_system_tests()` - Test generation
- `_create_demo_application()` - Gradio app creation
- `_create_readme_documentation()` - Documentation generation

**Critical Features**:
- **Integration Generation**: Dynamic module integration
- **Test Creation**: Comprehensive test suites
- **Gradio Apps**: Professional UI generation
- **Documentation**: Auto-generated README files

**Extension Points**:
- Add new test patterns
- Support for different UI frameworks (carefully!)
- Implement additional integration patterns

### 5. Flow Orchestration (`flow.py`)

**Purpose**: Orchestrates the entire process

**Key Functions**:
- `run()`: Main function to execute the flow.
- `get_requirements()`: Handles requirements input (file or interactive).

**Usage**:
- Run as a module: `python -m engineering_team.main_flow`
- Or via the CLI script (see README for details).

**Extension Points**:
- Add new CLI arguments or input modes.
- Customize summary or output formatting.

### 6. Main Flow Entry Point (`main_flow.py`)
**Purpose**: Main entry point for running the agent from the command line. Handles argument parsing, requirements input (file or interactive), and starts the engineering flow.

**Key Functions**:
- `run()`: Main function to execute the flow.
- `get_requirements()`: Handles requirements input (file or interactive).

**Usage**:
- Run as a module: `python -m engineering_team.main_flow`
- Or via the CLI script (see README for details).

**Extension Points**:
- Add new CLI arguments or input modes.
- Customize summary or output formatting.

### 7. Crew Agent Configuration (`crew.py`)
**Purpose**: Defines and configures CrewAI agent roles and their instantiation. Loads agent definitions from `config/agents.yaml` and provides agent objects for use in the flow.

**Key Functions**:
- Agent creation and role assignment.
- Loading agent configuration from YAML.

**Extension Points**:
- Add new agent roles or modify agent behaviors.
- Update `agents.yaml` for new roles or capabilities.

### 8. Data Models (`models.py`)

### SystemArchitecture
- **Purpose**: Represents the complete system design
- **Key Fields**: `system_name`, `description`, `modules`, `assembly_instructions`

### ModuleSpec
- **Purpose**: Specification for individual modules
- **Key Fields**: `name`, `class_name`, `purpose`, `dependencies`, `interfaces`, `priority`

### ModuleCreationState
- **Purpose**: Tracks module creation progress
- **Key Methods**: `get_next_module()`, `mark_module_completed()`, `is_system_complete()`

### 9. Package Marker (`__init__.py`)
**Purpose**: Marks the `engineering_team` directory as a Python package. No additional logic by default.

## Agent Configuration (`config/agents.yaml`)

### Agent Roles

1. **Engineering Lead**
   - **Responsibility**: Architecture design and technical specifications
   - **Key Constraint**: Never design UI modules

2. **Backend Engineer**  
   - **Responsibility**: Module implementation with exact interface compliance
   - **Key Constraint**: Never create UI modules

3. **Frontend Engineer**
   - **Responsibility**: Gradio application creation
   - **Key Constraint**: Only call verified module methods

4. **Test Engineer**
   - **Responsibility**: Comprehensive test suite generation
   - **Focus**: Unit tests, integration tests, edge cases

5. **Module Integrator**
   - **Responsibility**: System integration and orchestration
   - **Key Constraint**: Never integrate UI modules

## Development Environment Setup

### UV Development (Recommended)
```bash
git clone https://github.com/your-org/engineering-team-ai-agent.git
cd engineering-team-ai-agent
uv sync --dev
uv run pre-commit install
uv run engineering_team --interactive
```

### Docker Development
```bash
git clone https://github.com/your-org/engineering-team-ai-agent.git
cd engineering-team-ai-agent
cp .env.example .env
# Add your API keys to .env
docker compose --profile dev up -d
docker compose exec engineering-agent-dev bash
# In container:
python -m engineering_team.main_flow --interactive
```
- Or run production container interactively:
```bash
docker compose run --rm engineering-agent python -m engineering_team.main_flow --interactive
```

### Traditional Python Development
```bash
git clone https://github.com/your-org/engineering-team-ai-agent.git
cd engineering-team-ai-agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
engineering_team --interactive
```

## Testing & Quality Assurance

### Running Tests
```bash
# UV
yuv run pytest -v --cov=src/engineering_team
# Docker
docker compose exec engineering-agent-dev pytest -v --cov
# Traditional
pytest -v --cov=src/engineering_team
```

### Code Quality Checks
```bash
uv run black src/
uv run isort src/
uv run mypy src/
uv run flake8 src/
# All checks
uv run black src/ && uv run isort src/ && uv run mypy src/ && uv run flake8 src/
```

### Pre-commit Hooks
```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Development Guidelines

### Code Quality Standards

1. **Type Hints**: All functions must have complete type annotations
2. **Error Handling**: Comprehensive try-catch blocks with meaningful messages
3. **Documentation**: Docstrings for all public methods and classes
4. **Validation**: Input validation for all external inputs
5. **Logging**: Use structured logging instead of print statements

### Testing Strategy

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test module interactions
3. **End-to-End Tests**: Test complete flow execution
4. **Validation Tests**: Test constraint enforcement (UI prevention)
5. **Docker Tests**: Verify containerized functionality

### Security Considerations

1. **Environment Variables**: Never hardcode API keys
2. **Input Validation**: Sanitize all user inputs
3. **Code Generation**: Validate generated code before execution
4. **File Operations**: Use safe file handling practices
5. **Container Security**: Use non-root users in Docker with proper home directory permissions

## Extension and Customization

### Adding New Agents

1. **Update `agents.yaml`**: Add agent configuration
2. **Extend `crew.py`**: Add agent method
3. **Implement Tasks**: Create appropriate task generation logic
4. **Test Integration**: Ensure proper agent interaction

### Adding New Module Types

1. **Extend `ModuleSpec`**: Add new module properties
2. **Update Creation Logic**: Handle new module types
3. **Implement Validation**: Add appropriate validation rules
4. **Test Generation**: Ensure proper test coverage

### Adding New Validation Rules

1. **Architecture Level**: Update `ArchitecturePlanner`
2. **Module Level**: Update `ModuleCreator`
3. **Integration Level**: Update `SystemAssembler`
4. **Configuration**: Update validation in `config.py`

## Performance Optimization

### Current Optimizations

1. **Dependency-Based Ordering**: Modules created in proper dependency order
2. **Interface Caching**: Module interfaces cached after extraction
3. **Retry Logic**: Efficient error correction with targeted feedback
4. **Path Management**: Centralized path handling for efficiency

### Future Optimization Opportunities

1. **Parallel Module Creation**: Create independent modules in parallel
2. **Template Caching**: Cache common code patterns
3. **Incremental Generation**: Update only changed modules
4. **Smart Retry**: More intelligent retry strategies

## Debugging and Troubleshooting

### Common Debug Points

1. **Architecture Parsing**: Check JSON extraction in `ArchitecturePlanner`
2. **Module Validation**: Verify interface extraction in `ModuleCreator`
3. **Integration Issues**: Check dependency resolution in `SystemAssembler`
4. **UI Module Detection**: Verify UI prevention logic

### Debugging Tools

1. **Flow Results**: Check `output/flow_results.json` for detailed execution data
2. **Module Interfaces**: Inspect extracted interfaces for validation issues
3. **Agent Outputs**: Review individual agent outputs for quality
4. **Validation Logs**: Check validation error messages

### Error Recovery

1. **Retry Logic**: Automatic retry with error feedback
2. **Graceful Degradation**: Continue execution with partial failures
3. **Detailed Logging**: Comprehensive error reporting
4. **Manual Intervention**: Clear error messages for manual fixes

## Testing the System

### Running Unit Tests

```bash
# Run all tests
pytest src/

# Run specific test file
pytest src/test_architecture_planner.py

# Run with coverage
pytest --cov=src/
```

### Integration Testing

```bash
# Test complete flow with sample requirements
engineering_team --interactive
```

### Performance Testing

```bash
# Test with complex requirements
time engineering_team
```

## Code Examples

### Adding a New Validation Rule

```python
# In architecture_planner.py
def _validate_and_clean_architecture(self, architecture: SystemArchitecture) -> SystemArchitecture:
    # Existing UI validation...
    
    # New validation rule
    large_modules = [m for m in architecture.modules if len(m.interfaces) > 10]
    if large_modules:
        print(f"⚠️  Large modules detected: {[m.name for m in large_modules]}")
        # Handle large modules...
    
    return architecture
```

### Adding a New Agent

```python
# In crew.py
@agent
def data_engineer(self) -> Agent:
    return Agent(
        config=self.agents_config['data_engineer'],
        verbose=True
    )
```

### Extending Configuration

```python
# In config.py
class Config:
    def __init__(self, output_dir: Optional[str] = None, 
                 req_file: Optional[str] = None,
                 max_retries: int = 3):  # New option
        self.max_retries = max_retries
        # Existing initialization...
```

## CI/CD and Deployment

### GitHub Actions Workflow
Create `.github/workflows/ci.yml`:
```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    - name: Install UV
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
    - name: Set up Python
      run: uv python install ${{ matrix.python-version }}
    - name: Install dependencies
      run: uv sync --dev
    - name: Run tests
      run: uv run pytest --cov
    - name: Run linting
      run: |
        uv run black --check src/
        uv run flake8 src/
        uv run mypy src/

  docker-build:
    runs-on: ubuntu-latest
    needs: test
    steps:
    - uses: actions/checkout@v4
    - name: Build Docker image
      run: docker build -t engineering-ai-agent .
    - name: Test Docker image
      run: |
        docker run --rm engineering-ai-agent python -c "import engineering_team"
```

### Container Registry & Production Deployment
```bash
# Build and tag for registry
docker build -t your-registry/engineering-ai-agent:latest .
docker build -t your-registry/engineering-ai-agent:v2.0.0 .
# Push to registry
docker push your-registry/engineering-ai-agent:latest
docker push your-registry/engineering-ai-agent:v2.0.0
# Deploy to production
docker run -d \
  --name engineering-ai-agent \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v /host/output:/app/output \
  your-registry/engineering-ai-agent:latest
```

### Production Deployment with Docker Compose
```