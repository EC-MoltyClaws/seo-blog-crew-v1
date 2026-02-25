from dotenv import load_dotenv

from flow import BlogFlow

load_dotenv()


def main():
    BlogFlow().kickoff()


if __name__ == "__main__":
    main()
