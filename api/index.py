import sys
import os

# Add the project directory to sys.path so Python can find the 'app' package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "clinic-ai-receptionist"))

from app.main import app  # noqa: E402
