import argparse
import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

load_dotenv()

agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


def load_config() -> dict:
    """Load agent configuration and force local memory storage to avoid DB errors."""
    config_path = Path(__file__).parent.parent / "agent_config.json"

    config = {}
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading config file: {e}")

    config["storage"] = {"type": "memory"}
    config["scheduler"] = {"type": "memory"}

    if "name" not in config:
        config["name"] = "quiz-generator-agent"
    if "author" not in config:
        config["author"] = "developer@example.com"
    if "deployment" not in config:
        config["deployment"] = {"url": "http://127.0.0.1:3773", "expose": True}

    return config


async def initialize_agent() -> None:
    """Initialize the Quiz Generator agent with the OpenRouter model."""
    global agent

    # Get API keys and Model from environment
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    model_name = os.getenv("MODEL_NAME", "google/gemini-2.0-flash-lite-preview-02-05:free")

    if not openrouter_api_key:
        print(" ERROR: OPENROUTER_API_KEY not found in .env")
        sys.exit(1)

    # Initialize the OpenRouter Model
    model = OpenRouter(
        id=model_name,
        api_key=openrouter_api_key,
    )

    # Create the Quiz Generator agent
    agent = Agent(
        name="Quiz Generator Agent",
        model=model,
        description="Educational Assessment Expert specializing in MCQ generation.",
        instructions=dedent("""\
            You are a professional teacher. Your task is to generate a quiz based on the provided text.
            
            1. Create exactly 10 Multiple Choice Questions (MCQs).
            2. For each question, provide 4 options: A, B, C, and D.
            3. Ensure only one answer is correct.
            4. Provide a 1-sentence explanation for why the correct answer is right.
            5. Keep the language clear and academic.
        """),
        expected_output=dedent("""\
            # 📝 Quiz: Knowledge Check
            
            ---
            
            ### Question 1
            [Question text here]
            A) [Option A]
            B) [Option B]
            C) [Option C]
            D) [Option D]
            
            **Correct Answer:** [A/B/C/D]
            **Explanation:** [Brief explanation]
            
            ---
            (Repeat for questions 2 through 10)
        """),
        markdown=True,
    )
    print(f" Quiz Generator Agent initialized with model: {model_name}")


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    # Lazy initialization on first call to ensure async safety
    async with _init_lock:
        if not _initialized:
            await initialize_agent()
            _initialized = True

    if not agent:
        raise RuntimeError("Agent failed to initialize.")

    # Run the agent and return the response
    response = await agent.arun(messages)
    return response


def main():
    """Run the main entry point for the Bindu-powered Quiz Agent."""
    print("🤖 Quiz Generator Agent - Starting Server...")

    # Set model name if passed as argument, otherwise use .env
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default=os.getenv("MODEL_NAME"))
    args = parser.parse_args()

    if args.model:
        os.environ["MODEL_NAME"] = args.model

    # Load and clean configuration
    config = load_config()

    try:
        print(f" Server will run on: {config['deployment']['url']}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n Quiz Agent stopped by user")
    except Exception as e:
        print(f"Critical Error during startup: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
