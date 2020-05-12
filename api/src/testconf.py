"""
Configuration file for the development target
"""

ERROR_404_HELP = False
OPENAPI_SPEC = 'openapi/spec.yml'

# SQLalchemy Settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False