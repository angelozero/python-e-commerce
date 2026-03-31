import sys
import os
from agent_loop_langchain_tool_calling import run_agent

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def main():
    answer = run_agent("What is the price of a laptop applying a gold discount?")
    print(f"\nRESPONSE: {answer}")
    print("")


if __name__ == "__main__":
    main()