import os
import sys

# Add the src directory to sys.path
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

pytest_plugins = 'src.utils.fixtures'
