import os
from dotenv import load_dotenv
from crew import build_crew

load_dotenv()


def main():
    topic = "best pet-friendly hotels in Southeast Asia"  # replace or make dynamic

    crew = build_crew(topic)
    result = crew.kickoff()

    print("\n=== CREW RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
