# Code Executors in AutoGen

In **AutoGen**, a **code executor** is the part of the system that allows an AI agent to actually *run* code it has generated or been given — instead of just returning code as text.  

Think of it as the “hands” of the agent — the LLM does the thinking, and the executor does the doing.  

---

## Why Code Executors Exist
LLMs are great at producing code, but they can’t *run* it by themselves.  
In many scenarios, you want the AI to:
- Test the code it wrote
- Get real outputs from it
- Debug and fix errors automatically

That’s where code executors come in — they take the generated code, run it in a controlled environment, and return the results to the agent.

---

## Types of Code Executors in AutoGen

### 1. Local Execution (`use_docker=False`)
- Runs code directly on your machine.
- Fast and easy to set up.
- **Risk:** If the generated code is harmful (e.g., deletes files), it could affect your local environment.
- Good for **trusted** or experimental scenarios.

**Example:**
```
python
code_execution_config={
    "work_dir": "codes",
    "use_docker": False}
```

### 2. Docker-based Execution (use_docker=True)
- Runs code inside an isolated Docker container.
- Safer — even if the AI writes malicious code, it can’t affect your host machine.
- Supports persistent or disposable environments.
- More secure for running untrusted code.

### 3. Custom Code Executors
- You can plug in your own executor if you have a custom environment.
- Useful if you need special dependencies, GPU access, or integration with cloud notebooks (Colab, SageMaker, etc.).

### How Code Execution Fits in the Workflow
```
UserProxyAgent → AssistantAgent → Generates code → Code Executor runs it → Returns results → AI uses results

```
#### Example:
- UserProxyAgent sends "Plot a chart of META and TESLA stock price change".
- AssistantAgent writes Python code using something like matplotlib or yfinance.
- Code executor runs the Python code (locally or in Docker).
- Output chart is sent back to the user.

### Best Practices
- For security: Use use_docker=True when running AI-generated code from unknown or external sources.
- For reproducibility: Use a clean environment or container snapshot for consistent results.
- For debugging: Store executed code and logs in work_dir.