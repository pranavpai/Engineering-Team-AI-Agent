# Developer Documentation

## Engineering Team AI Agent - Developer Guide

This document provides technical details for developers working on and contributing to the Engineering Team AI Agent codebase.

> **Note**: For user installation and usage, see [README.md](README.md).

## Architecture Overview

### System Design Philosophy

The Engineering Team AI Agent follows a **modular, specialized architecture** where each component has a single, well-defined responsibility:

1. **Orchestration Layer** (`flow.py`) - Coordinates the entire process using CrewAI Flow
2. **Planning Layer** (`architecture_planner.py`) - System design and validation
3. **Creation Layer** (`module_creator.py`) - Code generation with retry logic
4. **Assembly Layer** (`system_assembler.py`) - Integration, testing, and demos
5. **Configuration Layer** (`config.py`) - Centralized settings management
6. **Agent Management** (`crew.py`) - CrewAI agent definitions and configuration

### Data Flow

```
Requirements (req.txt) 
    ↓
EngineeringFlow (flow.py) - CrewAI Flow orchestration
    ↓
ArchitecturePlanner → SystemArchitecture
    ↓
ModuleCreator → Dict[modules] with interfaces
    ↓
SystemAssembler → Complete System (integration, tests, demo, docs)
    ↓
Output Directory (generated project)
```

## Module Details

### 1. Configuration Management (`config.py`)

**Purpose**: Centralized configuration and path management

**Key Features**:
- Dynamic path configuration with Path objects
- Environment validation for API keys
- Configurable output directories with auto-creation
- Requirements file management

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
- `plan_architecture()` - Main planning method with CrewAI Task
- `_validate_and_clean_architecture()` - UI module prevention
- `create_module_state()` - Dependency tracking initialization
- `_parse_architecture_result()` - Robust JSON parsing with regex fallback

**Critical Features**:
- **UI Enforcement**: Automatically removes UI modules (ui.py, interface.py, etc.)
- **JSON Parsing**: Robust parsing of AI agent outputs with regex fallback
- **Validation**: Ensures architectural consistency and Gradio-only constraint
- **CrewAI Integration**: Uses Engineering Lead agent for architecture design

**Extension Points**:
- Add new architectural patterns
- Implement additional validation rules
- Support for different module types

### 3. Module Creation (`module_creator.py`)

**Purpose**: Creates individual modules with validation and retry logic

**Key Components**:
- `create_modules()` - Main creation orchestrator with dependency ordering
- `_create_single_module_with_retry()` - Retry logic implementation (max 2 retries)
- `_extract_module_interface()` - AST-based interface extraction
- `_validate_module_interface()` - Interface validation against specifications
- `_get_specific_interface()` - Dependency interface resolution

**Critical Features**:
- **Retry Logic**: Automatic error correction with feedback (2 retry attempts)
- **Interface Extraction**: AST parsing for precise interface detection
- **Dependency Management**: Proper module ordering based on dependencies
- **UI Prevention**: Multiple safety checks at creation time
- **CrewAI Integration**: Uses Engineering Lead and Backend Engineer agents

**Extension Points**:
- Add new validation rules
- Implement different retry strategies
- Support for additional programming languages

### 4. System Assembly (`system_assembler.py`)

**Purpose**: Creates integration, tests, and demo applications

**Key Components**:
- `assemble_system()` - Main assembly method
- `_create_system_integration_with_retry()` - Integration with retry logic
- `_create_system_tests()` - Test generation using Test Engineer agent
- `_create_demo_application()` - Gradio app creation using Frontend Engineer agent
- `_create_readme_documentation()` - Documentation generation
- `_validate_integration_dependencies()` - Post-creation validation

**Critical Features**:
- **Integration Generation**: Dynamic module integration with dependency handling
- **Test Creation**: Comprehensive test suites using Test Engineer agent
- **Gradio Apps**: Professional UI generation using Frontend Engineer agent
- **Documentation**: Auto-generated README files with setup instructions
- **Validation**: Post-creation dependency validation

**Extension Points**:
- Add new test patterns
- Support for different UI frameworks (carefully!)
- Implement additional integration patterns

### 5. Flow Orchestration (`flow.py`)

**Purpose**: Orchestrates the entire process using CrewAI Flow

**Key Functions**:
- `architecture_planning()`: PHASE 1 - Engineering Lead creates system architecture
- `create_modules()`: PHASE 2 - Create all modules based on architecture
- `assemble_system()`: PHASE 3 - Create system integration, tests, and demo

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
- `display_completion_summary()`: User-friendly completion summary
- `analyze_imports_and_create_requirements()`: Auto-generate requirements.txt
- `cleanup_ui_files()`: Remove any UI files that shouldn't exist
- `save_detailed_results()`: Save flow results for debugging

**Usage**:
- Run as a module: `python -m engineering_team.main_flow`
- Interactive mode: `python -m engineering_team.main_flow --interactive`
- Or via the CLI script (see README for details).

