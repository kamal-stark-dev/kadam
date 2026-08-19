"""
Quick smoke test — confirms OPENAI_API_KEY works before Day 4 AI integration.

Run from backend/:
    python scripts/test_openai.py
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not found. Create backend/.env with:")
    print('  OPENAI_API_KEY=sk-your-key-here')
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("openai package not installed. Run: pip install openai")
    sys.exit(1)

client = OpenAI()

try:
    resp = client.responses.create(
        model="gpt-5.6-terra",
        input="Reply with exactly: connection ok",
    )
    print("Response:", resp.output_text.strip())
    print("OpenAI connection is working.")
except Exception as e:
    print("OpenAI call failed:", e)
    sys.exit(1)
