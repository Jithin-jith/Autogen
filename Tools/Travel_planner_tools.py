# -----------------------------
# IMPORT REQUIRED LIBRARIES
# -----------------------------
import os  # For accessing environment variables like API keys
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent  
# ConversableAgent: general-purpose agent for conversation
# AssistantAgent: specialized for LLM-powered tool suggestion
# UserProxyAgent: specialized for acting as a human proxy to execute tools

from typing import Annotated  # For adding descriptive metadata to function parameters
from dotenv import load_dotenv  # For loading environment variables from a .env file

# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------
load_dotenv()  # Reads .env file and makes variables accessible via os.environ

# -----------------------------
# CONFIGURE LLM SETTINGS
# -----------------------------
model = "gpt-4o-mini"  # The AI model being used
llm_config = {
    "model": model,  # Model selection
    "temperature": 0.9,  # Controls randomness; higher value = more creative
    "api_key": os.environ["OPENAI_API_KEY"],  # Loads API key from environment
}

# -----------------------------
# TOOL FUNCTIONS
# -----------------------------

# Function to calculate travel time given distance and speed
# Annotated helps provide LLM-friendly descriptions for each parameter
def calculate_travel_time(
    distance: Annotated[int, "Distance in kilometers"],
    speed: Annotated[int, "Speed in km/h"],
) -> str:
    travel_time = distance / speed  # Time = Distance / Speed
    return f"At a speed of {speed} km/h, it will take approximately {travel_time:.2f} hours to travel {distance} kilometers."

# Function to convert currency from USD to EUR
def convert_currency(
    amount: Annotated[float, "Amount in USD"],
    rate: Annotated[float, "Exchange rate to EUR"],
) -> str:
    converted_amount = amount * rate
    return f"${amount} USD is approximately €{converted_amount:.2f} EUR."

# Function to suggest activities for a location
def suggest_activity(location: Annotated[str, "Location"]) -> str:
    activities = {
        "Paris": "Visit the Eiffel Tower and the Louvre Museum.",
        "New York": "See Times Square and Central Park.",
        "Tokyo": "Explore the Shibuya Crossing and the Senso-ji Temple.",
    }
    # Return activity if location exists, else return fallback
    return activities.get(location, f"No specific activities found for {location}.")

# -----------------------------
# CREATE ASSISTANT AGENT
# -----------------------------
assistant = AssistantAgent(
    name="TravelPlannerAssistant",  # Agent name
    system_message="You are a helpful AI travel planner. Return 'TERMINATE' when the task is done.",  # System instructions
    llm_config=llm_config,  # LLM configuration
)

# -----------------------------
# CREATE USER PROXY AGENT
# -----------------------------
user_proxy = ConversableAgent(
    name="User",  # Agent name
    # Function that decides when to end the conversation (looks for 'TERMINATE' in content)
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="TERMINATE",  # Waits for termination message, not manual user input
)

# -----------------------------
# REGISTER TOOLS FOR LLM USE
# -----------------------------
# These tell the assistant what functions it can call, along with descriptions
assistant.register_for_llm(
    name="calculate_travel_time",
    description="Calculate travel time based on distance and speed",
)(calculate_travel_time)

assistant.register_for_llm(
    name="convert_currency",
    description="Convert USD to EUR based on exchange rate",
)(convert_currency)

assistant.register_for_llm(
    name="suggest_activity",
    description="Suggest activities for a specific location",
)(suggest_activity)

# -----------------------------
# REGISTER TOOL EXECUTION
# -----------------------------
# These connect tool names to their actual Python functions for execution
user_proxy.register_for_execution(name="calculate_travel_time")(calculate_travel_time)
user_proxy.register_for_execution(name="convert_currency")(convert_currency)
user_proxy.register_for_execution(name="suggest_activity")(suggest_activity)

# -----------------------------
# START THE CONVERSATION
# -----------------------------
# Begin a conversation where the assistant can call registered tools
user_proxy.initiate_chat(
    assistant,
    message="I am planning a trip to Paris. What should I do there?",
)
