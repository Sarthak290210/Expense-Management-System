import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"Project root: {project_root}")
print("*"*20)
sys.path.insert(0, project_root)
print(f"sys.path: {sys.path}")