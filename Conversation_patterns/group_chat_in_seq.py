import os
from autogen import ConversableAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv

# Load environment variables from the .env file (contains API keys, etc.)
load_dotenv()

# Define the model and LLM configuration
model = "gpt-4o-mini"
llm_config = {
    "model": model,                  # Model to use for conversation
    "temperature": 0.4,               # Lower temperature = more deterministic responses
    "api_key": os.environ["OPENAI_API_KEY"],  # Retrieve API key from environment
}

# ===================================================
# Group Chat in a Sequential Chat
# This example shows how a Group Chat can be inserted into a sequence of two-agent chats.
# In this flow, the Group Chat Manager behaves like a single agent in the sequence.
# ===================================================

# --------------------------
# Define travel planning agents
# --------------------------

# Agent responsible for suggesting flights
flight_agent = ConversableAgent(
    name="Flight_Agent",
    system_message="You provide the best flight options for the given destination and dates.",
    llm_config=llm_config,
    description="Provides flight options.",
)

# Agent responsible for suggesting hotels
hotel_agent = ConversableAgent(
    name="Hotel_Agent",
    system_message="You suggest the best hotels for the given destination and dates.",
    llm_config=llm_config,
    description="Suggests hotel options.",
)

# Agent responsible for suggesting activities and attractions
activity_agent = ConversableAgent(
    name="Activity_Agent",
    system_message="You recommend activities and attractions to visit at the destination.",
    llm_config=llm_config,
    description="Recommends activities and attractions.",
)

# Agent responsible for suggesting restaurants
restaurant_agent = ConversableAgent(
    name="Restaurant_Agent",
    system_message="You suggest the best restaurants to dine at in the destination.",
    llm_config=llm_config,
    description="Recommends restaurants.",
)

# Agent responsible for providing weather forecasts
weather_agent = ConversableAgent(
    name="Weather_Agent",
    system_message="You provide the weather forecast for the travel dates.",
    llm_config=llm_config,
    description="Provides weather forecast.",
)

# --------------------------
# Create a Group Chat with introduction messages
# --------------------------
group_chat_with_introductions = GroupChat(
    agents=[flight_agent, hotel_agent, activity_agent, restaurant_agent, weather_agent],
    messages=[],                # No prior messages at start
    max_round=6,                 # Maximum conversation rounds allowed
    send_introductions=True,     # Send each agent’s introduction message at the start
)

# --------------------------
# Create a Group Chat Manager
# --------------------------
group_chat_manager_with_intros = GroupChatManager(
    groupchat=group_chat_with_introductions,
    llm_config=llm_config,
)

# --------------------------
# Define a regular summarizing agent for sequential chat
# --------------------------
travel_planner_agent = ConversableAgent(
    name="Travel_Planner_Agent",
    system_message="You summarize the travel plan provided by the group chat.",
    llm_config=llm_config,
    description="Summarizes the travel plan.",
)

# --------------------------
# Start a sequence of chats
# The group chat manager acts like a single agent in the sequence
# --------------------------
chat_result = travel_planner_agent.initiate_chats(
    [
        {
            # First chat: Travel planner asks group chat to prepare a plan
            "recipient": group_chat_manager_with_intros,
            "message": "I'm planning a trip to Paris for the first week of September. Can you help me plan? I will be leaving from Miami and will stay for a week.",
            "summary_method": "reflection_with_llm",  # Summarize context for next step
        },
        {
            # Second chat: Refine the travel plan with extra details
            "recipient": group_chat_manager_with_intros,
            "message": "Please refine the plan with additional details.",
            "summary_method": "reflection_with_llm",
        },
    ]
)

# --------------------------
# Print the cost of each chat result
# --------------------------
for result in chat_result:
    print(result.cost)
