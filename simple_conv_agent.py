# Import the os module to interact with environment variables and file paths
import os

# Import the ConversableAgent class from the autogen package to create an AI-powered conversational agent
from autogen import ConversableAgent

# Import the load_dotenv function from the dotenv package to load environment variables from a .env file
from dotenv import load_dotenv

# Load environment variables from the .env file into the system's environment
load_dotenv()

# Define the OpenAI model to be used for generating responses
model = "gpt-4o-mini"

# Create a configuration dictionary for the language model
llm_config = {
    "model": model,  # Specify which model to use
    "api_key": os.environ.get("OPENAI_API_KEY"),  # Retrieve the API key from environment variables
    "temperature":0.8 #set temperature close to 1 so that the model is creative
}

# Initialize the ConversableAgent with its configuration
agent = ConversableAgent(
    name="chatbot",               # Name of the agent
    llm_config=llm_config,        # Language model configuration
    code_execution_config=False,  # Disable code execution capability
    human_input_mode="NEVER",     # The agent will not request manual human input
)

# Generate a reply from the agent based on a given user message
response = agent.generate_reply(
    messages=[{"role": "user", "content": "Tell me a funny joke."}]
)

# Print the generated response to the console
print(response)
