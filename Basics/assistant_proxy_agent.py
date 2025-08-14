# Import the 'os' module to access environment variables and interact with the operating system
import os  

# Import AssistantAgent and UserProxyAgent classes from AutoGen for AI agent interactions
from autogen import AssistantAgent, UserProxyAgent  

# Import 'load_dotenv' to load environment variables from a .env file
from dotenv import load_dotenv  

# Load environment variables from the .env file into the program's environment
load_dotenv()  

# Specify the model name to be used for the LLM (here, a smaller, faster GPT-4 variant)
model = "gpt-4o-mini"  

# Define the LLM configuration, including model and API key from environment variables
llm_config = {
    "model": model,
    "api_key": os.environ.get("OPENAI_API_KEY"),  # Retrieve API key securely from environment
}

# Create an AssistantAgent instance
# - name: Identifier for the assistant agent
# - llm_config: Language model configuration defined above
assistant = AssistantAgent(
    name="Personal_Assistant", 
    llm_config=llm_config
)

# Create a UserProxyAgent instance
# - name: Identifier for the user proxy agent
# - llm_config: Same model configuration
# - code_execution_config: Settings for running AI-generated code
#   - workd_dir: Directory for storing executed code files (note: possible typo, should be 'work_dir')
#   - use_docker: Whether to run code in Docker container (False = run locally)
# - human_input_mode: "NEVER" means it won't pause for human input
user_proxy = UserProxyAgent(
    name="user_proxy",
    llm_config=llm_config,
    code_execution_config={
        "work_dir": "code_execution", 
        "use_docker": False,
    },
    human_input_mode="NEVER",
)

# Start the conversation between the UserProxyAgent and the AssistantAgent
# - The 'user_proxy' sends the initial message to 'assistant'
# - The assistant will respond using the specified LLM
user_proxy.initiate_chat(
    assistant,
    message="What is the capital of France?",
)
