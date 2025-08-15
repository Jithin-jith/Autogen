# Import necessary libraries
import os  # For accessing environment variables and OS-related functionality
from autogen import ConversableAgent  # Core class from AutoGen to create conversational AI agents
from typing import Annotated  # For adding metadata/annotations to function parameters
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load environment variables from the .env file into the OS environment
load_dotenv()

# Define the LLM model to be used
model = "gpt-4o-mini"
llm_config = {
    "model": model,                  # The selected LLM model
    "temperature": 0.0,              # Controls randomness (0.0 means deterministic output)
    "api_key": os.environ["OPENAI_API_KEY"],  # Load API key from environment variable
}

# ---------------------------
# TOOL FUNCTIONS (Calculator)
# ---------------------------

# Function to add two integers with descriptive parameter annotations
def add_numbers(
    a: Annotated[int, "First number"],  # Annotated type hint for better documentation
    b: Annotated[int, "Second number"]  # Annotated type hint for better documentation
) -> str:
    # Return a formatted string showing the sum
    return f"The sum of {a} and {b} is {a + b}."

# Function to multiply two integers with descriptive parameter annotations
def multiply_numbers(
    a: Annotated[int, "First number"],
    b: Annotated[int, "Second number"]
) -> str:
    # Return a formatted string showing the product
    return f"The product of {a} and {b} is {a * b}."

# ----------------------------------
# ASSISTANT AGENT CONFIGURATION
# ----------------------------------

# Create an assistant agent that suggests which tool (function) to call
assistant = ConversableAgent(
    name="CalculatorAssistant",  # Agent's identity name
    system_message="You are a helpful AI calculator. Return 'TERMINATE' when the task is done.",  # Instruction for behavior
    llm_config=llm_config,  # LLM settings defined earlier
)

# Create a user proxy agent that acts as the "human" side of the conversation
user_proxy = ConversableAgent(
    name="User",  # Agent's identity name
    # Function to determine when the conversation should stop
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",  # The user will not provide manual input; automation only
)

# ----------------------------------
# TOOL REGISTRATION
# ----------------------------------

# Register tool signatures with the assistant so it knows what functions it can call
assistant.register_for_llm(name="add_numbers", description="Add two numbers")(add_numbers)
assistant.register_for_llm(name="multiply_numbers", description="Multiply two numbers")(multiply_numbers)

# Register the actual tool execution with the user proxy (the "executor" side)
user_proxy.register_for_execution(name="add_numbers")(add_numbers)
user_proxy.register_for_execution(name="multiply_numbers")(multiply_numbers)

# ----------------------------------
# CHAT INITIATION
# ----------------------------------

# Start the conversation by asking the assistant a math question
user_proxy.initiate_chat(
    assistant,
    message="What is the sum of 7 and 5?"  # Initial prompt from the user
)
