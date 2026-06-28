from agent.router import detect_route
from agent.tools import calculator, task_manager
from agent.agent import chat_with_gemini

# Tool Registry
TOOLS = {
    "calculator": calculator,
    "task_manager": task_manager,
    "chat": chat_with_gemini
}


def run_agent(user_input):

    # Get execution plan from router
    plan = detect_route(user_input)

    # Debug (Optional)
    print("\n========== EXECUTION PLAN ==========")
    print(plan)
    print("====================================\n")

    # Extract steps
    steps = plan["steps"]

    # Store results from every executed tool
    results = []

    # Execute every step
    for step in steps:

        tool = step["tool"]
        tool_input = step["input"]

        # Call the correct function dynamically
        result = TOOLS[tool](tool_input)

        # Save output
        results.append(result)

    return results