import os
import pathlib

def create_project_structure():
    """
    Generates the folder and file structure for the Multi-Agent System PoC
    with empty files.
    """
    # Define the directory structure in a list of paths
    dirs = [
        "app/api",
        "app/agents",
        "app/core",
        "app/graph",
        "app/llm",
        "app/tools",
        "tests"
    ]

    # Define the empty files to be created
    files = [
        "app/__init__.py",
        "app/main.py",
        "app/api/__init__.py",
        "app/api/endpoints.py",
        "app/agents/__init__.py",
        "app/agents/supervisor.py",
        "app/agents/web_agent.py",
        "app/core/__init__.py",
        "app/core/config.py",
        "app/graph/__init__.py",
        "app/graph/state.py",
        "app/graph/workflow.py",
        "app/llm/__init__.py",
        "app/llm/groq_client.py",
        "app/tools/__init__.py",
        "app/tools/handoff.py",
        "tests/__init__.py",
        "tests/test_agents.py",
        ".env",
        "requirements.txt",
        "README.md"
    ]

    # Create directories
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")

    # Create empty files
    for file_path in files:
        pathlib.Path(file_path).touch()
        print(f"Created file: {file_path}")

if __name__ == "__main__":
    create_project_structure()
    print("\nProject structure with empty files created successfully!")
    print("Next steps:")
    print("1. Add your API keys to the .env file.")
    print("2. Add your dependencies to the requirements.txt file.")
    print("3. Start developing the agent logic in the 'app' directory.")