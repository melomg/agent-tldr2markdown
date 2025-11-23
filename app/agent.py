"""Top level agent."""
import os
from datetime import date

import google.auth
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools import load_artifacts
from google.genai import types

from .prompts import return_instructions_root

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

date_today = date.today()

root_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL", "gemini-2.5-flash"),
    name="tldr2markdown",
    instruction=return_instructions_root(),
    global_instruction=(
        f"""
        You summarize the given TLDR email in Markdown format.
        Todays date: {date_today}
        """
    ),
    tools=[
        load_artifacts,
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)

app = App(root_agent=root_agent, name="app")
