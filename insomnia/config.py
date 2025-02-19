import os

TOKEN = os.getenv("INSOMNIA_TOKEN")
USER_AGENT = os.getenv("INSOMNIA_USER_AGENT")
BROWSER = os.getenv("INSOMNIA_BROWSER")
OS = os.getenv("INSOMNIA_OS")

if None in [TOKEN, USER_AGENT, BROWSER, OS]:
    raise ValueError("Please set the required config environment variables")
