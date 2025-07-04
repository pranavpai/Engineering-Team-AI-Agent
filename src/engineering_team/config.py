"""
Configuration management for the Engineering Team AI Agent
"""
import os
from pathlib import Path
from typing import Optional

class Config:
    """Centralized configuration management"""
    
    # Default paths
    DEFAULT_OUTPUT_DIR = "output"
    DEFAULT_REQ_FILE = "req.txt"
    
    def __init__(self, output_dir: Optional[str] = None, req_file: Optional[str] = None):
        self.output_dir = Path(output_dir or self.DEFAULT_OUTPUT_DIR)
        self.req_file = Path(req_file or self.DEFAULT_REQ_FILE)
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
    
    @property
    def output_path(self) -> Path:
        """Get the output directory path"""
        return self.output_dir
    
    @property
    def requirements_file(self) -> Path:
        """Get the requirements file path"""
        return self.req_file
    
    def get_module_path(self, module_name: str) -> Path:
        """Get the full path for a module file"""
        return self.output_dir / module_name
    
    def validate_environment(self) -> list[str]:
        """Validate required environment variables and files"""
        issues = []
        
        # Check for requirements file
        if not self.req_file.exists():
            issues.append(f"Requirements file not found: {self.req_file}")
        
        # Check for essential environment variables (optional but recommended)
        recommended_env_vars = ["OPENAI_API_KEY"]
        for var in recommended_env_vars:
            if not os.getenv(var):
                issues.append(f"Recommended environment variable not set: {var}")
        
        return issues
    
    def __str__(self) -> str:
        return f"Config(output_dir={self.output_dir}, req_file={self.req_file})"

# Global configuration instance
config = Config()