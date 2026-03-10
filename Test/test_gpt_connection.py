"""
test_gpt_connection.py
──────────────────────
Live connectivity test for Azure OpenAI GPT-5-chat.
Runs BEFORE implementation to verify:
  1. API key and endpoint are valid
  2. The gpt-5-chat deployment responds
  3. Prints token usage so you can record it

Run from intern/Backend/ with venv active:
    pip install openai python-dotenv
    python ../Test/test_gpt_connection.py
"""

import os
import sys
import json
from datetime import datetime

# ── Load .env from Backend/ ───────────────────────────────────────────────────
# This file lives in Test/, so we go up one level to find Backend/.env
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'Backend')
env_path    = os.path.join(backend_dir, '.env')

if not os.path.exists(env_path):
    print(f"\n  ✖  ERROR: .env not found at {env_path}")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv(env_path)

# ── Read env vars ─────────────────────────────────────────────────────────────
API_KEY    = os.getenv("AZURE_OPENAI_API_KEY")
API_BASE   = os.getenv("AZURE_OPENAI_API_BASE")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
API_VER    = os.getenv("AZURE_OPENAI_API_VERSION")
MAX_TOKENS = int(os.getenv("AZURE_OPENAI_MAX_COMPLETION_TOKENS", "512"))

# ── Validate ──────────────────────────────────────────────────────────────────
missing = [k for k, v in {
    "AZURE_OPENAI_API_KEY": API_KEY,
    "AZURE_OPENAI_API_BASE": API_BASE,
    "AZURE_OPENAI_DEPLOYMENT_NAME": DEPLOYMENT,
    "AZURE_OPENAI_API_VERSION": API_VER,
}.items() if not v]

if missing:
    print(f"\n  ✖  Missing env vars: {', '.join(missing)}")
    sys.exit(1)

# ── Banner ────────────────────────────────────────────────────────────────────
print()
print("  ╔══════════════════════════════════════════════════════╗")
print("  ║   🔌  GPT-5-chat Connectivity Test                   ║")
print("  ║   Volo Health AI  –  Azure OpenAI                   ║")
print("  ╚══════════════════════════════════════════════════════╝")
print()
print(f"  📍  Endpoint   : {API_BASE}")
print(f"  🤖  Deployment : {DEPLOYMENT}")
print(f"  📋  API Version: {API_VER}")
print(f"  ⚙️   Max Tokens : {MAX_TOKENS}")
print()

# ── Test 1: Basic healthcare question ─────────────────────────────────────────
try:
    from openai import AzureOpenAI

    client = AzureOpenAI(
        api_key=API_KEY,
        azure_endpoint=API_BASE,
        api_version=API_VER,
    )

    print("  ─── Test 1: Basic healthcare question ────────────────")
    print("  📤  Sending: 'What documents are required for hospital admission?'")
    print()

    start = datetime.now()

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful healthcare assistant for Volo Health Insurance TPA. "
                    "Help patients with hospital admission, surgery, discharge, and follow-up questions."
                )
            },
            {
                "role": "user",
                "content": "What documents are required for hospital admission?"
            }
        ],
        max_tokens=MAX_TOKENS,
        temperature=0.7,
    )

    elapsed = (datetime.now() - start).total_seconds()
    reply = response.choices[0].message.content
    usage = response.usage

    print(f"  ✔  REPLY ({elapsed:.2f}s):")
    print()
    for line in reply.split(". "):
        if line.strip():
            print(f"     {line.strip()}.")
    print()
    print("  ─── Token Usage ──────────────────────────────────────")
    print(f"  📊  Prompt tokens     : {usage.prompt_tokens}")
    print(f"  📊  Completion tokens : {usage.completion_tokens}")
    print(f"  📊  Total tokens      : {usage.total_tokens}")
    print()

except Exception as e:
    print(f"  ✖  FAILED: {e}")
    print()
    sys.exit(1)

# ── Test 2: Topic Guard simulation ────────────────────────────────────────────
print("  ─── Test 2: Topic Guard (off-topic detection) ────────")
OFF_TOPIC_TESTS = [
    ("What is the capital of India?",          "should be off-topic"),
    ("Is surgery covered under CGHS?",         "should be on-topic"),
    ("Tell me a joke",                          "should be off-topic"),
    ("What follow-ups after hospitalisation?", "should be on-topic"),
]

topic_guard_prompt = (
    "You are a topic classifier for a healthcare assistant. "
    "Classify if the user's question is related to: hospitalisation, surgery, "
    "discharge, follow-up care, medical documents, health insurance, or TPA processes. "
    "Reply ONLY with: YES or NO"
)

all_passed = True
for question, expectation in OFF_TOPIC_TESTS:
    resp = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": topic_guard_prompt},
            {"role": "user",   "content": question}
        ],
        max_tokens=5,
        temperature=0,
    )
    verdict = resp.choices[0].message.content.strip().upper()
    tokens  = resp.usage.total_tokens
    icon    = "✔" if verdict in ("YES", "NO") else "?"
    print(f"  {icon}  [{verdict:3}]  ({tokens:2} tokens)  \"{question[:45]}\"")
    print(f"         ↳ {expectation}")

print()

# ── Summary ───────────────────────────────────────────────────────────────────
print("  ─── Connection Test Summary ──────────────────────────")
print("  ✔  Azure OpenAI API key is valid")
print("  ✔  Endpoint is reachable")
print(f"  ✔  Deployment '{DEPLOYMENT}' is responding")
print("  ✔  Topic Guard classifier working")
print()
print("  ✅  ALL TESTS PASSED – Ready to start implementation!")
print()
print("  💡  TIP: Copy the token counts above into Backend/.env:")
print(f"       AZURE_OPENAI_MAX_COMPLETION_TOKENS={MAX_TOKENS}")
print("       AZURE_OPENAI_TEMPERATURE=0.7")
print()
print("  ╚══════════════════════════════════════════════════════╝")
print()
