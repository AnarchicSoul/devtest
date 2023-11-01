# def qui execute le script script.py
import subprocess
import os

def test_answer():
    subprocess.run(['python3', 'script.py'])
    assert os.path.isdir('output')
