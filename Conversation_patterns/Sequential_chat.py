# Import required modules
import os                                      # For interacting with environment variables
from autogen import ConversableAgent           # ConversableAgent: an AutoGen agent capable of chatting with other agents
from typing import Annotated                   # Useful for type annotations (not directly used in this code)
from dotenv import load_dotenv                 # To load environment variables from a .env file

# Load environment variables from the .env file into the system environment
load_dotenv()

# Define the LLM model to be used
model = "gpt-4o-mini"

# LLM configuration dictionary
# temperature → Controls randomness in LLM output (0 = deterministic, 1 = highly creative)
# api_key → Loaded securely from environment variables
llm_config = {
    "model": model,
    "temperature": 0.0,
    "api_key": os.environ["OPENAI_API_KEY"],  # Access the API key from environment variables
}

# ------------------------
# Define Agents
# ------------------------

# Agent 1: Initial Agent
# Always returns the exact text provided to it.
initial_agent = ConversableAgent(
    name="Initial_Agent",
    system_message="You return me the text I give you.",
    llm_config=llm_config,
    human_input_mode="NEVER",   # Disables human intervention during the conversation
)

# Agent 2: Uppercase Agent
# Converts the given text to uppercase.
uppercase_agent = ConversableAgent(
    name="Uppercase_Agent",
    system_message="You convert the text I give you to uppercase.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Agent 3: Word Count Agent
# Counts the number of words in the given text.
word_count_agent = ConversableAgent(
    name="WordCount_Agent",
    system_message="You count the number of words in the text I give you.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Agent 4: Reverse Text Agent
# Reverses the given text.
reverse_text_agent = ConversableAgent(
    name="ReverseText_Agent",
    system_message="You reverse the sentence I sent you. For eg: if i semt you 'Hai you' then you need to sent me 'uoy iah'",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Agent 5: Summarize Agent
# Summarizes the given text.
summarize_agent = ConversableAgent(
    name="Summarize_Agent",
    system_message="You summarize the text I give you.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# ------------------------
# Initiating Multiple Chats
# ------------------------

# Start a series of two-agent conversations using initiate_chats
# Each dictionary in the list defines:
# - recipient: The agent to chat with
# - message: The text sent to the agent
# - max_turns: Maximum turns for the conversation
# - summary_method: How to summarize the conversation ("last_msg" = use last message as summary)
chat_results = initial_agent.initiate_chats(
    [
        {
            "recipient": uppercase_agent,
            "message": "This is a sample text document.",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": word_count_agent,
            "message": "count the number of words in the text",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": reverse_text_agent,
            "message": "Reverse the sentence I sent you. For eg: if i semt you 'Hai you' then you need to sent me 'uoy iah'",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": summarize_agent,
            "message": "summarize the text",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
    ]
)

# ------------------------
# Display Results
# ------------------------

# Print the summary of each chat in sequence
print("First Chat Summary: ", chat_results[0].summary)   # Output from Uppercase Agent
print('\n')
print("Second Chat Summary: ", chat_results[1].summary)  # Output from Word Count Agent
print('\n')
print("Third Chat Summary: ", chat_results[2].summary)   # Output from Reverse Text Agent
print('\n')
print("Fourth Chat Summary: ", chat_results[3].summary)  # Output from Summarize Agent
