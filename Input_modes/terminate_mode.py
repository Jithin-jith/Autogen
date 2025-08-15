# Import required libraries
import os  # For accessing environment variables

from dotenv import load_dotenv  # For loading API keys and settings from a .env file
from autogen import ConversableAgent  # For creating conversational AI agents

# Load environment variables from .env into the system's environment variables
load_dotenv()

# Define the LLM (Large Language Model) to use
model = "gpt-4o-mini"

# Configuration for the LLM
llm_config = {
    "model": model,  # Model name
    "temperature": 0.9,  # Controls randomness (higher = more creative responses)
    "api_key": os.environ["OPENAI_API_KEY"],  # Get API key from environment variables
}

# Create the first agent: "agent_with_animal"
# This agent has the animal "elephant" in mind and will give hints until guessed
agent_with_animal = ConversableAgent(
    "agent_with_animal",  # Unique identifier for this agent
    system_message=(
        "You are thinking of an animal. You have the animal 'elephant' in your mind, "
        "and I will try to guess it. If I guess incorrectly, give me a hint. "
    ),
    llm_config=llm_config,  # Pass model configuration
    max_consecutive_auto_reply=1,  # Max consecutive AI replies before asking for human input
    is_termination_msg=lambda msg: "elephant" in msg["content"],  # Stop if 'elephant' is guessed
    human_input_mode="TERMINATE",  # Continue asking for human input until termination condition is met
)

# Create the second agent: "agent_guess_animal"
# This agent will try to guess the animal in the other agent's mind
agent_guess_animal = ConversableAgent(
    "agent_guess_animal",  # Unique identifier for this agent
    system_message=(
        "I have an animal in my mind, and you will try to guess it. "
        "If I give you a hint, use it to narrow down your guesses. "
    ),
    llm_config=llm_config,  # Pass model configuration
    human_input_mode="NEVER",  # This agent never takes human input — fully automated
)

# Start a new conversation between both agents
# Note: The comment in the code reminds you to clear previous chat history/cache before starting
result = agent_with_animal.initiate_chat(
    agent_guess_animal,
    message="I am thinking of an animal. Guess which one!",
)
