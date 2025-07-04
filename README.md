# Engineering Team AI Agent

> 🤖 **Generate complete software systems from natural language requirements**

A powerful multi-agent system built with CrewAI that automatically creates production-ready applications including modular code, tests, documentation, and Gradio-based UIs.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Docker](https://img.shields.io/badge/docker-supported-blue)

## ✨ What It Does

Transform this:
```
Create a Task Management System for small teams with user authentication, 
project creation, and real-time notifications.
```

Into this:
- 📦 **Modular Python Code** with clean architecture
- 🧪 **Comprehensive Tests** with high coverage  
- 🖥️ **Professional Gradio UI** ready to deploy
- 📚 **Complete Documentation** and setup guides
- ⚙️ **Environment Configuration** with security best practices

## 🚀 Quick Start

### 1. Clone and Configure
```bash
git clone https://github.com/your-org/engineering-team-ai-agent.git
cd engineering-team-ai-agent
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

### 2. Run the Agent (Choose One)

#### Docker (Recommended)
```bash
# Run with default req.txt file
docker-compose up

# Or run interactively to input requirements
docker compose run --rm engineering-agent python -m engineering_team.main_flow --interactive
```
- *Interactive mode lets you enter requirements line by line (type 'END' to finish).*
- *To use a different requirements file, replace req.txt before running.*

#### UV (Modern Python)
```bash
uv sync
uv run engineering_team
```

#### Traditional Python
```bash
pip install -e .
engineering_team
```

## 🎯 Key Features

- **🏗️ Architecture Planning**: Designs modular systems automatically
- **🔧 Code Generation**: Creates production-ready Python modules
- **🔄 Self-Correction**: Built-in retry logic with error feedback
- **🖥️ Gradio Integration**: Professional UIs for all generated apps
- **🧪 Testing**: Comprehensive test suites with validation
- **📖 Documentation**: Auto-generated README and API docs
- **🔐 Security**: Environment variable management and validation

## 📋 Usage

1. **Edit `req.txt`** with your project requirements, or use interactive mode.
2. **Run the agent** (see Quick Start above).
3. **Check your generated project** in the `output/` directory.

## ⚙️ Configuration

### Environment Variables
Required variables for the `.env` file:
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
# Optional integrations
SERPER_API_KEY=your_serper_api_key
SENDGRID_API_KEY=your_sendgrid_key
```

### Custom Configuration
```python
from engineering_team.config import Config
config = Config(
    output_dir="my_projects",
    req_file="my_requirements.txt"
)
```

## 📁 Generated Project Structure

Every generated project includes:
```
output/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── app.py                   # Gradio web application
├── test_system.py           # Comprehensive tests
├── system_integration.py    # Module orchestration
├── module1.py               # Business logic modules
├── module2.py               # (Generated based on requirements)
└── ...
```

## 🛠️ Advanced Usage

- **Multiple Deployment Methods**: See Quick Start for pip, UV, and Docker options.
- **Custom Requirements**: Edit `req.txt` or use `--interactive` mode.
- **Development Mode**: Use `docker compose --profile dev up` for live code changes.

## 🧪 Testing Generated Applications

```bash
cd output/
python test_system.py         # Run the test suite
python app.py                 # Launch the web application (http://localhost:7860)
pip install -r requirements.txt
python -m pytest              # If pytest tests are generated
```

## 🔧 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
```bash
cp .env.example .env
echo "OPENAI_API_KEY=your_key_here" >> .env
```

**"Module creation failed"**
- Check your internet connection
- Verify API key is valid
- The system automatically retries with error feedback

**"Permission denied (Docker)"**
```bash
sudo usermod -aG docker $USER
# Then logout and login again
# If you see permission errors with appuser, the Dockerfile has been fixed
# Rebuild the image: docker compose build --no-cache
```

### Performance Tips
- **Large projects**: Complex requirements may take 10-15 minutes
- **Docker**: Use development profile for faster iteration
- **UV**: Fastest dependency management for Python projects

## 📖 Documentation
- **[Developer Guide](DEVELOPER.md)** - Technical details for contributors
- **[API Reference](DEVELOPER.md#api-reference)** - Core classes and methods
- **[Architecture Overview](DEVELOPER.md#architecture-overview)** - System design

## 🤝 Contributing
We welcome contributions! See our [Developer Guide](DEVELOPER.md) for:
- Development setup with Docker/UV
- Code quality standards
- Testing requirements
- Pull request process

Quick development setup:
```bash
git clone https://github.com/your-org/engineering-team-ai-agent.git
cd engineering-team-ai-agent
uv sync --dev
pre-commit install
```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits
- Built with [CrewAI](https://www.crewai.com/) multi-agent framework
- UI powered by [Gradio](https://gradio.app/)
- Dependency management with [UV](https://github.com/astral-sh/uv)

---
**⭐ Star this repo if it helped you build amazing applications!**# Trigger workflow
