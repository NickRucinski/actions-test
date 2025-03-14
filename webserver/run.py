import os
import subprocess
import sys

VENV_DIR = ".venv"
DOCS_DIR = "docs"
FLASK_APP = "app.app"
FLASK_HOST = "0.0.0.0"
FLASK_PORT = "5000"

def activate_virtualenv():
    """Activate the virtual environment."""
    if not os.path.exists(VENV_DIR):
        print("Virtual environment not found. Please create one with 'python -m venv venv'.")
        sys.exit(1)

    activate_script = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "activate")
    if os.name != "nt":
        subprocess.run(["source", activate_script], shell=True, executable="/bin/bash")
    else:
        subprocess.run(activate_script, shell=True)

def install_dependencies():
    """Install dependencies from requirements.txt."""
    if os.path.exists("requirements.txt"):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def build_sphinx_docs():
    """Build Sphinx documentation."""
    if os.path.exists(DOCS_DIR):
        print("Building Sphinx documentation...")
        subprocess.run(["make", "html"], cwd=DOCS_DIR, check=True)
    else:
        print("Sphinx documentation directory not found.")

def run_flask():
    """Run the Flask application."""
    env = os.environ.copy()
    env["FLASK_APP"] = FLASK_APP
    env["FLASK_ENV"] = "development"  # Change to 'production' if needed

    subprocess.run([sys.executable, "-m", "flask", "run", "--host", FLASK_HOST, "--port", FLASK_PORT], env=env)

if __name__ == "__main__":
    activate_virtualenv()
    install_dependencies()
    build_sphinx_docs()
    run_flask()
