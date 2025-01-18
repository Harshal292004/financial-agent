import datetime
from rich.console import Console
import os


class RichLogger:
    """
    Class for logging during development

    Logs with time and color:
        - error
        - warning
        - info
        - debug
        - success
    """
    def __init__(self, log_file="logs/general_logs.log", log_to_file=True, print_to_console=True):
        self.console = Console()
        self.log_file = log_file
        self.print_to_console = print_to_console
        self.log_to_file = log_to_file

        if self.log_to_file:
            try:
                # Ensure the directory for the log file exists
                os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            except Exception as e:
                self.console.print(f"Failed to create log directory: {e}", style="red")
                self.log_to_file = False  # Disable file logging if directory creation fails

    def log_with_time(self, message: str, style: str = "cyan"):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{now}] {message}"

        # Print to console if enabled
        if self.print_to_console:
            self.console.print(formatted_message, style=style)

        # Log to file if enabled
        if self.log_to_file:
            try:
                with open(self.log_file, "a") as file:
                    file.write(formatted_message + "\n")
            except Exception as e:
                self.console.print(f"Failed to write to log file: {e}", style="red")

    def error(self, message: str):
        self.log_with_time(message=message, style="red")

    def warn(self, message: str):
        self.log_with_time(message=message, style="yellow")

    def info(self, message: str):
        self.log_with_time(message=message, style="blue")

    def debug(self, message: str):
        self.log_with_time(message=message, style="magenta")

    def success(self, message: str):
        self.log_with_time(message=message, style="green")
