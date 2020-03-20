"""
Top-level module, creates the app instance in development as well as production 
scenarios.
"""

from src import create_app

app = create_app()


@app.shell_context_processor
def shell_context():
    """Creates the context for the `flask shell` command

    This function passes a dictionary back to the shell_context_processor 
    decorator function. The dict contains objects from the app and provides 
    them to the interpreter. This is useful for quick iteration testing 
    of new code without starting a new development instance
    """
    create_tables()
    return {'db': db, 'User': User}
