from __future__ import annotations
import html
import os
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.db import (
    init_db, fetch_cards, create_reading, update_reading, save_review,
    save_followup, dataframe_query, table_counts, get_db_path,
    completed_lessons, save_lesson_completion,
)
from src.tarot_engine import POSITION_LABELS, SPREAD_DESCRIPTIONS, draw_cards, card_meaning
from src.curriculum import build_curriculum
from src.ai_guide import get_api_key, get_model, generate_guide_response

st.set_page_config(page_title='ARCANA LAB', layout='wide', initial_sidebar_state='expanded')
init_db()

# Typographic / diagram-led visual language. No decorative card UI or gradients.
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;450;500;600;700&display=swap');
:root {
  --bg:#0B0F10; --surface:#101718; --line:#273334; --line-soft:#1C2829;
  --ink:#E9EEEB; --muted:#93A19D; --dim:#657570; --accent:#C6A879;
  --fire:#D49A55; --water:#78A8B8; --air:#B8C6CE; --earth:#94A47C; --major:#C1B39A;
}
html, body, [class*="css"] { font-family:'IBM Plex Sans',sans-serif; }
[data-testid="stAppViewContainer"] {
  background-color:var(--bg);
  background-image:radial-gradient(rgba(137,166,155,.13) .65px, transparent .65px);
  background-size:22px 22px;
  color:var(--ink);
}
[data-testid="stHeader"] { background:rgba(11,15,16,.92); }
[data-testid="stSidebar"] { background:#0E1415; border-right:1px solid var(--line); }
[data-testid="stSidebar"] > div { padding-top:1.6rem; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { color:var(--ink); }
h1,h2,h3,h4 { font-family:'IBM Plex Sans',sans-serif !important; letter-spacing:-.035em; color:var(--ink); }
h1 { font-weight:500 !important; font-size:2.15rem !important; }
h2 { font-weight:500 !important; font-size:1.42rem !important; }
h3 { font-weight:600 !important; font-size:1.02rem !important; }
p, li { line-height:1.55; }
.arcana-kicker,.mono,.mini-label,code { font-family:'IBM Plex Mono',monospace !important; }
.arcana-kicker { color:var(--accent); font-size:10px; letter-spacing:.16em; text-transform:uppercase; }
.arcana-header { display:flex; align-items:center; justify-content:space-between; gap:20px; border-bottom:1px solid var(--line); padding:3px 0 18px; margin-bottom:22px; }
.arcana-header-copy { min-width:0; }
.arcana-header-title { font-size:2rem; line-height:1.1; letter-spacing:-.045em; font-weight:500; margin-top:7px; }
.arcana-subtitle { color:var(--muted); font-size:.91rem; margin-top:8px; max-width:800px; }
.arcana-mark { width:104px; min-width:104px; opacity:.78; }
.mini-label { font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:.12em; }
.arcana-rule { border-top:1px solid var(--line); margin:18px 0; }
.arcana-muted { color:var(--muted); }
.arcana-keywords { color:var(--accent); font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:.01em; line-height:1.7; }
.arcana-reading-item { border-left:2px solid var(--line); padding:4px 0 5px 13px; margin:8px 0 18px; }
.arcana-reading-title { font-size:1.02rem; font-weight:600; margin:5px 0 4px; }
.arcana-reading-lens { color:var(--muted); font-size:12px; margin:4px 0; }
.arcana-course-index { border-bottom:1px solid var(--line-soft); padding:8px 0; }
.arcana-stat { border-top:1px solid var(--line); padding-top:8px; }
.arcana-stat-value { font-size:1.55rem; letter-spacing:-.04em; font-weight:500; }
.arcana-stat-label { font:10px 'IBM Plex Mono',monospace; color:var(--muted); text-transform:uppercase; letter-spacing:.12em; }
.arcana-progress { height:3px; background:#263333; width:100%; margin:8px 0 14px; }
.arcana-progress > span { display:block; height:3px; background:var(--accent); }
.arcana-tag { display:inline-block; font:10px 'IBM Plex Mono',monospace; color:var(--muted); border:1px solid var(--line); padding:3px 7px; margin:2px 4px 2px 0; text-transform:uppercase; letter-spacing:.04em; }
.arcana-note { border-left:2px solid var(--accent); padding:7px 0 7px 12px; color:var(--muted); font-size:.9rem; }
.arcana-diagram { border-top:1px solid var(--line); border-bottom:1px solid var(--line); margin:12px 0 18px; padding:8px 0; }
.arcana-diagram svg { display:block; width:100%; height:auto; max-height:340px; }
.arcana-diagram text { font-family:'IBM Plex Mono',monospace; }
[data-testid="stMetric"] { background:transparent; border:0; border-top:1px solid var(--line); border-radius:0; padding:10px 0 0; }
[data-testid="stMetricLabel"] { color:var(--muted) !important; font:10px 'IBM Plex Mono',monospace !important; text-transform:uppercase; letter-spacing:.1em; }
[data-testid="stMetricValue"] { color:var(--ink) !important; font-weight:500; }
.stButton>button, [data-testid="stFormSubmitButton"] button { border-radius:2px; min-height:38px; border:1px solid #59665F; background:#D4DDDA; color:#0B1111; font-weight:600; }
.stButton>button:hover, [data-testid="stFormSubmitButton"] button:hover { border-color:var(--accent); color:#0B1111; background:#E5EAE7; }
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"],.stMultiSelect div[data-baseweb="select"] { border-radius:2px !important; }
[data-baseweb="tab-list"] { gap:16px; }
[data-baseweb="tab"] { font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.06em; }
[data-testid="stDataFrame"] { border:1px solid var(--line); }
hr { border-color:var(--line) !important; }
footer { visibility:hidden; }
</style>
''', unsafe_allow_html=True)

cards = fetch_cards()
cards_by_id = {c['card_id']: c for c in cards}
card_names = [c['card_name'] for c in cards]
card_by_name = {c['card_name']: c for c in cards}
lessons = build_curriculum(cards)
lesson_by_id = {x['lesson_id']: x for x in lessons}
completed = completed_lessons()
SUIT_COLORS = {'Wands':'#D49A55','Cups':'#78A8B8','Swords':'#B8C6CE','Pentacles':'#94A47C','Major Arcana':'#C1B39A'}


def page_header(kicker: str, title: str, subtitle: str):
    mark = '''<svg viewBox="0 0 120 92" role="img" aria-label="Geometric orbital mark">
      <g fill="none" stroke="#62756E" stroke-width=".8">
        <circle cx="60" cy="46" r="29"/><circle cx="60" cy="46" r="18" stroke="#C6A879"/>
        <path d="M60 5 L60 87 M19 46 L101 46 M31 17 L89 75 M89 17 L31 75" opacity=".65"/>
      </g><g fill="#C6A879"><circle cx="60" cy="17" r="2.7"/><circle cx="89" cy="46" r="2"/><circle cx="60" cy="75" r="2.7"/><circle cx="31" cy="46" r="2"/></g>
      <circle cx="60" cy="46" r="4" fill="#E8EDE9"/></svg>'''
    st.markdown(f'''<div class="arcana-header"><div class="arcana-header-copy">
      <div class="arcana-kicker">{html.escape(kicker)}</div><div class="arcana-header-title">{html.escape(title)}</div>
      <div class="arcana-subtitle">{html.escape(subtitle)}</div></div><div class="arcana-mark">{mark}</div></div>''', unsafe_allow_html=True)


def element_color(card: dict) -> str:
    return SUIT_COLORS.get(card.get('suit') or 'Major Arcana', SUIT_COLORS['Major Arcana'])


def render_spread_diagram(spread: str, drawn: list[dict] | None = None):
    """Render a position map for every supported spread; optionally label drawn cards."""
    positions = POSITION_LABELS[spread]
    layouts = {
        'Single-card focus': [(300, 125)],
        'Three-card reflection': [(105, 130), (300, 130), (495, 130)],
        'Decision compass': [(300, 58), (475, 145), (300, 232), (125, 145)],
        'Five-point compass': [(300, 48), (493, 125), (420, 252), (180, 252), (107, 125)],
    }
    points = layouts[spread]
    links = []
    if len(points) == 3:
        links = [(0, 1), (1, 2)]
    elif len(points) == 4:
        links = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    elif len(points) == 5:
        links = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 3), (2, 4)]
    height = 335 if len(points) == 5 else (310 if len(points) == 4 else 245)
    chunks = [f'<svg viewBox="0 0 600 {height}" role="img" aria-label="{html.escape(spread)} spread diagram">']
    for a, b in links:
        x1, y1 = points[a]; x2, y2 = points[b]
        chunks.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#3A4A46" stroke-width="1.2"/>')
    for idx, ((x, y), (label, _prompt)) in enumerate(zip(points, positions)):
        item = drawn[idx] if drawn and idx < len(drawn) else None
        color = element_color(item) if item else '#81918A'
        short_label = html.escape(label.upper())
        card_label = html.escape(item.get('card_name','')) if item else ''
        chunks.append(f'<circle cx="{x}" cy="{y}" r="25" fill="#101718" stroke="{color}" stroke-width="1.35"/>')
        chunks.append(f'<circle cx="{x}" cy="{y}" r="19" fill="none" stroke="{color}" stroke-opacity=".32" stroke-width=".8"/>')
        chunks.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{color}"/>')
        chunks.append(f'<text x="{x}" y="{y-34}" text-anchor="middle" fill="#C6A879" font-size="9">{idx+1:02d}</text>')
        # Position label and card name remain outside the node, keeping the diagram legible.
        chunks.append(f'<text x="{x}" y="{y+42}" text-anchor="middle" fill="#DDE4DF" font-size="9">{short_label[:22]}</text>')
        if card_label:
            chunks.append(f'<text x="{x}" y="{y+56}" text-anchor="middle" fill="{color}" font-size="8">{card_label[:24]}</text>')
    chunks.append('</svg>')
    st.markdown('<div class="arcana-diagram">' + ''.join(chunks) + '</div>', unsafe_allow_html=True)
    st.caption(SPREAD_DESCRIPTIONS[spread])


def stat_block(label: str, value: str):
    st.markdown(f'<div class="arcana-stat"><div class="arcana-stat-value">{html.escape(value)}</div><div class="arcana-stat-label">{html.escape(label)}</div></div>', unsafe_allow_html=True)


def render_process_map(labels: list[str], colors: list[str] | None = None, height: int = 128):
    """A compact geometric process diagram used as a primary navigation cue."""
    colors = colors or ['#C6A879'] * len(labels)
    width = max(600, len(labels) * 190)
    left, right = 78, width - 78
    xs = [left + (right-left) * i / max(1, len(labels)-1) for i in range(len(labels))]
    chunks = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Process map">']
    for i in range(len(xs)-1):
        chunks.append(f'<line x1="{xs[i]}" y1="45" x2="{xs[i+1]}" y2="45" stroke="#45534E" stroke-width="1.2"/>')
        mid = (xs[i] + xs[i+1]) / 2
        chunks.append(f'<circle cx="{mid}" cy="45" r="2" fill="#8C9A91"/>')
    for i, (x, label, color) in enumerate(zip(xs, labels, colors)):
        safe = html.escape(label.upper())
        chunks.append(f'<circle cx="{x}" cy="45" r="20" fill="#101718" stroke="{color}" stroke-width="1.5"/>')
        chunks.append(f'<circle cx="{x}" cy="45" r="13" fill="none" stroke="{color}" stroke-opacity=".3"/>')
        chunks.append(f'<text x="{x}" y="49" text-anchor="middle" fill="{color}" font-size="9">{i+1:02d}</text>')
        chunks.append(f'<text x="{x}" y="87" text-anchor="middle" fill="#DDE4DF" font-size="10">{safe[:25]}</text>')
    chunks.append('</svg>')
    st.markdown('<div class="arcana-diagram">' + ''.join(chunks) + '</div>', unsafe_allow_html=True)


def start_page():
    done = len(completed.intersection(lesson_by_id))
    total = len(lessons)
    progress = done / total if total else 0
    page_header('00 / Orientation', 'Start here', 'A guided entry into tarot. Learn the structure first, ask a focused question, then practice one reading.')
    st.markdown('<div class="mini-label">THE COMPLETE LEARNING LOOP</div>', unsafe_allow_html=True)
    render_process_map(['Orient', 'Learn', 'Ask', 'Draw', 'Reflect', 'Observe'],
                       ['#B9C4BE', '#C1B39A', '#78A8B8', '#D49A55', '#94A47C', '#B9C4BE'])

    st.markdown('<div class="arcana-rule"></div><div class="mini-label">YOUR CURRENT POSITION</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: stat_block('Course progress', f'{progress:.0%}')
    with c2: stat_block('Lessons completed', f'{done:02d} / {total:02d}')
    with c3: stat_block('Readings recorded', str(table_counts()['readings']))

    next_lesson = next((item for item in lessons if item['lesson_id'] not in completed), lessons[-1])
    st.markdown('<div class="arcana-rule"></div><div class="mini-label">RECOMMENDED NEXT STEP</div>', unsafe_allow_html=True)
    st.subheader(f"{next_lesson['sequence']:02d} / {next_lesson['title']}")
    st.write(next_lesson['objective'])
    st.caption('Open Learn in the left navigation. The course is ordered for beginners; start at lesson 01 and move forward.')

    module_rows = []
    seen = []
    for lesson in lessons:
        if lesson['module_id'] not in seen:
            seen.append(lesson['module_id'])
    for module_id in seen:
        items = [x for x in lessons if x['module_id'] == module_id]
        module_rows.append({'Module': f"{module_id} · {items[0]['module_title']}",
                            'Completed': sum(x['lesson_id'] in completed for x in items),
                            'Remaining': sum(x['lesson_id'] not in completed for x in items)})
    module_df = pd.DataFrame(module_rows)
    fig = px.bar(module_df, x=['Completed', 'Remaining'], y='Module', orientation='h',
                 title='COURSE MAP / LESSONS BY MODULE',
                 color_discrete_map={'Completed': '#C6A879', 'Remaining': '#33413C'})
    fig.update_layout(barmode='stack', showlegend=True, legend_title_text='',
                      yaxis={'categoryorder': 'array', 'categoryarray': module_df['Module'].tolist()[::-1]})
    st.plotly_chart(chart_style(fig, 300), use_container_width=True)

    st.markdown('<div class="arcana-rule"></div><div class="mini-label">THREE WAYS TO ENTER</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    routes = [
        ('01 / I am new', 'Begin with Foundations. No prior tarot knowledge is required.', 'LEARN'),
        ('02 / I have a question', 'Use the AI Question Coach to turn a vague thought into a useful reflection.', 'AI GUIDE'),
        ('03 / I already drew cards', 'Open Practice to enter a physical draw and map its positions.', 'PRACTICE'),
    ]
    for col, (title, desc, target) in zip(cols, routes):
        with col:
            st.markdown(f'<div class="arcana-reading-item"><div class="mini-label">{html.escape(title)}</div><div style="color:#AAB7B0;font-size:13px;line-height:1.5;margin-top:9px">{html.escape(desc)}</div><div class="arcana-keywords" style="margin-top:10px">OPEN {target}</div></div>', unsafe_allow_html=True)
    st.caption('Use the left navigation to open a workspace. You can return here at any time.')


def ai_guide_page():
    page_header('01 / AI-assisted learning', 'AI Guide', 'A question coach, reading interpreter and study tutor. The AI supports your thinking; it does not tell your future.')
    render_process_map(['Your context', 'Structured prompt', 'Symbolic lens', 'Insight', 'Your action'],
                       ['#78A8B8', '#C1B39A', '#D49A55', '#94A47C', '#C6A879'])

    key = get_api_key()
    if key:
        st.markdown('<div class="mini-label">CONNECTION STATUS</div>', unsafe_allow_html=True)
        st.markdown('<span class="arcana-tag" style="color:#94A47C;border-color:#53634F">AI CONNECTED</span>', unsafe_allow_html=True)
        st.caption(f'Model configured: {html.escape(get_model())}. API requests are made only when you send a message.')
    else:
        st.markdown('<span class="arcana-tag">AI NOT CONNECTED</span>', unsafe_allow_html=True)
        st.warning('The app works without AI. To activate the guide, add an OpenAI API key to Streamlit secrets. Do not put a key in app.py, GitHub, or a public file.')
        with st.expander('Connect the AI Guide / setup once'):
            st.markdown('**Local development**')
            st.markdown('Create `.streamlit/secrets.toml` inside the project:')
            st.code('OPENAI_API_KEY = "your-api-key"\nARCANA_AI_MODEL = "gpt-6-astra"', language='toml')
            st.markdown('**Streamlit Community Cloud**')
            st.markdown('Open your app → Settings → Secrets, then paste the same TOML lines. Save and let the app reload.')
            st.markdown('Create/manage API access at [OpenAI API Platform](https://platform.openai.com/). ChatGPT subscriptions and API usage have separate billing; check API billing before enabling paid usage.')
            st.caption('Only the active prompt and selected reading or lesson context are sent. The whole database is not uploaded. Avoid personal identifiers and sensitive details.')

    mode = st.radio('GUIDE MODE', ['Question coach', 'Reading interpreter', 'Study tutor'], horizontal=True, key='ai_guide_mode')
    context = ''
    chat_scope = mode
    options = pd.DataFrame()
    placeholder = 'Ask a question.'
    if mode == 'Question coach':
        st.markdown('<div class="mini-label">QUESTION DESIGN / VISUAL LOGIC</div>', unsafe_allow_html=True)
        render_process_map(['Vague thought', 'Real situation', 'Open question', 'Useful action'],
                           ['#657570', '#78A8B8', '#C6A879', '#94A47C'])
        domain = st.selectbox('LIFE DOMAIN', ['Identity & values', 'Work & learning', 'Relationships', 'Health & body', 'Resources & security', 'Creativity', 'Time & priorities', 'Other'], key='ai_question_domain')
        context = f"Question design mode. Life domain: {domain}. Available spreads and position logic: " + '; '.join(f"{name}: " + ' → '.join(label for label, _ in defs) for name, defs in POSITION_LABELS.items())
        chat_scope = f'{mode}|{domain}'
        placeholder = 'Describe what is on your mind in ordinary language. It does not need to be a good tarot question yet.'
    elif mode == 'Reading interpreter':
        options = dataframe_query('SELECT reading_id, created_at, question FROM readings ORDER BY created_at DESC LIMIT 100')
        if options.empty:
            st.info('Create a reading in Practice first. The AI interpreter needs the actual question, spread positions and cards to work from.')
            context = 'No saved reading selected.'
        else:
            ids = [int(x) for x in options['reading_id'].tolist()]
            labels = {int(row.reading_id): f"#{int(row.reading_id):04d} · {str(row.question)[:72]}" for row in options.itertuples()}
            chosen = st.selectbox('READING TO INTERPRET', ids, format_func=lambda x: labels[x], key='ai_reading_choice')
            chat_scope = f'{mode}|{chosen}'
            r_df = dataframe_query('SELECT * FROM readings WHERE reading_id=?', (chosen,))
            draw_df = dataframe_query('''SELECT rc.position_index, rc.position_label, rc.orientation,
                rc.personal_interpretation, c.card_name, c.suit, c.arcana, c.element,
                c.upright_keywords, c.reversed_keywords, c.imagery_observation,
                c.reflection_prompt_1, c.reflection_prompt_2
                FROM reading_cards rc JOIN cards c ON c.card_id=rc.card_id
                WHERE rc.reading_id=? ORDER BY rc.position_index''', (chosen,))
            if not r_df.empty and not draw_df.empty:
                r = r_df.iloc[0]
                st.markdown('<div class="mini-label">SELECTED READING / POSITION MAP</div>', unsafe_allow_html=True)
                render_spread_diagram(r['spread_type'], draw_df.to_dict('records'))
                context_lines = [f"Question: {r['question']}", f"Life domain: {r['life_domain']}", f"Context: {r.get('context', '')}", f"Spread: {r['spread_type']}", 'Position data:']
                for _, card in draw_df.iterrows():
                    key_col = 'upright_keywords' if card['orientation'] == 'Upright' else 'reversed_keywords'
                    context_lines.append(f"{card['position_index']}. {card['position_label']} — {card['card_name']} ({card['orientation']}; {card['suit']}; {card['arcana']}); keywords: {card[key_col]}; image: {card['imagery_observation']}; prompt: {card['reflection_prompt_1']} {card['reflection_prompt_2']}; user's note: {card['personal_interpretation'] or 'none'}")
                context = 'Use this saved reading as reference data. Do not invent facts.\n' + '\n'.join(context_lines)
            placeholder = 'Ask what a card-position relationship might suggest, request an alternative interpretation, or ask for help finding the reading’s central pattern.'
    else:
        lesson_labels = {x['lesson_id']: f"{x['sequence']:02d} · {x['title']}" for x in lessons}
        selected_lesson = st.selectbox('CURRENT LESSON', list(lesson_labels), format_func=lambda x: lesson_labels[x], key='ai_tutor_lesson')
        chat_scope = f'{mode}|{selected_lesson}'
        lesson = lesson_by_id[selected_lesson]
        context = f"Study tutor mode. Lesson: {lesson['title']}. Objective: {lesson['objective']}. Key points: {'; '.join(lesson['key_points'])}. Exercise: {lesson['exercise']}"
        if lesson.get('card_id') in cards_by_id:
            card = cards_by_id[lesson['card_id']]
            context += f"\nCard: {card['card_name']}. Upright: {card['upright_keywords']}. Reversed: {card['reversed_keywords']}. Imagery: {card['imagery_observation']}. Plain explanation: {card['child_explanation']}"
        placeholder = 'Ask for an explanation, a worked example, or a quick test of your understanding.'

    if st.session_state.get('ai_chat_scope') != chat_scope:
        st.session_state['ai_chat_scope'] = chat_scope
        st.session_state['ai_messages'] = []
    messages = st.session_state.setdefault('ai_messages', [])
    if st.button('Clear this conversation', key='clear_ai_chat'):
        st.session_state['ai_messages'] = []
        st.rerun()
    st.markdown('<div class="arcana-rule"></div><div class="mini-label">CONVERSATION / SESSION ONLY</div>', unsafe_allow_html=True)
    if not messages:
        welcome = {
            'Question coach': 'Tell me what is on your mind. I will help turn it into one clear, open question and recommend a spread.',
            'Reading interpreter': 'Ask about a pattern in the selected reading. I will separate traditional symbolism from your own context.',
            'Study tutor': 'Ask about this lesson. I will explain the idea, give an example and test your recall.',
        }[mode]
        with st.chat_message('assistant'):
            st.write(welcome)
    for item in messages:
        with st.chat_message(item['role']):
            st.markdown(item['content'])

    if mode == 'Reading interpreter' and options.empty:
        st.caption('Create a reading in Practice, then return here to explore it with the AI Guide.')
    elif not key:
        st.caption('Connect an API key above to start the conversation. The course and reading tools remain available without AI.')
    else:
        prompt = st.chat_input(placeholder)
        if prompt:
            with st.chat_message('user'):
                st.markdown(prompt)
            with st.chat_message('assistant'):
                with st.spinner('Structuring the response…'):
                    try:
                        reply = generate_guide_response(mode=mode, context=context, message=prompt, history=messages)
                        st.markdown(reply)
                        messages.extend([{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': reply}])
                    except RuntimeError as exc:
                        st.error(str(exc))




def render_keyword_orbit(card: dict, orientation: str = 'Upright'):
    """Turn a card's stored keyword group into a four-node orbit diagram."""
    meaning = card_meaning(card, orientation)
    words = [x.strip() for x in meaning['keywords'].split(',') if x.strip()][:4]
    if not words:
        words = [meaning['keywords'] or 'No keywords']
    positions = [(105, 72), (495, 72), (105, 188), (495, 188)]
    center_x, center_y = 300, 130
    color = element_color(card)
    parts = ['<svg viewBox="0 0 600 260" role="img" aria-label="Card keyword orbit">']
    parts.append('<circle cx="300" cy="130" r="86" fill="none" stroke="#34443F" stroke-dasharray="2 5"/>')
    parts.append('<circle cx="300" cy="130" r="57" fill="none" stroke="#4A5B54" stroke-width="1"/>')
    for i, word in enumerate(words):
        x, y = positions[i]
        parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" stroke="{color}" stroke-opacity=".65" stroke-width="1"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="34" fill="#101718" stroke="{color}" stroke-width="1.2"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="28" fill="none" stroke="{color}" stroke-opacity=".24"/>')
        label = html.escape(word[:22])
        parts.append(f'<text x="{x}" y="{y+3}" text-anchor="middle" fill="#E2E8E4" font-size="9">{label}</text>')
    title = html.escape(card['card_name'][:28])
    sub = html.escape(f"{card.get('suit','')} / {orientation}"[:32])
    parts.append('<circle cx="300" cy="130" r="39" fill="#101718" stroke="#C6A879" stroke-width="1.4"/>')
    parts.append(f'<text x="300" y="126" text-anchor="middle" fill="#E9EEEB" font-size="10">{title}</text>')
    parts.append(f'<text x="300" y="143" text-anchor="middle" fill="#A9B6AF" font-size="8">{sub}</text>')
    parts.append('</svg>')
    st.markdown('<div class="arcana-diagram">' + ''.join(parts) + '</div>', unsafe_allow_html=True)


def course_page():
    total = len(lessons)
    done = len(completed.intersection(lesson_by_id))
    progress = done / total if total else 0
    page_header('01 / Structured course', 'Learn tarot, in sequence', 'A complete pathway from deck fundamentals to independent, responsible readings. 93 lessons · 8 modules.')
    st.markdown(f'<div class="arcana-progress"><span style="width:{progress*100:.2f}%"></span></div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    with p1: stat_block('Course completion', f'{progress:.0%}')
    with p2: stat_block('Lessons completed', f'{done:02d} / {total}')
    with p3: stat_block('Lessons remaining', str(total-done))
    st.markdown('<div class="arcana-rule"></div>', unsafe_allow_html=True)

    module_order = []
    for lesson in lessons:
        if lesson['module_id'] not in [m[0] for m in module_order]:
            module_order.append((lesson['module_id'], lesson['module_title']))
    module_ids = [x[0] for x in module_order]
    selected_module = st.selectbox('COURSE MODULE', module_ids,
        format_func=lambda key: f"{key}  /  {next(title for mid,title in module_order if mid == key)}",
        key='course_module')
    module_lessons = [x for x in lessons if x['module_id'] == selected_module]
    completed_in_module = sum(x['lesson_id'] in completed for x in module_lessons)
    st.caption(f'MODULE PROGRESS  ·  {completed_in_module} / {len(module_lessons)} lessons complete')
    lesson_ids = [x['lesson_id'] for x in module_lessons]
    if st.session_state.get('course_lesson') not in lesson_ids:
        st.session_state['course_lesson'] = lesson_ids[0]
    current_lesson_id = st.selectbox('LESSON SEQUENCE', lesson_ids,
        format_func=lambda key: f"{lesson_by_id[key]['sequence']:02d}  /  {lesson_by_id[key]['title']}" + ('   ✓' if key in completed else ''),
        key='course_lesson')
    lesson = lesson_by_id[current_lesson_id]
    if st.session_state.get('last_checked_lesson_id') != current_lesson_id:
        st.session_state['course_check_result'] = None
        st.session_state['last_checked_lesson_id'] = current_lesson_id
    st.markdown('<div class="arcana-rule"></div>', unsafe_allow_html=True)
    status = 'COMPLETED' if current_lesson_id in completed else 'IN PROGRESS'
    st.markdown(f'<div class="mini-label">LESSON {lesson["sequence"]:02d}  /  {len(lessons):02d} &nbsp;·&nbsp; {status}</div>', unsafe_allow_html=True)
    st.subheader(lesson['title'])
    st.write(lesson['objective'])

    if lesson['kind'] == 'card' and lesson['card_id'] in cards_by_id:
        card = cards_by_id[lesson['card_id']]
        color = element_color(card)
        up = card_meaning(card, 'Upright')
        rev = card_meaning(card, 'Reversed')
        st.markdown(f'''<div class="arcana-rule"></div><div class="mini-label">{html.escape(card['arcana'].upper())} ARCANA &nbsp;·&nbsp; {html.escape(card['suit'].upper())} &nbsp;·&nbsp; {html.escape(str(card['rank']))}</div>
          <div style="font-size:1.6rem;font-weight:500;margin:8px 0 4px;color:{color}">{html.escape(card['card_name'])}</div>
          <div class="arcana-keywords">UPRIGHT &nbsp;·&nbsp; {html.escape(up['keywords'])}</div>
          <div class="arcana-keywords" style="color:#9AA8A2">REVERSED · {html.escape(rev['keywords'])}</div>''', unsafe_allow_html=True)
        study_orientation = st.radio('KEYWORD MAP / ORIENTATION', ['Upright', 'Reversed'], horizontal=True, key=f'keyword_orientation_{card["card_id"]}')
        render_keyword_orbit(card, study_orientation)
        left, right = st.columns(2)
        with left:
            st.markdown('<div class="mini-label">IMAGE TO NOTICE</div>', unsafe_allow_html=True)
            st.write(card['imagery_observation'])
        with right:
            st.markdown('<div class="mini-label">TRADITIONAL CORRESPONDENCE</div>', unsafe_allow_html=True)
            correspondence = card.get('astrological_correspondence') or 'Not assigned'
            st.write(correspondence)
            if card.get('correspondence_system'):
                st.caption(card['correspondence_system'])
        st.markdown('<div class="arcana-note">' + html.escape(card['child_explanation']) + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="mini-label">REFLECTION PROMPTS</div>', unsafe_allow_html=True)
        st.write(f"1. {card['reflection_prompt_1']}  \n2. {card['reflection_prompt_2']}")
        st.markdown('<div class="arcana-rule"></div>', unsafe_allow_html=True)
        distractors = [c['upright_keywords'] for c in cards if c['card_id'] != card['card_id']]
        options = [card['upright_keywords']] + distractors[:2]
        random.Random(sum(ord(ch) for ch in card['card_id'])).shuffle(options)
        with st.form(f'lesson_check_{current_lesson_id}'):
            st.markdown('<div class="mini-label">RETRIEVAL CHECK</div>', unsafe_allow_html=True)
            selected_answer = st.radio('Which keyword group is assigned to this card when upright?', options, index=None)
            recall = st.slider('How easily could you recall this before reviewing?', 1, 5, 3)
            lesson_submit = st.form_submit_button('Check answer', use_container_width=True)
        if lesson_submit:
            correct = selected_answer == card['upright_keywords']
            interval = 1 if not correct or recall == 1 else (3 if recall == 2 else (7 if recall == 3 else (14 if recall == 4 else 30)))
            save_review({'card_id':card['card_id'], 'quiz_score':int(correct), 'quiz_total':1,
                         'recall_rating':recall, 'minutes_spent':5,
                         'next_review_at':(date.today()+timedelta(days=interval)).isoformat()})
            st.session_state['last_checked_lesson_id'] = current_lesson_id
            if correct:
                save_lesson_completion(current_lesson_id)
                st.session_state['course_check_result'] = 'correct'
            else:
                st.session_state['course_check_result'] = 'retry'
            st.rerun()
        result = st.session_state.get('course_check_result')
        if result == 'correct' and current_lesson_id in completed:
            st.success('Correct. Lesson completed and added to your review schedule.')
        elif result == 'retry':
            st.info('Not quite. Review the keywords and try again. The lesson remains open.')
    else:
        st.markdown('<div class="mini-label">CONCEPT SEQUENCE / KEY IDEAS</div>', unsafe_allow_html=True)
        render_process_map([point[:25] for point in lesson['key_points']])
        for point in lesson['key_points']:
            st.markdown(f'<div class="arcana-course-index"><span class="arcana-muted">—</span> &nbsp;{html.escape(point)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="arcana-rule"></div><div class="mini-label">PRACTICE / CHECKPOINT</div>', unsafe_allow_html=True)
        st.write(lesson['exercise'])
        with st.form(f'lesson_complete_{current_lesson_id}'):
            exercise_done = st.checkbox('I completed this exercise and can explain the main idea.', key=f'complete_check_{current_lesson_id}')
            mark_complete = st.form_submit_button('Mark lesson complete', use_container_width=True)
        if mark_complete:
            if exercise_done:
                save_lesson_completion(current_lesson_id)
                st.session_state['course_check_result'] = None
                st.rerun()
            else:
                st.warning('Complete the checkpoint before marking this lesson finished.')
        if current_lesson_id in completed:
            st.success('Lesson completed.')

    st.markdown('<div class="arcana-rule"></div><div class="mini-label">COURSE MAP</div>', unsafe_allow_html=True)
    for module_id, module_title in module_order:
        module_items = [x for x in lessons if x['module_id'] == module_id]
        module_done = sum(x['lesson_id'] in completed for x in module_items)
        with st.expander(f"{module_id}  /  {module_title}  ·  {module_done}/{len(module_items)}"):
            for item in module_items:
                flag = '✓' if item['lesson_id'] in completed else '·'
                st.markdown(f'<div class="arcana-course-index"><span class="mono" style="color:#C6A879">{item["sequence"]:02d}</span> &nbsp; {flag} &nbsp; {html.escape(item["title"])}</div>', unsafe_allow_html=True)


def practice_page():
    page_header('02 / Reading laboratory', 'Practice a reading', 'Choose a spread, study the position map, and translate card keywords into one useful insight and action.')
    st.markdown('<div class="arcana-note">Use the cards as symbolic prompts. Keep facts, assumptions and interpretations separate. The cards do not establish facts or predict outcomes.</div>', unsafe_allow_html=True)

    top_a, top_b = st.columns([1.4,1])
    with top_a:
        spread = st.selectbox('SPREAD STRUCTURE', list(POSITION_LABELS.keys()), key='practice_spread')
        question = st.text_area('REFLECTIVE QUESTION', value='What is happening within me right now, and what do I need to understand?', height=80, key='practice_question')
        context = st.text_input('CONTEXT / OPTIONAL', placeholder='One or two factual lines; separate facts from assumptions.')
        domain = st.selectbox('LIFE DOMAIN', ['Identity & values','Work & learning','Relationships','Health & body','Resources & security','Creativity','Time & priorities','Other'])
    with top_b:
        st.markdown('<div class="mini-label">SPREAD MAP / POSITION LOGIC</div>', unsafe_allow_html=True)
        render_spread_diagram(spread)

    method = st.radio('CARD SOURCE', ['Random in-app draw','Enter my physical draw'], horizontal=True, key='card_source')
    with st.form('new_reading_form'):
        tags = st.multiselect('REFLECTION THEMES', ['Change','Boundaries','Confidence','Recovery','Uncertainty','Work','Relationships','Resources','Learning','Decision','Rest','Creativity'])
        positions = POSITION_LABELS[spread]
        manual_values = []
        if method == 'Enter my physical draw':
            st.markdown('<div class="mini-label">ENTER THE CARDS YOU DREW</div>', unsafe_allow_html=True)
            for i, (position_label, prompt) in enumerate(positions, start=1):
                st.markdown(f'<div class="arcana-course-index"><span class="mono">{i:02d}</span> &nbsp;{html.escape(position_label)} <span class="arcana-muted">— {html.escape(prompt)}</span></div>', unsafe_allow_html=True)
                cc1,cc2 = st.columns(2)
                with cc1:
                    manual_name = st.selectbox(f'Card {i}', card_names, key=f'manual_card_{spread}_{i}')
                with cc2:
                    manual_orientation = st.selectbox(f'Orientation {i}', ['Upright','Reversed'], key=f'manual_orientation_{spread}_{i}')
                manual_values.append((manual_name,manual_orientation))
        else:
            reversed_probability = st.slider('REVERSED-CARD RATE', 0, 100, 30, 5,
                                              help='A setting for the random draw, not a probability about real events.')
        draw_submit = st.form_submit_button('Create reading', type='primary', use_container_width=True)

    if draw_submit:
        if not question.strip():
            st.error('Write a reflective question before creating a reading.')
        elif method == 'Enter my physical draw' and len({name for name, _orientation in manual_values}) != len(manual_values):
            st.error('A standard tarot deck contains one copy of each card. Check the manual draw for duplicates.')
        else:
            if method == 'Random in-app draw':
                chosen = draw_cards(cards, count=len(positions), reversed_probability=reversed_probability/100)
            else:
                chosen = [{**card_by_name[name], 'orientation':ori} for name,ori in manual_values]
            draw_payload = [{**card, 'position_label':positions[i][0]} for i, card in enumerate(chosen)]
            reading_id = create_reading({'question':question.strip(), 'life_domain':domain, 'context':context,
                                         'spread_type':spread, 'draw_method':method,
                                         'theme_tags':', '.join(tags)}, draw_payload)
            st.session_state['active_reading_id'] = reading_id
            st.success(f'Reading #{reading_id} recorded.')

    active_id = st.session_state.get('active_reading_id')
    if active_id:
        reading = dataframe_query('SELECT * FROM readings WHERE reading_id=?', (active_id,))
        drawn = dataframe_query('''SELECT rc.*, c.card_name, c.arcana, c.suit, c.rank, c.element,
            c.upright_keywords, c.reversed_keywords, c.technical_upright, c.technical_reversed,
            c.child_explanation, c.imagery_observation, c.reflection_prompt_1, c.reflection_prompt_2,
            c.astrological_correspondence, c.correspondence_system
            FROM reading_cards rc JOIN cards c ON c.card_id=rc.card_id
            WHERE rc.reading_id=? ORDER BY rc.position_index''', (active_id,))
        if not reading.empty and not drawn.empty:
            r = reading.iloc[0]
            spread_name = r['spread_type']
            st.markdown('<div class="arcana-rule"></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mini-label">READING {active_id:04d}  /  {html.escape(r["life_domain"].upper())}  /  {html.escape(r["created_at"])}</div>', unsafe_allow_html=True)
            st.subheader(r['question'])
            drawn_records = [x.to_dict() for _, x in drawn.iterrows()]
            st.markdown('<div class="mini-label">SPREAD DIAGRAM / SELECTED CARDS</div>', unsafe_allow_html=True)
            render_spread_diagram(spread_name, drawn_records)
            suit_counts = pd.Series([x.get('suit', 'Major Arcana') for x in drawn_records]).value_counts().rename_axis('Suit').reset_index(name='Cards')
            suit_colors = {'Wands':'#D49A55','Cups':'#78A8B8','Swords':'#B8C6CE','Pentacles':'#94A47C','Major Arcana':'#C1B39A'}
            pattern_fig = px.pie(suit_counts, names='Suit', values='Cards', hole=.68, title='DRAW COMPOSITION / SUIT')
            pattern_fig.update_traces(marker=dict(colors=[suit_colors.get(x, '#C1B39A') for x in suit_counts['Suit']]), textposition='outside', textinfo='label+value')
            pattern_fig.update_layout(showlegend=False)
            pattern_col, note_col = st.columns([1, 1.3])
            with pattern_col:
                st.plotly_chart(chart_style(pattern_fig, 250), use_container_width=True)
            with note_col:
                st.markdown('<div class="mini-label">PATTERN KEY</div>', unsafe_allow_html=True)
                st.caption('The chart shows only the composition of this draw. It does not indicate good, bad, balanced or unbalanced outcomes.')
                for suit, count in suit_counts[['Suit','Cards']].itertuples(index=False, name=None):
                    st.markdown(f'<div class="arcana-course-index"><span class="arcana-keywords">{html.escape(str(suit).upper())}</span> &nbsp; {int(count)} card(s)</div>', unsafe_allow_html=True)
            st.markdown('<div class="mini-label">POSITION INTERPRETATION</div>', unsafe_allow_html=True)
            cards_per_row = min(len(drawn_records), 3)
            for start in range(0, len(drawn_records), cards_per_row):
                row_items = drawn_records[start:start+cards_per_row]
                cols = st.columns(len(row_items))
                for col, item in zip(cols, row_items):
                    meaning = card_meaning(item, item['orientation'])
                    pos_index = int(item['position_index'])
                    pos_def = POSITION_LABELS[spread_name][pos_index-1]
                    color = element_color(item)
                    with col:
                        st.markdown(f'''<div class="arcana-reading-item" style="border-left-color:{color}">
                          <div class="mini-label">{pos_index:02d} / {html.escape(item['position_label'].upper())}</div>
                          <div class="arcana-reading-title">{html.escape(item['card_name'])}</div>
                          <div class="mini-label">{html.escape(item['orientation'].upper())} · {html.escape(item['suit'].upper())}</div>
                          <div class="arcana-keywords">{html.escape(meaning['keywords'])}</div>
                          <div class="arcana-reading-lens">POSITION LENS · {html.escape(pos_def[1])}</div>
                          <div class="arcana-reading-lens">IMAGE · {html.escape(item['imagery_observation'])}</div>
                        </div>''', unsafe_allow_html=True)

            st.markdown('<div class="arcana-rule"></div><div class="mini-label">YOUR INTERPRETATION / SYNTHESIS</div>', unsafe_allow_html=True)
            st.caption('Use the keywords and position lenses as inputs. You write the interpretation; the app does not decide what the cards mean for you.')
            with st.form(f'interpretation_{active_id}'):
                card_updates=[]
                for idx, item in enumerate(drawn_records, start=1):
                    personal = st.text_input(f"{idx:02d} · {item['position_label']} / {item['card_name']}", key=f'personal_{active_id}_{idx}', placeholder='What does this symbol suggest in the context of your question?')
                    card_updates.append({'position_index':idx,'visual_observation':'','personal_interpretation':personal})
                overall = st.text_area('SYNTHESIS / HOW DO THE POSITIONS RELATE?', height=70, key=f'overall_{active_id}', placeholder='Write one to three concise lines.')
                insight = st.text_input('KEY INSIGHT / ONE SENTENCE', key=f'insight_{active_id}')
                action = st.text_input('ACTION / SOMETHING WITHIN YOUR CONTROL', key=f'action_{active_id}')
                follow_due = st.date_input('REVIEW DATE', value=date.today()+timedelta(days=7), key=f'due_{active_id}')
                save_interpretation = st.form_submit_button('Save insight and action', type='primary', use_container_width=True)
            if save_interpretation:
                update_reading(active_id, {'initial_observation':'','overall_interpretation':overall,
                    'key_insight':insight,'action_commitment':action,'follow_up_due':follow_due.isoformat()}, card_updates)
                st.success('Interpretation saved.')

    st.markdown('<div class="arcana-rule"></div><div class="mini-label">FOLLOW-UP / OBSERVE WHAT HAPPENED</div>', unsafe_allow_html=True)
    reading_options = dataframe_query('SELECT reading_id, created_at, question FROM readings ORDER BY created_at DESC LIMIT 100')
    if reading_options.empty:
        st.caption('Follow-up becomes available after the first reading.')
    else:
        labels = {int(row.reading_id): f"#{int(row.reading_id)} · {row.created_at} · {str(row.question)[:65]}" for row in reading_options.itertuples()}
        chosen_reading = st.selectbox('READING TO REVIEW', list(labels.keys()), format_func=lambda x: labels[x])
        with st.form('followup_form'):
            outcome = st.text_area('OBSERVABLE OUTCOME', placeholder='What happened since the reading? Separate observable facts from impressions.', height=65)
            completed_action = st.checkbox('I completed the action I committed to')
            alignment = st.slider('How aligned did the action feel with my values?',1,5,3)
            emotion = st.selectbox('DOMINANT FEELING', ['','Calm','Uncertain','Motivated','Relieved','Frustrated','Sad','Hopeful','Other'])
            follow_submit = st.form_submit_button('Save follow-up')
        if follow_submit:
            save_followup({'reading_id':chosen_reading,'outcome_note':outcome,'action_completed':completed_action,
                           'alignment_rating':alignment,'emotion_label':emotion})
            st.success('Follow-up saved.')


def chart_style(fig, height=300):
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family='IBM Plex Sans', color='#DDE4DF', size=11),
                      margin=dict(l=8,r=8,t=38,b=8), height=height,
                      title=dict(font=dict(size=13, family='IBM Plex Mono'), x=0, xanchor='left'),
                      legend=dict(orientation='h', y=1.12, x=0))
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor='#33403C', tickfont=dict(size=10))
    fig.update_yaxes(showgrid=True, gridcolor='#263230', zeroline=False, linecolor='#33403C', tickfont=dict(size=10))
    return fig


def observe_page():
    page_header('03 / Personal observatory', 'Observe your patterns', 'A descriptive record of study, readings, recurring symbols and actions. Frequency is not destiny or diagnosis.')
    counts = table_counts()
    study_avg = dataframe_query('SELECT AVG(1.0*quiz_score/quiz_total) AS avg_score FROM study_reviews').iloc[0]['avg_score']
    read_cards = dataframe_query('SELECT COUNT(*) AS n FROM reading_cards').iloc[0]['n']
    stats = [('Readings',str(counts['readings'])),('Cards drawn',str(int(read_cards))),('Lessons complete',f'{len(completed)} / {len(lessons)}'),('Study reviews',str(counts['study_reviews']))]
    cols = st.columns(4)
    for col,(label,value) in zip(cols,stats):
        with col: stat_block(label,value)
    readings = dataframe_query('SELECT * FROM readings ORDER BY created_at')
    if readings.empty:
        st.markdown('<div class="arcana-rule"></div>', unsafe_allow_html=True)
        st.caption('No reading data yet. Use Practice to create your first record.')
    else:
        details = dataframe_query('SELECT * FROM v_reading_detail ORDER BY created_at DESC')
        left,right = st.columns(2)
        with left:
            domain_counts = readings['life_domain'].value_counts().rename_axis('Domain').reset_index(name='Records')
            fig = px.bar(domain_counts, x='Records', y='Domain', orientation='h', title='READINGS / LIFE DOMAIN', text='Records')
            fig.update_traces(marker_color='#9BAE9F', textposition='outside')
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(chart_style(fig,280), use_container_width=True)
        with right:
            suit_data = details[details['suit'] != 'Major Arcana']['suit'].value_counts().rename_axis('Suit').reset_index(name='Draws')
            fig = px.bar(suit_data, x='Suit', y='Draws', title='MINOR ARCANA / SUIT DISTRIBUTION', color='Suit',
                         color_discrete_map={'Wands':'#D49A55','Cups':'#78A8B8','Swords':'#B8C6CE','Pentacles':'#94A47C'})
            fig.update_layout(showlegend=False)
            st.plotly_chart(chart_style(fig,280), use_container_width=True)
        timeline = readings.copy()
        timeline['date'] = pd.to_datetime(timeline['created_at'], errors='coerce').dt.date
        trend = timeline.groupby('date').size().reset_index(name='Readings')
        fig = px.line(trend, x='date', y='Readings', title='READING ACTIVITY / OVER TIME', markers=True)
        fig.update_traces(line_color='#C6A879', marker_color='#C6A879', line_width=1.5)
        st.plotly_chart(chart_style(fig,250), use_container_width=True)
        frequent = details['card_name'].value_counts().head(10).rename_axis('Card').reset_index(name='Frequency')
        st.markdown('<div class="mini-label">MOST FREQUENTLY RECORDED CARDS</div>', unsafe_allow_html=True)
        st.dataframe(frequent, use_container_width=True, hide_index=True)
        tag_values=[]
        for value in readings['theme_tags'].fillna(''):
            tag_values.extend([tag.strip() for tag in str(value).split(',') if tag.strip()])
        if tag_values:
            tag_df = pd.Series(tag_values).value_counts().head(12).rename_axis('Theme').reset_index(name='Frequency')
            fig = px.bar(tag_df, x='Frequency', y='Theme', orientation='h', title='SELF-SELECTED THEMES')
            fig.update_traces(marker_color='#78A8B8')
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(chart_style(fig,300), use_container_width=True)
        st.markdown('<div class="mini-label">READING JOURNAL / KEY INSIGHTS AND ACTIONS</div>', unsafe_allow_html=True)
        journal = readings[['reading_id','created_at','life_domain','question','key_insight','action_commitment','follow_up_due']].copy()
        st.dataframe(journal.sort_values('created_at',ascending=False), use_container_width=True, hide_index=True)

    study = dataframe_query('''SELECT sr.created_at, c.card_name, sr.quiz_score, sr.quiz_total,
        sr.recall_rating, sr.minutes_spent, sr.next_review_at FROM study_reviews sr
        JOIN cards c ON c.card_id=sr.card_id ORDER BY sr.created_at''')
    if not study.empty:
        st.markdown('<div class="mini-label">LEARNING PERFORMANCE / RECALL</div>', unsafe_allow_html=True)
        study['accuracy'] = study['quiz_score'] / study['quiz_total']
        fig = px.line(study, x='created_at', y='accuracy', markers=True, title='RETRIEVAL CHECK ACCURACY')
        fig.update_traces(line_color='#94A47C', marker_color='#94A47C')
        fig.update_yaxes(range=[0,1], tickformat='.0%')
        st.plotly_chart(chart_style(fig,240), use_container_width=True)


def data_page():
    page_header('04 / Data stewardship', 'Data and exports', 'Your records are personal data. Back them up and keep private journals out of the public repository.')
    counts = table_counts()
    cols = st.columns(len(counts))
    for col,(name,n) in zip(cols,counts.items()):
        with col: stat_block(name.replace('_',' '),str(n))
    st.markdown('<div class="arcana-rule"></div><div class="mini-label">REFERENCE DATA / DOWNLOAD</div>', unsafe_allow_html=True)
    db_path = get_db_path()
    if db_path.exists():
        st.download_button('Download SQLite database backup', data=db_path.read_bytes(), file_name='arcana_lab_backup.sqlite', mime='application/octet-stream', use_container_width=True)
    for title, filename, mime in [
        ('Cards CSV','cards.csv','text/csv'),
        ('Correspondences CSV','correspondences.csv','text/csv'),
        ('SQLite schema SQL','schema.sql','text/plain'),
    ]:
        path = ROOT / ('database' if filename.endswith('.sql') else 'data') / filename
        st.download_button(f'Download {title}', data=path.read_bytes(), file_name=filename, mime=mime)
    st.markdown('<div class="arcana-rule"></div><div class="mini-label">PERSONAL RECORDS / CSV EXPORT</div>', unsafe_allow_html=True)
    for table in ['readings','reading_cards','study_reviews','followups','lesson_progress']:
        df = dataframe_query(f'SELECT * FROM {table}')
        st.download_button(f'Export {table}.csv', data=df.to_csv(index=False).encode('utf-8-sig'), file_name=f'{table}.csv', mime='text/csv')
    st.markdown('<div class="arcana-rule"></div>', unsafe_allow_html=True)
    st.warning('This is a single-user prototype. Streamlit Community Cloud storage is not durable. Back up records or add a managed database before relying on hosted persistence.')
    st.caption('Keep data/arcana_lab.db, personal exports, passwords and API keys out of GitHub. Reference meanings and application code may remain public.')


with st.sidebar:
    st.markdown('<div class="arcana-kicker">PERSONAL LEARNING SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('## ARCANA LAB')
    st.caption('SYMBOLIC STUDY / READING / SELF-REFLECTION')
    page = st.radio('WORKSPACE', ['Start here', 'AI Guide', 'Learn', 'Practice', 'Observe', 'Data'],
                    index=0, label_visibility='collapsed', key='workspace_page')
    st.markdown('<div class="arcana-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">RECOMMENDED SEQUENCE</div>', unsafe_allow_html=True)
    st.caption('START → LEARN → ASK → PRACTICE → OBSERVE')
    st.markdown('<div class="arcana-rule"></div>', unsafe_allow_html=True)
    st.caption('v0.3 · AI guide and guided onboarding')
    st.info('Tarot is a symbolic reflection practice. It is not a diagnostic or predictive method.')

if page == 'Start here':
    start_page()
elif page == 'AI Guide':
    ai_guide_page()
elif page == 'Learn':
    course_page()
elif page == 'Practice':
    practice_page()
elif page == 'Observe':
    observe_page()
else:
    data_page()
