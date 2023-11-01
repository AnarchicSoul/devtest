# def qui execute le script script.py
import subprocess
import os

subprocess.run(['python3', 'script.py'])

def test_answer():
    assert os.path.isdir('output')
