import logging
import json
from pathlib import Path
from rich.console import Console
from rich.theme import Theme
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
from datetime import datetime
import os
from typing import Optional, Dict, Any

class Logger:
    """
    A developer-friendly logger class that provides both console and file logging capabilities.
    Implements the singleton pattern to ensure consistent logging across the application.
    
    Features:
    - Rich console output with color-coded log levels and clickable file paths
    - Bounding boxes around log messages for better visibility
    - JSON file logging for structured data
    - Caller information in logs
    - Configurable log levels
    - Thread-safe operations
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logging()
            self._initialized = True
    
    def _setup_logging(self):
        """Initialize the logger with console and file handlers"""
        # Create logs directory
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup console with custom theme
        self.console = Console(theme=Theme({
            "info": "bold green",
            "warning": "bold yellow",
            "error": "bold red",
            "critical": "bold red reverse",
            "debug": "bold blue",
            "path": "blue underline",
            "function": "cyan",
            "line": "yellow",
            "panel.info": "green",
            "panel.warning": "yellow",
            "panel.error": "red",
            "panel.critical": "red reverse",
            "panel.debug": "blue",
            "title": "bold white",
            "message": "white",
            "location": "dim"
        }))
        
        # Create logger instance
        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Add file handler for JSON logging
        self._setup_file_handlers()
    
    def _setup_file_handlers(self):
        """Setup file handlers for different log levels"""
        self.log_files = {
            'INFO': self.log_dir / 'info.json',
            'WARNING': self.log_dir / 'warning.json',
            'ERROR': self.log_dir / 'error.json',
            'CRITICAL': self.log_dir / 'critical.json',
            'DEBUG': self.log_dir / 'debug.json'
        }
        
        # Ensure log files exist
        for log_file in self.log_files.values():
            if not log_file.exists():
                with open(log_file, 'w') as f:
                    json.dump([], f)
    
    def _get_caller_info(self) -> Dict[str, Any]:
        """Get information about the caller"""
        import inspect
        # Go up 3 frames to skip the logger's own methods
        caller_frame = inspect.currentframe().f_back.f_back.f_back
        if caller_frame:
            caller_info = inspect.getframeinfo(caller_frame)
            # Get relative path from workspace root
            workspace_root = os.getcwd()
            file_path = os.path.relpath(caller_info.filename, workspace_root)
            return {
                'file': file_path,
                'line': caller_info.lineno,
                'function': caller_info.function
            }
        return {}
    
    def _format_message(self, message: str, caller_info: Dict[str, Any], **kwargs) -> str:
        """Format the log message with rich formatting"""
        # Format the main message
        formatted_message = f"[message]{message}[/message]"
        
        # Add any extra information
        if kwargs:
            formatted_message += "\n" + "\n".join(f"  [dim]{k}:[/dim] {v}" for k, v in kwargs.items())
        
        # Add location information at the bottom
        file_path = caller_info.get('file', '')
        line_number = caller_info.get('line', '')
        function_name = caller_info.get('function', '')
        
        if file_path and function_name:
            location = f"[location]{function_name} in {file_path}:{line_number}[/location]"
            formatted_message += f"\n\n{location}"
        
        return formatted_message
    
    def _create_panel(self, level: str, message: str, caller_info: Dict[str, Any]) -> Panel:
        """Create a rich panel for the log message"""
        # Define panel styles based on log level
        panel_styles = {
            'INFO': 'panel.info',
            'WARNING': 'panel.warning',
            'ERROR': 'panel.error',
            'CRITICAL': 'panel.critical',
            'DEBUG': 'panel.debug'
        }
        
        # Create the panel with appropriate styling
        return Panel(
            message,
            title=f" {level} ",
            border_style=panel_styles.get(level, ''),
            title_align="left",
            padding=(1, 2),
            expand=False
        )
    
    def _log_to_file(self, level: str, message: str, **kwargs):
        """Log message to appropriate JSON file"""
        log_file = self.log_files[level]
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'extra': kwargs,
            **self._get_caller_info()
        }
        
        # Load existing logs and append new entry
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
            
        logs.append(log_entry)
        
        # Save updated logs
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def _log(self, level: str, message: str, **kwargs):
        """Internal logging method that handles both console and file logging"""
        # Get caller information
        caller_info = self._get_caller_info()
        
        # Format the message with rich markup
        formatted_message = self._format_message(message, caller_info, **kwargs)
        
        # Create and display the panel
        panel = self._create_panel(level, formatted_message, caller_info)
        self.console.print(panel)
        
        # Log to file
        self._log_to_file(level, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log an info message"""
        self._log('INFO', message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log a debug message"""
        self._log('DEBUG', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log a warning message"""
        self._log('WARNING', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log an error message"""
        self._log('ERROR', message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log a critical message"""
        self._log('CRITICAL', message, **kwargs)
    
    def set_level(self, level: str):
        """Set the logging level for all handlers"""
        level = level.upper()
        if hasattr(logging, level):
            self.logger.setLevel(getattr(logging, level))

def get_logger() -> Logger:
    """
    Get the singleton logger instance.
    
    Returns:
        Logger: The singleton logger instance
        
    Example:
        logger = get_logger()
        logger.info("Application started")
        logger.error("Something went wrong", exc_info=True)
    """
    return Logger()