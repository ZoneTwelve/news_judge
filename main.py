#!/usr/bin/env python
"""
Main entry point for News Inferencer.

This module loads environment variables from .env file, making them available
to other modules in the project. Import this module to ensure environment
variables are loaded before accessing them.
"""

from dotenv import load_dotenv
import os

# Configurations
load_dotenv()
