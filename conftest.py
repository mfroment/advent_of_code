import sys

def pytest_ignore_collect(path):
    if str(path).endswith(".txt"):
        return True
