# Import necessary libraries
import os  # For accessing environment variables
from autogen import ConversableAgent  # For creating conversational AI agents
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from .env into system environment
load_dotenv()

# Define the LLM (Large Language Model) to use
model = "gpt-4o-mini"

# Configuration for the LLM
# Includes the model name and the API key stored in the environment variables
llm_config = {
    "model": model,
    "api_key": os.environ.get("OPENAI_API_KEY"),  # Retrieve API key securely from .env
}

# Create the first agent: "agent_with_animal"
# This agent has the animal "elephant" in mind and will respond with hints if guessed incorrectly
agent_with_animal = ConversableAgent(
    "agent_with_animal",  # Unique name for the agent
    system_message=(
        "You are thinking of an animal. You have the animal 'elephant' in your mind, "
        "and I will try to guess it. If I guess incorrectly, give me a hint. "
    ),
    llm_config=llm_config,  # Pass the model configuration
    is_termination_msg=lambda msg: "elephant" in msg["content"],  # Stop conversation if 'elephant' is guessed
    human_input_mode="NEVER",  # Do not ask for manual/human input for this agent
)

# Create the second agent: "human_proxy"
# This acts as a bridge for actual human input (not an AI)
human_proxy = ConversableAgent(
    "human_proxy",  # Unique name for the human proxy
    llm_config=False,  # No AI model — this agent will only take human input
    human_input_mode="ALWAYS",  # Always ask the user for input
)

# Start the conversation
# human_proxy sends the first guess "Parrot" to agent_with_animal
# The game will continue until the termination condition (guessing "elephant") is met
result = human_proxy.initiate_chat(
    agent_with_animal,
    message="Parrot",
)
