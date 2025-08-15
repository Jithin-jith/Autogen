# Importing necessary libraries
import os  # For accessing environment variables
from autogen import ConversableAgent # For creating AI agents that can converse
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from the .env file into the system environment
load_dotenv()

# Define the model to be used for the agents
model = "gpt-4o-mini"

# Configuration for the LLM (Large Language Model)
# Includes the model name and API key from environment variables
llm_config = {
    "model": model,
    "api_key": os.environ.get("OPENAI_API_KEY"),  # Retrieve API key from environment
}

# Create the first agent ("agent_with_animal")
# This agent has an animal ("elephant") in mind and will give hints if guessed incorrectly
agent_with_animal = ConversableAgent(
    "agent_with_animal",  # Unique name for the agent
    system_message=(
        "You are thinking of an animal. You have the animal 'elephant' in your mind, "
        "and I will try to guess it. If I guess incorrectly, give me a hint. "
    ),
    llm_config=llm_config,  # Pass the model configuration
    is_termination_msg=lambda msg: "elephant" in msg["content"],  # End chat if 'elephant' is guessed
    human_input_mode="NEVER",  # No manual/human input during the chat
)

# Create the second agent ("agent_guess_animal")
# This agent will try to guess the animal in the other agent's mind using given hints
agent_guess_animal = ConversableAgent(
    "agent_guess_animal",  # Unique name for the agent
    system_message=(
        "I have an animal in my mind, and you will try to guess it. "
        "If I give you a hint, use it to narrow down your guesses. "
    ),
    llm_config=llm_config,  # Pass the model configuration
    human_input_mode="NEVER",  # No manual/human input during the chat
)

# Start the conversation
# 'agent_with_animal' starts by challenging 'agent_guess_animal' to guess the animal
agent_with_animal.initiate_chat(
    agent_guess_animal,
    message="I am thinking of an animal. Guess which one!",
)

