
"""
EcoScanPro - Eco AI Chatbot Service

Features:
- Google Gemini AI integration
- Hindi, English and Hinglish support
- Conversation history
- Environmental knowledge base
- Automatic retry for temporary server errors
- Offline fallback
"""

import json
import logging
import os
import time
from pathlib import Path

from google import genai
from google.genai import types, errors

LOGGER = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
KB_PATH = ROOT / "data" / "waste_guidelines.json"

MAX_RETRIES = 3


# ------------------------------------------
# Load Environmental Knowledge Base
# ------------------------------------------

def _knowledge_base():
    try:
        with open(KB_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, dict) else {}

    except (OSError, ValueError) as exc:
        LOGGER.warning("Knowledge base error: %s", exc)
        return {}


# ------------------------------------------
# Offline Knowledge Base Fallback
# ------------------------------------------

def _fallback(message, kb, notice=None):

    words = message.lower()

    aliases = {
        "biodegradable": ["biodegradable", "organic"],
        "plastic": ["plastic"],
        "segregation": ["segregat", "wet waste", "dry waste"],
        "compost": ["compost"],
        "e-waste": ["e-waste", "electronic", "battery"],
        "recycling": ["recycl"],
        "india": ["india", "municipal"],
        "pollution": ["pollut", "burning"],
        "ai": ["artificial intelligence", "machine learning"],
    }

    matches = []

    for category, keywords in aliases.items():
        if category in kb:
            if any(word in words for word in keywords):
                matches.append(str(kb[category]))

    if matches:
        response = " ".join(matches[:2])
    else:
        response = (
            "I can help with recycling, waste segregation, "
            "composting, electronic waste, plastic pollution "
            "and sustainable living. Please ask about "
            "one of these environmental topics."
        )

    return {
        "response": response,
        "mode": "knowledge-base-fallback",
        "notice": notice or (
            "Offline knowledge-base response. "
            "Not a live Gemini AI response."
        ),
    }


# ------------------------------------------
# Main Gemini Chatbot
# ------------------------------------------

def answer(message, history=None):

    kb = _knowledge_base()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        return _fallback(
            message,
            kb,
            "Gemini API key is not configured."
        )

    try:

        # ----------------------------------
        # System Instructions
        # ----------------------------------

        context = "\n".join(
            f"{name}: {value}"
            for name, value in kb.items()
        )

        system_instruction = (
            "You are Eco AI, the intelligent environmental "
            "assistant of EcoScanPro. "

            "You specialize in waste management, recycling, "
            "plastic pollution, composting, electronic waste, "
            "waste segregation and sustainability. "

            "Answer naturally in the user's language. "
            "Support English, Hindi and Hinglish. "

            "If the user speaks Hinglish, reply in Hinglish. "

            "Give accurate, helpful and practical explanations. "

            "Use the environmental knowledge base when relevant. "

            "Do not invent local recycling regulations. "

            "Explain uncertainty when information is unavailable. "

            "Do not claim to have analyzed an image unless "
            "image analysis was actually performed. "

            "Keep answers conversational and easy to understand. "

            "If a question is unrelated to environmental topics, "
            "politely redirect the conversation. "

            "\n\nEnvironmental Knowledge Base:\n"
            + context
        )

        # ----------------------------------
        # Conversation History
        # ----------------------------------

        contents = []

        for item in (history or [])[-10:]:

            if not isinstance(item, dict):
                continue

            role = item.get("role")
            content = item.get("content")

            if (
                role in ("user", "assistant")
                and isinstance(content, str)
                and content.strip()
            ):

                gemini_role = (
                    "model" if role == "assistant"
                    else "user"
                )

                contents.append(
                    types.Content(
                        role=gemini_role,
                        parts=[
                            types.Part.from_text(
                                text=content[:2000]
                            )
                        ],
                    )
                )

        # Current User Message

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=message
                    )
                ],
            )
        )

        # ----------------------------------
        # Initialize Gemini Client
        # ----------------------------------

        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=20000
            ),
        )

        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        ).strip()

        if not model_name:
            raise ValueError("GEMINI_MODEL is empty")

        # ----------------------------------
        # Gemini API With Automatic Retry
        # ----------------------------------

        result = None

        for attempt in range(MAX_RETRIES):

            try:

                result = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.5,
                        max_output_tokens=700,
                    ),
                )

                break

            except errors.ServerError as exc:

                error_code = getattr(exc, "code", None)

                if (
                    error_code not in (500, 502, 503, 504)
                    or attempt == MAX_RETRIES - 1
                ):
                    raise

                wait_time = 2 ** attempt

                LOGGER.warning(
                    "Gemini server error %s. "
                    "Retry %s/%s after %s seconds.",
                    error_code,
                    attempt + 1,
                    MAX_RETRIES,
                    wait_time,
                )

                time.sleep(wait_time)

        # ----------------------------------
        # Process Gemini Response
        # ----------------------------------

        if result is None:
            raise RuntimeError("Gemini returned no result")

        response = (result.text or "").strip()

        if not response:
            raise ValueError(
                "Gemini returned an empty response"
            )

        return {
            "response": response,
            "mode": "llm",
            "provider": "gemini",
        }

    except Exception as exc:

        LOGGER.warning(
            "Gemini request failed (%s): %s",
            type(exc).__name__,
            exc,
        )

        return _fallback(
            message,
            kb,
            "Live Gemini service is unavailable. "
            "Showing offline knowledge-base guidance.",
        )
