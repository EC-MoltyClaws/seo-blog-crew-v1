import os
from dotenv import load_dotenv
from crew import build_crew

load_dotenv()


def main():
    result = build_crew().kickoff()

    print("\n=== CREW RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
