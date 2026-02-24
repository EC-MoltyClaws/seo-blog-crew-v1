import sys
from dotenv import load_dotenv
from crew import build_crew

load_dotenv()


def main():
    skip_research = "--skip-research" in sys.argv
    result = build_crew(skip_research=skip_research).kickoff()

    print("\n=== CREW RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
