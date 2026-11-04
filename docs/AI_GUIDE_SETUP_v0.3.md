# ARCANA LAB — AI Guide setup v0.3

## What the AI does

The AI Guide has three bounded roles:

1. **Question Coach** — turns an unstructured concern into an open, specific, non-predictive question and suggests a spread whose positions fit the question.
2. **Reading Interpreter** — reads only the selected saved reading: question, context, positions, cards, orientations, stored keywords, imagery cues and the learner's notes. It offers hypotheses, patterns and an action prompt; it does not claim to reveal facts.
3. **Study Tutor** — explains the selected lesson, gives a plain-language example and checks understanding.

The AI is optional. Without an API key, the course, reading journal, visualizations and exports continue to work.

## Connect locally

1. Create an API key in the OpenAI API Platform.
2. In the project folder, create `.streamlit/secrets.toml`.
3. Add:

```toml
OPENAI_API_KEY = "your-api-key"
ARCANA_AI_MODEL = "gpt-6-astra"
```

4. Install dependencies and restart the Streamlit app.

## Connect on Streamlit Community Cloud

Open the deployed app's **Settings → Secrets** and paste the same TOML lines. Save the settings; the app reloads with the configured key.

Never commit `secrets.toml`, a `.env` file, or an API key to GitHub. The project `.gitignore` excludes the local secrets file.

## Billing and privacy

OpenAI API usage is billed separately from ChatGPT subscriptions. Check the API billing/usage settings before enabling paid usage.

When a message is submitted, ARCANA LAB sends the current prompt, the selected mode context, and up to the last four exchanges to the OpenAI API. In Reading Interpreter mode, that context includes only the selected reading and its card metadata. The application does not upload the SQLite database, unrelated readings, or the full journal.

Do not include real names, addresses, account details, secrets, or highly sensitive personal information in prompts. AI conversation history is held in the current Streamlit session and is not saved as a permanent database conversation.

## Interpretation boundaries

- Tarot is a symbolic and reflective practice, not a diagnostic, evidence-generating, or predictive method.
- AI outputs are possible interpretations, not authoritative meanings.
- The app distinguishes traditional card data from user context and AI-generated hypotheses.
- The user owns every decision and action.
- Do not use readings or AI output as a substitute for qualified medical, legal, financial, or safety advice.

## Technical design

- Client: OpenAI Python SDK.
- API: Responses API.
- Model: configurable through `ARCANA_AI_MODEL`; default `gpt-6-astra`.
- Key resolution: `OPENAI_API_KEY` environment variable or Streamlit secrets.
- SDK import is lazy, so the app can launch with no AI key configured.
- API errors are caught and shown as short user-facing messages; secrets and request headers are not displayed.
