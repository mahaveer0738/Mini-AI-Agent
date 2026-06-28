from agent.orchestrator import run_agent


def main():

    print("====== Mini AI Agent ======")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        results = run_agent(user_input)

        print("\nAgent:")

        for result in results:
            print(f"- {result}")

        print()

if __name__ == "__main__":
    main()