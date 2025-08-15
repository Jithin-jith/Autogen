# -----------------------------
# IMPORT REQUIRED LIBRARIES
# -----------------------------
import os  # For accessing environment variables from the operating system
from autogen import ConversableAgent  # AutoGen's class for creating conversational AI agents
from typing import Annotated  # To add metadata/description to type hints for better LLM context
from dotenv import load_dotenv  # To load environment variables from a .env file

# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------
# This loads variables from the .env file into the OS environment so we can use them in code
load_dotenv()

# -----------------------------
# CONFIGURE LLM SETTINGS
# -----------------------------
model = "gpt-4o-mini"  # The AI model to be used
llm_config = {
    "model": model,  # Which model to use
    "temperature": 0.0,  # 0.0 means deterministic, consistent responses
    "api_key": os.environ["OPENAI_API_KEY"],  # Fetch API key from environment variables
}

# -----------------------------
# TOOL FUNCTIONS
# -----------------------------

# Function to get the status of a given flight
# Annotated[str, "Flight number"] means the parameter must be a string,
# and the annotation helps AutoGen describe this parameter to the LLM
def get_flight_status(flight_number: Annotated[str, "Flight number"]) -> str:
    # Dummy data simulating flight status lookups
    dummy_data = {"AA123": "On time", "DL456": "Delayed", "UA789": "Cancelled"}
    # Return the status or 'unknown' if not found
    return f"The current status of flight {flight_number} is {dummy_data.get(flight_number, 'unknown')}."

# Function to get top hotel information for a location
def get_hotel_info(location: Annotated[str, "Location"]) -> str:
    dummy_data = {
        "New York": "Top hotel in New York: The Plaza - 5 stars",
        "Los Angeles": "Top hotel in Los Angeles: The Beverly Hills Hotel - 5 stars",
        "Chicago": "Top hotel in Chicago: The Langham - 5 stars",
    }
    # Return hotel info or fallback if no data found
    return dummy_data.get(location, f"No hotels found in {location}.")

# Function to get travel advice for a location
def get_travel_advice(location: Annotated[str, "Location"]) -> str:
    dummy_data = {
        "New York": "Travel advice for New York: Visit Central Park and Times Square.",
        "Los Angeles": "Travel advice for Los Angeles: Check out Hollywood and Santa Monica Pier.",
        "Chicago": "Travel advice for Chicago: Don't miss the Art Institute and Millennium Park.",
    }
    # Return travel advice or fallback if no advice found
    return dummy_data.get(location, f"No travel advice available for {location}.")

# -----------------------------
# CREATE ASSISTANT AGENT
# -----------------------------
# The assistant suggests which tool (function) should be used
assistant = ConversableAgent(
    name="TravelAssistant",  # Agent name
    system_message="You are a helpful AI travel assistant. Return 'TERMINATE' when the task is done.",  # Agent instructions
    llm_config=llm_config,  # LLM settings defined above
)

# -----------------------------
# CREATE USER PROXY AGENT
# -----------------------------
# Acts as the "executor" that actually runs the functions when the assistant requests them
user_proxy = ConversableAgent(
    name="User",  # Agent name
    is_termination_msg=lambda msg: msg.get("content") is not None
    and "TERMINATE" in msg["content"],  # Condition to stop the conversation
    human_input_mode="NEVER",  # No manual user input — fully automated execution
)

# -----------------------------
# REGISTER TOOLS FOR LLM USE
# -----------------------------
# These tell the assistant which functions are available to call and describe them
assistant.register_for_llm(
    name="get_flight_status",
    description="Get the current status of a flight based on the flight number",
)(get_flight_status)

assistant.register_for_llm(
    name="get_hotel_info",
    description="Get information about hotels in a specific location",
)(get_hotel_info)

assistant.register_for_llm(
    name="get_travel_advice",
    description="Get travel advice for a specific location"
)(get_travel_advice)

# -----------------------------
# REGISTER TOOL EXECUTION
# -----------------------------
# These map the tool names to their actual Python functions so they can be run during chat
user_proxy.register_for_execution(name="get_flight_status")(get_flight_status)
user_proxy.register_for_execution(name="get_hotel_info")(get_hotel_info)
user_proxy.register_for_execution(name="get_travel_advice")(get_travel_advice)

# -----------------------------
# INITIATE CHAT
# -----------------------------
# This starts the conversation between the user proxy and the assistant
# The assistant will decide which tools to call based on the user's request
user_proxy.initiate_chat(
    assistant,
    message="I need help with my travel plans. Can you help me? I am traveling to New York. I need hotel information. Also give me the status of my flight AA123.",
)