**Extension Points**:
- Add new CLI arguments or input modes.
- Customize summary or output formatting.

### 7. Crew Agent Configuration (`crew.py`)

**Purpose**: Defines and configures CrewAI agent roles and their instantiation. Loads agent definitions from `config/agents.yaml` and provides agent objects for use in the flow.

**Key Functions**:
- Agent creation and role assignment.
- Loading agent configuration from YAML.
- Crew creation with sequential process.

**Agents**:
- `engineering_lead()`: Architecture design and technical specifications
- `backend_engineer()`: Module implementation with exact interface compliance
- `frontend_engineer()`: Gradio application creation
- `test_engineer()`: Comprehensive test suite generation
- `module_integrator()`: System integration and orchestration

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

**Purpose**: Marks the `engineering_team` directory as a Python package. Exports main classes and models.

**Exports**:
- `EngineeringFlow`
- `SystemArchitecture`
- `ModuleSpec`
- `ModuleCreationState`
- `EngineeringTeam`

## Agent Configuration (`config/agents.yaml`)

### Agent Roles

1. **Engineering Lead**
   - **Responsibility**: Architecture design and technical specifications
   - **Key Constraint**: Never design UI modules
   - **LLM**: gpt-4o-mini

2. **Backend Engineer**  
   - **Responsibility**: Module implementation with exact interface compliance
   - **Key Constraint**: Never create UI modules
   - **LLM**: gpt-4o-mini

3. **Frontend Engineer**
   - **Responsibility**: Gradio application creation
   - **Key Constraint**: Only call verified module methods
   - **LLM**: gpt-4o-mini

4. **Test Engineer**
   - **Responsibility**: Comprehensive test suite generation
   - **Focus**: Unit tests, integration tests, edge cases
   - **LLM**: gpt-4o-mini

5. **Module Integrator**
   - **Responsibility**: System integration and orchestration
   - **Key Constraint**: Never integrate UI modules
   - **LLM**: gpt-4o-mini

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
uv run pytest -v --cov=src/engineering_team
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
3. **Retry Logic**: Efficient error correction with targeted feedback (max 2 retries)
4. **Path Management**: Centralized path handling for efficiency
5. **CrewAI Flow**: Sequential processing for predictable execution

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

1. **Retry Logic**: Automatic retry with error feedback (2 attempts max)
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
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  engineering-ai-agent:
    image: your-registry/engineering-ai-agent:latest
    container_name: engineering-ai-agent-prod
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./output:/app/output
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - engineering-network

networks:
  engineering-network:
    driver: bridge
```

## Monitoring and Observability

### Logging Configuration

The system uses structured logging for better observability:

```python
import logging
from engineering_team.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.log_path),
        logging.StreamHandler()
    ]
)
```

### Metrics and Monitoring

Key metrics to monitor:

1. **Module Creation Success Rate**: Track successful vs failed module generations
2. **Agent Response Times**: Monitor AI agent performance
3. **Retry Frequency**: Track how often retry logic is triggered
4. **Memory Usage**: Monitor resource consumption during generation
5. **Output Quality**: Track validation success rates

### Health Checks

```python
# health_check.py
def check_system_health():
    """Perform comprehensive system health check"""
    checks = {
        'api_keys': check_api_keys(),
        'disk_space': check_disk_space(),
        'memory_usage': check_memory_usage(),
        'agent_connectivity': check_agent_connectivity()
    }
    return all(checks.values()), checks
```

## Contributing Guidelines

### Pull Request Process

1. **Fork the Repository**: Create your own fork
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Follow Code Standards**: Ensure all quality checks pass
4. **Add Tests**: Include tests for new functionality
5. **Update Documentation**: Update relevant documentation
6. **Submit PR**: Create pull request with detailed description

### Commit Message Convention

Use conventional commit messages:

```
feat: add new validation rule for large modules
fix: resolve JSON parsing issue in architecture planner
docs: update deployment documentation
test: add integration tests for module creation
refactor: improve error handling in system assembler
```

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact considered
- [ ] Error handling is comprehensive

## Release Process

### Version Management

The project follows semantic versioning (SemVer):

- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

### Release Steps

1. **Update Version**: Update version in `pyproject.toml`
2. **Update Changelog**: Add entries to `CHANGELOG.md`
3. **Create Release Branch**: `git checkout -b release/v1.2.0`
4. **Run Full Test Suite**: Ensure all tests pass
5. **Build and Test Docker Image**: Verify container functionality
6. **Merge to Main**: Merge release branch to main
7. **Tag Release**: `git tag -a v1.2.0 -m "Release v1.2.0"`
8. **Push Tags**: `git push origin --tags`
9. **Create GitHub Release**: Add release notes and assets

### Automated Release Pipeline

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker image
        run: |
          docker build -t your-registry/engineering-ai-agent:${{ github.ref_name }} .
          docker push your-registry/engineering-ai-agent:${{ github.ref_name }}
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. API Key Issues
**Problem**: "Invalid API key" errors
**Solution**: 
- Verify API keys are set correctly in environment
- Check API key permissions and quotas
- Ensure keys are not expired

#### 2. Module Creation Failures
**Problem**: Modules fail to create or validate
**Solution**:
- Check agent output quality in logs
- Verify interface extraction logic
- Review retry logic configuration

#### 3. Docker Container Issues
**Problem**: Container fails to start or run
**Solution**:
- Check Docker daemon status
- Verify image build process
- Review container logs: `docker logs engineering-ai-agent`

#### 4. Memory Issues
**Problem**: Out of memory errors during generation
**Solution**:
- Increase container memory limits
- Optimize module creation process
- Implement memory-efficient processing

#### 5. Network Connectivity
**Problem**: Cannot connect to AI services
**Solution**:
- Check internet connectivity
- Verify firewall settings
- Test API endpoints directly

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set debug environment variable
export DEBUG=true

# Run with debug logging
python -m engineering_team.main_flow --debug
```

