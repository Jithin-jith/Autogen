# Import required Python libraries
import os                       # For interacting with the operating system (e.g., accessing environment variables)
from autogen import ConversableAgent   # ConversableAgent is a type of AI agent in AutoGen that can have conversations with other agents
import pprint                   # Pretty-printing of Python objects for better readability in console output
from autogen import Cache
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load environment variables from the .env file into the system environment
load_dotenv()

# Define the model to use for LLM-based conversations
model = "gpt-4o-mini"

# LLM (Large Language Model) configuration dictionary
# temperature → controls randomness (0 = deterministic, 1 = more creative)
# api_key → pulled securely from environment variables
llm_config = {
    "model": model,
    "temperature": 0.9,
    "api_key": os.environ["OPENAI_API_KEY"],  # Read the API key from environment variables
}

# Create the first agent: Traveler_Agent
# This agent plays the role of a person planning a vacation
traveler_agent = ConversableAgent(
    name="Traveler_Agent",
    system_message="You are a traveler planning a vacation.",
    llm_config=llm_config,
)

# Create the second agent: Guide_Agent
# This agent plays the role of an experienced travel guide
guide_agent = ConversableAgent(
    name="Guide_Agent",
    system_message="You are a travel guide with extensive knowledge about popular destinations.",
    llm_config=llm_config,
)

# Initiate a conversation between Traveler_Agent and Guide_Agent
# message → first message from traveler to guide
# summary_method → determines how the chat summary is generated
# max_turns → limits the number of conversation turns

with Cache.disk(cache_seed=42, cache_path_root=".cache") as cache: #Add cache so that agent can use it during multiple runs
    chat_result = traveler_agent.initiate_chat(
        guide_agent,
        message="What are the must-see attractions in Tokyo?",
        summary_method="reflection_with_llm",
        max_turns=2,
        cache=cache
    )

# Print chat summary to the console
print(" \n ***Chat Summary***: \n")
# 'summary' → an auto-generated summary of the conversation
print(chat_result.summary)

# Display the default input prompt used internally by the LLM
print(" \nDefault Input Prompt: \n")
print(ConversableAgent.DEFAULT_SUMMARY_PROMPT)

# Display the entire chat history between the agents
print(" \nChat history: \n")
pprint.pprint(chat_result.chat_history)

# Display the cost of the conversation (tokens used × cost per token)
print(" \n**Chat Cost**: \n")
pprint.pprint(chat_result.cost)
