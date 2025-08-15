# Human Input Modes in AutoGen

In **AutoGen**, the `human_input_mode` parameter controls **when and how** an agent should request input from a human during a conversation.  
This setting is crucial for deciding the level of automation in multi-agent workflows.

---

## **Available Modes**

### 1. `ALWAYS`
- **Description:**  
  The agent **always** requests human input before sending its next message.
- **Use Case:**  
  When you want **full human control** over responses — useful in high-stakes scenarios or debugging.
- **Behavior Flow:**
  ```
  Agent → Ask human for input → Send message
  ```
- **Example:**
  ```python
  agent = ConversableAgent(
      "human_agent",
      llm_config=False,  # No AI model
      human_input_mode="ALWAYS"
  )
  ```
- **When to Use:**  
  - Interactive games with a human player
  - Manual decision-making tasks
  - Testing and prompt tuning

---

### 2. `NEVER`
- **Description:**  
  The agent **never** asks for human input and **operates fully autonomously**.
- **Use Case:**  
  Ideal for **fully automated AI-to-AI interactions** where no human intervention is needed.
- **Behavior Flow:**
  ```
  Agent → Auto-generate response → Continue conversation
  ```
- **Example:**
  ```python
  agent = ConversableAgent(
      "auto_agent",
      llm_config=llm_config,
      human_input_mode="NEVER"
  )
  ```
- **When to Use:**  
  - AI simulations
  - Batch processing tasks
  - Continuous autonomous workflows

---

### 3. `TERMINATE`
- **Description:**  
  The agent **keeps asking for human input until a termination condition is met**,  
  after which it stops requesting human input and ends the conversation.
- **Use Case:**  
  Perfect for **goal-oriented conversations** where human guidance is needed until a specific outcome is reached.
- **Behavior Flow:**
  ```
  Agent → Ask human for input → Continue until termination condition → End
  ```
- **Example:**
  ```python
  agent = ConversableAgent(
      "guided_agent",
      llm_config=llm_config,
      human_input_mode="TERMINATE",
      is_termination_msg=lambda msg: "done" in msg["content"]
  )
  ```
- **When to Use:**  
  - Quizzes or guessing games
  - Guided troubleshooting sessions
  - Human-assisted decision-making until a goal is reached

---

## **Quick Comparison Table**

| Mode       | Requests Human Input | Stops Asking Before Termination? | Typical Use Case                  |
|------------|----------------------|-----------------------------------|------------------------------------|
| `ALWAYS`   | Yes, every turn      | No                                | Full manual control                |
| `NEVER`    | No                   | N/A                               | Fully automated workflows          |
| `TERMINATE`| Yes, until condition | Yes, once termination is reached  | Goal-based, human-assisted sessions|

---

## **Final Notes**
- Choosing the right input mode depends on the **level of automation** and **human control** you want.
- Combine input modes with `is_termination_msg` to finely control conversation flow.