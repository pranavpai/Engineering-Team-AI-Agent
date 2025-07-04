#!/bin/bash
# Engineering Team AI Agent - Quick Setup Script

set -e

echo "🤖 Engineering Team AI Agent - Quick Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if running on supported OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_status "Detected OS: $OS"

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python version: $PYTHON_VERSION"
    
    # Check if Python version is >= 3.10
    if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
        print_error "Python 3.10 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed or not in PATH"
    exit 1
fi

# Function to setup with UV
setup_with_uv() {
    print_header "Setting up with UV (Modern Python tooling)"
    
    # Check if UV is installed
    if ! command -v uv &> /dev/null; then
        print_status "Installing UV..."
        if [[ "$OS" == "Windows" ]]; then
            powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
        else
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
        fi
    else
        print_status "UV is already installed"
    fi
    
    # Install dependencies
    print_status "Installing dependencies with UV..."
    uv sync --dev
    
    # Setup pre-commit
    print_status "Setting up pre-commit hooks..."
    uv run pre-commit install
    
    print_status "✅ Setup complete! Run: uv run engineering_team"
}

# Function to setup with Docker
setup_with_docker() {
    print_header "Setting up with Docker"
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first:"
        echo "  - macOS: https://docs.docker.com/docker-for-mac/install/"
        echo "  - Linux: https://docs.docker.com/engine/install/"
        echo "  - Windows: https://docs.docker.com/docker-for-windows/install/"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    print_status "Building Docker image..."
    docker-compose build
    
    print_status "✅ Setup complete! Run: docker-compose up"
}

# Function to setup with pip
setup_with_pip() {
    print_header "Setting up with pip (Traditional Python)"
    
    # Create virtual environment
    print_status "Creating virtual environment..."
    python3 -m venv .venv
    
    # Activate virtual environment
    if [[ "$OS" == "Windows" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install package in development mode
    print_status "Installing package in development mode..."
    pip install -e ".[dev]"
    
    # Setup pre-commit
    print_status "Setting up pre-commit hooks..."
    pre-commit install
    
    print_status "✅ Setup complete! Activate venv and run: engineering_team"
    if [[ "$OS" == "Windows" ]]; then
        echo "  Activate: .venv\\Scripts\\activate"
    else
        echo "  Activate: source .venv/bin/activate"
    fi
}

# Setup environment file
setup_environment() {
    print_header "Setting up environment"
    
    if [[ ! -f .env ]]; then
        print_status "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please edit .env and add your OPENAI_API_KEY"
        echo "  Required: OPENAI_API_KEY=your_api_key_here"
    else
        print_status ".env file already exists"
    fi
    
    # Check if API key is set
    if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
        print_warning "Don't forget to set your OPENAI_API_KEY in .env file!"
    fi
}

# Main setup function
main() {
    echo ""
    print_header "Choose your setup method:"
    echo "1) UV (Recommended - fastest and most modern)"
    echo "2) Docker (Good for isolation and deployment)"
    echo "3) Pip (Traditional Python virtual environment)"
    echo "4) Environment setup only"
    echo ""
    
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            setup_environment
            setup_with_uv
            ;;
        2)
            setup_environment
            setup_with_docker
            ;;
        3)
            setup_environment
            setup_with_pip
            ;;
        4)
            setup_environment
            ;;
        *)
            print_error "Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
    
    echo ""
    print_header "🎉 Setup Complete!"
    echo ""
    print_status "Next steps:"
    echo "  1. Edit .env file and add your OPENAI_API_KEY"
    echo "  2. Create req.txt with your project requirements"
    echo "  3. Run the agent with your chosen method"
    echo ""
    print_status "For help, see README.md or run: engineering_team --help"
}

# Run main function
main "$@"