### Performance Profiling

```python
import cProfile
import pstats

def profile_execution():
    """Profile the execution for performance analysis"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run your code here
    run_engineering_flow()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
```

## Future Roadmap

### Planned Features

1. **Multi-Language Support**: Extend beyond Python
2. **Template System**: Pre-built architectural templates
3. **Plugin Architecture**: Third-party plugin support
4. **Real-time Collaboration**: Multi-user development support
5. **Advanced Validation**: AI-powered code quality assessment

### Performance Improvements

1. **Parallel Processing**: Concurrent module creation
2. **Caching Layer**: Intelligent result caching
3. **Incremental Updates**: Update only changed components
4. **Resource Optimization**: Better memory and CPU usage

### Integration Enhancements

1. **IDE Integration**: VS Code and PyCharm plugins
2. **CI/CD Integration**: Automated deployment pipelines
3. **Cloud Platform Support**: AWS, GCP, Azure integration
4. **Monitoring Integration**: Prometheus, Grafana support

## Support and Community

### Getting Help

1. **Documentation**: Check this guide and README.md
2. **Issues**: Report bugs on GitHub Issues
3. **Discussions**: Use GitHub Discussions for questions
4. **Discord**: Join our community Discord server

### Contributing to Documentation

1. **Update This Guide**: Keep developer documentation current
2. **Add Examples**: Include practical code examples
3. **Improve Clarity**: Make complex concepts accessible
4. **Add Diagrams**: Visual explanations where helpful

### Community Guidelines

1. **Be Respectful**: Treat all community members with respect
2. **Help Others**: Share knowledge and assist newcomers
3. **Follow Standards**: Adhere to project coding standards
4. **Give Credit**: Acknowledge contributions appropriately

---

## Appendix

### A. Configuration Reference

Complete configuration options and their meanings:

```python
class Config:
    def __init__(self, 
                 output_dir: Optional[str] = None,
                 req_file: Optional[str] = None):
        # Configuration implementation
```

### B. API Reference

Key classes and methods:

```python
# Architecture Planning
class ArchitecturePlanner:
    def plan_architecture(self, requirements: str) -> SystemArchitecture: ...
    def _validate_and_clean_architecture(self, architecture: SystemArchitecture) -> SystemArchitecture: ...

# Module Creation
class ModuleCreator:
    def create_modules(self, architecture: SystemArchitecture, module_state: ModuleCreationState) -> Dict[str, Any]: ...
    def _create_single_module_with_retry(self, module_spec: ModuleSpec, architecture: SystemArchitecture) -> Dict[str, Any]: ...

# System Assembly
class SystemAssembler:
    def assemble_system(self, architecture: SystemArchitecture, modules: Dict[str, Any]) -> Dict[str, Any]: ...

# Flow Orchestration
class EngineeringFlow(Flow):
    @start()
    def architecture_planning(self) -> SystemArchitecture: ...
    
    @listen(architecture_planning)
    def create_modules(self, architecture: SystemArchitecture) -> Dict[str, Any]: ...
    
    @listen(create_modules)
    def assemble_system(self, modules_data: Dict[str, Any]) -> Dict[str, Any]: ...
```

### C. Environment Variables

Required and optional environment variables:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional
DEBUG=true
LOG_LEVEL=INFO
MAX_RETRIES=3
TIMEOUT=300
OUTPUT_DIR=/custom/output/path
```

### D. File Structure Reference

```
engineering-team-ai-agent/
├── src/engineering_team/
│   ├── __init__.py
│   ├── architecture_planner.py
│   ├── config.py
│   ├── crew.py
│   ├── flow.py
│   ├── main_flow.py
│   ├── models.py
│   ├── module_creator.py
│   ├── system_assembler.py
│   └── config/
│       └── agents.yaml
├── scripts/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── CHANGELOG.md
├── LICENSE
├── README.md
├── DEVELOPER.md
└── req.txt
```

*Note: For best practices, consider adding `docs/` for documentation and `tests/` for test code in the future as the project grows.*