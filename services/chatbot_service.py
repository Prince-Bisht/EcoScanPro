"""Eco AI: Gemini-backed environmental assistant with honest offline fallback."""
import json
import logging
import os
from pathlib import Path

LOGGER = logging.getLogger(__name__)
KB_PATH = Path(__file__).resolve().parents[1] / 'data' / 'waste_guidelines.json'


def _knowledge_base():
    try:
        data = json.loads(KB_PATH.read_text(encoding='utf-8'))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError) as exc:
        LOGGER.warning('Knowledge base unavailable: %s', exc)
        return {}


def _fallback(message, kb, notice=None):
    words = message.lower()
    aliases = {
        'biodegradable': ['biodegradable', 'organic'],
        'plastic': ['plastic'],
        'segregation': ['segregat', 'wet waste', 'dry waste'],
        'compost': ['compost'],
        'e-waste': ['e-waste', 'electronic', 'battery'],
        'recycling': ['recycl'],
        'india': ['india', 'municipal'],
        'pollution': ['pollut', 'burning'],
        'ai': ['artificial intelligence', 'machine learning', 'ai '],
    }
    matches = [str(kb[k]) for k, terms in aliases.items()
               if k in kb and any(term in words for term in terms)]
    response = ' '.join(matches[:2]) if matches else (
        'I can help with plastic recycling, composting, segregation, e-waste and sustainable habits. '
        'Please ask about one of these topics. I cannot verify city-specific collection rules.'
    )
    return {
        'response': response,
        'mode': 'knowledge-base-fallback',
        'notice': notice or 'Offline curated knowledge-base response, not a live AI response.',
    }


def answer(message, history=None):
    kb = _knowledge_base()
    key = os.getenv('GEMINI_API_KEY', '').strip()
    if not key:
        return _fallback(message, kb, 'Gemini API key is not configured; showing offline knowledge-base guidance.')

    try:
        from google import genai
        from google.genai import types

        context = '\n'.join(f'{name}: {value}' for name, value in kb.items())
        system_instruction = (
            'You are Eco AI, the helpful environmental assistant for EcoScanPro. '
            'Answer questions about waste, recycling, composting, pollution and sustainability. '
            'Reply in the user\'s language (English, Hindi or Hinglish), using clear practical explanations. '
            'Use the knowledge base when relevant, but do not invent local recycling regulations. '
            'Mention uncertainty where appropriate. Never claim to have visually inspected an image. '
            'If asked unrelated questions, politely redirect to environmental topics.\n\n'
            'Environmental knowledge base:\n' + context
        )
        contents = []
        for item in (history or [])[-10:]:
            if not isinstance(item, dict):
                continue
            role = item.get('role')
            content = item.get('content')
            if role in ('user', 'assistant') and isinstance(content, str) and content.strip():
                contents.append(types.Content(
                    role='model' if role == 'assistant' else 'user',
                    parts=[types.Part.from_text(text=content[:2000])]
                ))
        contents.append(types.Content(role='user', parts=[types.Part.from_text(text=message)]))

        client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=20000))
        result = client.models.generate_content(
            model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.5,
                max_output_tokens=700,
            ),
        )
        response = (result.text or '').strip()
        if not response:
            raise ValueError('Gemini returned an empty response')
        return {'response': response, 'mode': 'llm'}
    except Exception as exc:
        LOGGER.warning('Gemini request failed (%s): %s', type(exc).__name__, exc)
        return _fallback(message, kb, 'Live Gemini service is unavailable; showing offline knowledge-base guidance.')
