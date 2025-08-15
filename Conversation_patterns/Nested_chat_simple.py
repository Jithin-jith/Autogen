# Import required Python modules
import os  # For accessing environment variables like the API key
from autogen import AssistantAgent, UserProxyAgent  # Import agent classes from AutoGen

# ------------------------------------
# Define LLM (Large Language Model) configuration
# ------------------------------------
llm_config = {
    "model": "gpt-4o-mini",  # The OpenAI model to be used
    "temperature": 0.4,  # Lower temperature = more focused and deterministic output
    "api_key": os.environ["OPENAI_API_KEY"],  # Fetch API key from environment variables
}

# ------------------------------------
# Create the "Writer" agent
# ------------------------------------
writer = AssistantAgent(
    name="Writer",  # Agent's name for identification
    llm_config=llm_config,  # Link to the LLM configuration defined above
    system_message="""
    You are a professional writer, known for your insightful and engaging product reviews.
    You transform technical details into compelling narratives.
    You should improve the quality of the content based on the feedback from the user.
    """,  # This is the agent's role and behavior instructions
)

# ------------------------------------
# Create the "User Proxy" agent
# ------------------------------------
user_proxy = UserProxyAgent(
    name="User",  # Name of the proxy agent
    human_input_mode="NEVER",  # No human intervention; fully automated
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    # Lambda function to decide when the conversation should end
    code_execution_config={
        "last_n_messages": 1,  # Only execute code from the most recent message
        "work_dir": "my_code",  # Directory where code execution will take place
        "use_docker": False,    # Whether to use Docker for isolation (disabled here)
    },
)

# ------------------------------------
# Create the "Critic" agent
# ------------------------------------
critic = AssistantAgent(
    name="Critic",  # Name of the critic agent
    llm_config=llm_config,  # Use the same LLM configuration
    system_message="""
    You are a critic, known for your thoroughness and commitment to standards.
    Your task is to scrutinize content for any harmful elements or regulatory violations, ensuring
    all materials align with required guidelines.
    """,  # Behavior instructions for the critic
)

# ------------------------------------
# Function to create a reflection message
# This message will be sent to the critic to analyze the last content produced
# ------------------------------------
def reflection_message(recipient, messages, sender, config):
    print("Reflecting...")  # Debug print to indicate function execution
    # Get the last message from the sender and prepare a critique request
    return f"Reflect and provide critique on the following review. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"

# ------------------------------------
# Register nested chat
# This means when the 'writer' produces content, the 'critic' will automatically review it
# ------------------------------------
user_proxy.register_nested_chats(
    [
        {
            "recipient": critic,                # Who will receive the nested chat
            "message": reflection_message,      # The function to create the critic's message
            "summary_method": "last_msg",       # Only summarize the last message for context
            "max_turns": 1,                      # Maximum of 1 turn for the nested conversation
        }
    ],
    trigger=writer,  # Trigger the nested chat whenever 'writer' sends a message
)

# ------------------------------------
# Define the main task
# ------------------------------------
task = """Write a detailed and engaging product review for the new Meta VR headset."""

# ------------------------------------
# Start the conversation
# The 'user_proxy' sends the task to the 'writer', and the critic reviews the output
# ------------------------------------
res = user_proxy.initiate_chat(
    recipient=writer,  # The writer will create the review
    message=task,      # The initial task prompt
    max_turns=2,       # Maximum 2 exchanges between user_proxy and writer
    summary_method="last_msg"  # Only summarize the last message for final output
)
