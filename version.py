import subprocess
_version = subprocess.check_output(["git", "describe", "--tags"]).rstrip()

__version__ = _version.decode("utf-8")
