import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# print(os.path.join(parent_dir, "src"))
sys.path.insert(0, os.path.join(parent_dir, "src"))
