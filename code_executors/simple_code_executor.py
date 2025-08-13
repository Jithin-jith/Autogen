# Importing necessary modules
import os  # Provides functions to interact with the operating system (e.g., environment variables, file paths)
from autogen import AssistantAgent, UserProxyAgent  # Classes from AutoGen library to create AI agents
from dotenv import load_dotenv  # Utility to load environment variables from a `.env` file

# Load environment variables from `.env` file into the system's environment
load_dotenv()

# Define the model name to be used for the LLM
model = "gpt-4o-mini"

# Configuration dictionary for the LLM (Large Language Model)
llm_config = {
    "model": model,  # The LLM model to use
    "api_key": os.environ.get("OPENAI_API_KEY"),  # Fetch API key from environment variables
}

# Create an AI assistant agent with the given configuration
assistant = AssistantAgent(
    name="Assistant",  # Name of the assistant agent
    llm_config=llm_config,  # LLM configuration (model, API key, etc.)
)

# Create a user proxy agent that simulates human interaction with the assistant
user_proxy = UserProxyAgent(
    name="user",  # Name of the user proxy agent
    human_input_mode="ALWAYS",  # Always ask for user input when needed
    code_execution_config={  # Configuration for executing code
        "work_dir": "codes",  # Directory where generated/executed code will be saved
        "use_docker": False,  # Set to True to execute code inside a Docker container
    },
)

# Start the chat: The user proxy sends an initial message to the assistant
user_proxy.initiate_chat(
    recipient=assistant,  # The agent to send the message to (the assistant)
    message="Plot a chart of META and TESLA stock price change."  # Initial request from the user
)
