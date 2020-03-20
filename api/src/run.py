"""
Top-level module, creates the app instance in development as well as production 
scenarios.
"""

from src import create_app

app = create_app()
