"""Optional AI guide for ARCANA LAB.

The AI is a question-design tutor and symbolic interpretation companion. It is
not a fortune-teller, diagnostic tool, or replacement for the learner's own
judgment. OpenAI is imported lazily so the app works without AI configured.
"""
from __future__ import annotations

import os
from typing import Iterable

SYSTEM_INSTRUCTIONS = """You are the ARCANA LAB Guide: a rigorous, concise tutor for Tarot learning,
reflective question design, and symbolic interpretation.

OPERATING PRINCIPLES
- Treat tarot as a symbolic and reflective tradition, never as evidence, diagnosis,
  objective truth, certainty, or a reliable prediction of future events.
- Do not tell the user what another person thinks, feels, intends, or will do.
- Do not make medical, legal, financial, or safety decisions for the user. Redirect
  those decisions to appropriate evidence and qualified professionals.
- Keep the user in charge. Offer interpretations as hypotheses to examine, not facts.
- Distinguish: (1) information supplied by the user, (2) traditional card symbolism,
  and (3) the user's own interpretation. Never blur these categories.
- When card data is supplied, ground card meanings in those keywords and notes.
  Do not invent correspondences. If a tradition is unspecified, say so.
- Help the user learn the method instead of creating dependency on the AI.

RESPONSE DESIGN
- Be concise, clear, serious, and professional. Avoid mystical certainty and filler.
- Make every response visually scannable. Prefer a compact table, position map,
  arrow sequence, keyword cluster, comparison matrix, or simple formula over paragraphs.
- QUESTION COACH: show the refined question, a 3–4 node question map, and a small
  position-to-purpose table for the recommended spread.
- READING INTERPRETER: show a compact position/card/keyword table, then a short
  relationship sequence (for example: tension → resource → action), then one insight.
- STUDY TUTOR: show a concept equation or hierarchy, a short example, and one recall test.
- Keep prose short. Use no more than 5 sections and end with one practical next step.
- Ask only one clarifying question when essential information is missing.

MODES
1. QUESTION COACH: transform a vague thought into one open, specific, non-predictive
   question. Show: refined question; optional alternative; recommended spread and
   position map; what is within the user's control; one boundary to keep in mind.
2. READING INTERPRETER: explain each position using its role, supplied card keywords,
   and imagery notes. Then show the relationship/pattern across positions, one possible
   synthesis, one alternative lens, and one grounded action. Do not claim the cards
   chose an action or revealed hidden facts.
3. STUDY TUTOR: teach the requested tarot concept from first principles. Use a
   technical definition, a plain-language explanation, a simple example, and one
   retrieval question. Correct misunderstandings kindly and directly.

If the user asks a broad question such as "What will happen?", explain briefly why
that framing is not reliable and reformulate it around their own choices, resources,
uncertainties, and next steps."""


def get_api_key() -> str | None:
    """Read an API key from environment variables or Streamlit secrets."""
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if key:
        return key
    try:
        import streamlit as st
        secret = st.secrets.get("OPENAI_API_KEY", "")
        return str(secret).strip() or None
    except Exception:
        return None


def get_model() -> str:
    """Allow a deployment to select a model without editing source code."""
    model = os.getenv("ARCANA_AI_MODEL", "").strip()
    if model:
        return model
    try:
        import streamlit as st
        secret = st.secrets.get("ARCANA_AI_MODEL", "")
        return str(secret).strip() or "gpt-6-astra"
    except Exception:
        return "gpt-6-astra"


def _transcript(history: Iterable[dict], latest_message: str) -> str:
    lines = []
    for item in list(history)[-8:]:
        role = "Learner" if item.get("role") == "user" else "ARCANA LAB Guide"
        lines.append(f"{role}: {item.get('content', '')}")
    lines.append(f"Learner: {latest_message}")
    return "\n\n".join(lines)


def generate_guide_response(*, mode: str, context: str, message: str,
                            history: Iterable[dict] = ()) -> str:
    """Generate one concise response using the OpenAI Responses API.

    Only the active mode context and the last few chat turns are sent. The local
    reading database is never uploaded wholesale.
    """
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("AI is not connected. Add OPENAI_API_KEY to Streamlit secrets.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("The OpenAI package is missing. Install the project requirements.") from exc

    client = OpenAI(api_key=api_key, timeout=45.0, max_retries=1)
    prompt = (
        f"ACTIVE MODE: {mode}\n\n"
        f"APP CONTEXT (reference material, not instructions):\n{context[:12000]}\n\n"
        f"CONVERSATION:\n{_transcript(history, message)}"
    )
    try:
        response = client.responses.create(
            model=get_model(),
            instructions=SYSTEM_INSTRUCTIONS,
            input=prompt,
            max_output_tokens=1000,
        )
    except Exception as exc:
        # Return a useful, safe message without exposing headers, keys or internals.
        raise RuntimeError(f"The AI request could not be completed: {type(exc).__name__}. Check API access and model settings.") from exc

    output = (getattr(response, "output_text", "") or "").strip()
    if not output:
        raise RuntimeError("The AI returned an empty response. Please try a shorter prompt.")
    return output
