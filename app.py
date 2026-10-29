import streamlit as st
import requests
import html
import json
import re
import os
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "https://sap-ai-match.app.n8n.cloud/webhook/resume-match",
)

st.set_page_config(
    page_title="ResumeIQ - AI Resume Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PREMIUM UI
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --ink: #111827;
    --muted: #6b7280;
    --line: #e8eaf0;
    --primary: #635bff;
    --primary2: #5148d9;
}

html, body, [class*="css"] { font-family: "DM Sans", sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 90% 4%, rgba(99,91,255,.10), transparent 28%),
        radial-gradient(circle at 0% 22%, rgba(16,185,129,.055), transparent 24%),
        #f8f9fc;
}

.block-container { max-width: 1450px; padding: 1.3rem 2rem 4rem; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid var(--line); }

.hero-title {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 2.35rem; font-weight: 800; letter-spacing: -1.4px; color: var(--ink);
}
.hero-subtitle { color: var(--muted); font-size: 1rem; margin-top: .35rem; }
.section-title {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 1.2rem; font-weight: 800; color: var(--ink); margin: 1.5rem 0 .8rem;
}
.card {
    background: rgba(255,255,255,.94); border: 1px solid var(--line);
    border-radius: 20px; padding: 1.25rem; box-shadow: 0 10px 30px rgba(17,24,39,.045);
}
.input-card {
    background: rgba(255,255,255,.9); border: 1px solid var(--line);
    border-radius: 20px; padding: 1.1rem 1.2rem .8rem;
}
.result-hero {
    background:
        radial-gradient(circle at 92% 15%, rgba(99,91,255,.13), transparent 25%),
        linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
    border: 1px solid #e6e7f2; border-radius: 26px; padding: 1.8rem;
    box-shadow: 0 18px 45px rgba(31,41,55,.07);
}
.score-ring {
    width: 175px; height: 175px; border-radius: 50%;
    background: conic-gradient(var(--primary) calc(var(--score) * 1%), #e9eaf2 0);
    display: flex; align-items: center; justify-content: center; position: relative;
}
.score-ring::after {
    content: ""; position: absolute; width: 139px; height: 139px;
    border-radius: 50%; background: #fff;
}
.score-inner { position: relative; z-index: 2; text-align: center; }
.score-value {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 2.6rem; font-weight: 800; color: var(--ink); line-height: 1;
}
.score-caption {
    color: var(--muted); font-size: .7rem; font-weight: 800;
    letter-spacing: 1.1px; text-transform: uppercase; margin-top: .45rem;
}
.verdict-pill {
    display: inline-block; padding: .48rem .9rem; border-radius: 999px;
    background: #ecfdf5; color: #047857; font-size: .83rem; font-weight: 700; margin-top: .75rem;
}
.metric-card {
    background: #fff; border: 1px solid var(--line); border-radius: 18px;
    padding: 1.05rem 1.1rem; min-height: 124px; box-shadow: 0 7px 22px rgba(17,24,39,.035);
}
.metric-label { color: var(--muted); font-size: .82rem; font-weight: 700; }
.metric-value {
    color: var(--ink); font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 1.8rem; font-weight: 800; margin-top: .28rem;
}
.mini-track { height: 7px; border-radius: 99px; background: #eef0f5; margin-top: .78rem; overflow: hidden; }
.mini-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #635bff, #8b83ff); }
.summary-card {
    background: #fff; border: 1px solid var(--line); border-radius: 20px;
    padding: 1.25rem 1.4rem; color: #374151; line-height: 1.75;
    box-shadow: 0 8px 24px rgba(17,24,39,.035);
}
.rec-card {
    display: flex; gap: .85rem; padding: .95rem 1rem; margin: .55rem 0;
    border: 1px solid var(--line); border-radius: 15px; background: #fff;
}
.rec-number {
    min-width: 30px; height: 30px; border-radius: 9px; background: #eeecff;
    color: #5148d9; display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: .78rem;
}
.rec-text { color: #374151; line-height: 1.55; font-size: .9rem; }
.insight-good { border-left: 4px solid #10b981; background: #ecfdf5; padding: .9rem 1rem; border-radius: 12px; color: #065f46; margin: .45rem 0; }
.insight-warn { border-left: 4px solid #f59e0b; background: #fffbeb; padding: .9rem 1rem; border-radius: 12px; color: #92400e; margin: .45rem 0; }
.insight-bad  { border-left: 4px solid #ef4444; background: #fef2f2; padding: .9rem 1rem; border-radius: 12px; color: #991b1b; margin: .45rem 0; }
.small-muted { color: #9ca3af; font-size: .76rem; }
.stButton > button { border-radius: 12px !important; min-height: 45px; font-weight: 700 !important; }
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #635bff, #5148d9) !important;
    border: none !important; box-shadow: 0 8px 20px rgba(99,91,255,.25);
}
textarea { border-radius: 14px !important; }
hr { border-color: var(--line) !important; }
.skill-pill {
    display: inline-block; padding: .38rem .7rem; border-radius: 999px;
    margin: .2rem .25rem .2rem 0; font-size: .78rem; font-weight: 700;
}
.skill-match { background: #ecfdf5; color: #047857; }
.skill-missing { background: #fef2f2; color: #b91c1c; }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "analysis_result": None,
    "job_description": "",
    "resume_name": "",
    "history": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# HELPERS
# ============================================================

CORE_FIELDS = [
    "matchScore", "verdict", "summary", "experienceMatch", "skillsMatch",
    "educationMatch", "matchedSkills", "missingSkills", "recommendations",
]


def render_html(markup):
    """
    Render an HTML snippet in Streamlit.

    Streamlit's markdown parser treats lines indented by 4+ spaces (and HTML
    blocks containing blank lines) as code, which prints raw HTML text.
    Removing indentation and line breaks forces it to render as real HTML.
    """
    compact = re.sub(r"\s*\n\s*", "", str(markup).strip())
    st.markdown(compact, unsafe_allow_html=True)


def looks_like_analysis(data):
    return isinstance(data, dict) and any(key in data for key in CORE_FIELDS)


def try_parse_json_string(value):
    if not isinstance(value, str):
        return None
    text = value.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, (dict, list)) else None
    except (json.JSONDecodeError, TypeError):
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            parsed = json.loads(text[start:end + 1])
            return parsed if isinstance(parsed, (dict, list)) else None
        except (json.JSONDecodeError, TypeError):
            return None
    return None


def normalize_n8n_response(data):
    """Accept common n8n response shapes and return the ResumeIQ dict."""
    if isinstance(data, list):
        if not data:
            return {}
        for item in data:
            normalized = normalize_n8n_response(item)
            if looks_like_analysis(normalized):
                return normalized
        return normalize_n8n_response(data[0])

    if not isinstance(data, dict):
        return {}

    if looks_like_analysis(data):
        return data

    for wrapper in ["output", "result", "data", "response", "body", "json", "item"]:
        nested = data.get(wrapper)
        if isinstance(nested, (dict, list)):
            normalized = normalize_n8n_response(nested)
            if normalized:
                return normalized
        if isinstance(nested, str):
            parsed = try_parse_json_string(nested)
            if parsed is not None:
                normalized = normalize_n8n_response(parsed)
                if normalized:
                    return normalized

    for text_key in ["text", "content", "message", "response", "output"]:
        value = data.get(text_key)
        if isinstance(value, str):
            parsed = try_parse_json_string(value)
            if parsed is not None:
                normalized = normalize_n8n_response(parsed)
                if normalized:
                    return normalized
        elif isinstance(value, dict):
            normalized = normalize_n8n_response(value)
            if normalized:
                return normalized

    return data


def score(value):
    try:
        return max(0.0, min(100.0, float(value)))
    except (ValueError, TypeError):
        return 0.0


def as_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, str) and value.strip():
        parsed = try_parse_json_string(value)
        if isinstance(parsed, list):
            return parsed
        return [value]
    return []


def clean_display_text(value):
    """Convert text or accidental HTML from the AI workflow into readable text."""
    text = str(value if value is not None else "")
    text = re.sub(r"(?is)<(style|script)\b[^>]*>.*?</\1\s*>", " ", text)
    text = re.sub(r"(?s)<[^>]*>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_list(value):
    items = [clean_display_text(item) for item in as_list(value)]
    return [item for item in items if item]


def build_insights(match_score, experience, skills, education):
    insights = []

    if match_score >= 80:
        insights.append(("good", "Strong overall alignment between the resume and the job description."))
    elif match_score >= 60:
        insights.append(("warn", "The resume has useful overlap with the role, but additional tailoring may improve the match."))
    else:
        insights.append(("bad", "The current resume has significant gaps compared with the supplied job description."))

    if skills >= 80:
        insights.append(("good", "Skills alignment is strong according to the n8n analysis."))
    elif skills >= 60:
        insights.append(("warn", "Skills are partially aligned; the resume may benefit from clearer emphasis on role-relevant technologies."))
    else:
        insights.append(("bad", "Skills alignment is an important area to improve for this role."))

    if experience >= 80:
        insights.append(("good", "Experience alignment is strong for the supplied job description."))
    elif experience >= 60:
        insights.append(("warn", "Experience is partially aligned; stronger project or internship evidence may help."))
    else:
        insights.append(("bad", "Experience alignment is currently limited for this role."))

    if education >= 80:
        insights.append(("good", "Education alignment is strong according to the analysis."))
    elif education >= 60:
        insights.append(("warn", "Education appears reasonably aligned but should be clearly presented against the role requirements."))
    else:
        insights.append(("bad", "Education requirements may not be clearly demonstrated in the current analysis."))

    return insights


def create_interview_questions(matched=None, missing=None):
    matched = matched or []
    missing = missing or []

    questions = [
        "Tell me about yourself and explain why your background fits this role.",
        "Walk me through your most relevant project for this position.",
        "What was the most difficult technical problem you solved in your recent project?",
        "How do you approach debugging a problem in a production application?",
        "How do you learn a technology that you have not used before?",
        "Describe a situation where you improved the performance or quality of a project.",
    ]
    for skill in matched[:4]:
        questions.append(f"Explain your practical experience with {skill} and where you applied it.")
    for skill in missing[:3]:
        questions.append(f"The role mentions {skill}. How would you demonstrate or build this skill?")
    return questions[:12]


def rec_card_html(idx, text):
    return (
        f'<div class="rec-card"><div class="rec-number">{idx}</div>'
        f'<div class="rec-text">{html.escape(str(text))}</div></div>'
    )


def join_natural(items):
    items = [str(i) for i in items if str(i).strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def fit_level(value):
    """Turn a numeric score into a plain-language level (numbers are never shown)."""
    if value >= 75:
        return "strong"
    if value >= 50:
        return "moderate"
    return "limited"


def build_hiring_perspective(result):
    """Write a realistic, qualitative hiring-manager review from the analysis content."""
    overall = fit_level(score(result.get("matchScore", 0)))
    exp_level = fit_level(score(result.get("experienceMatch", 0)))
    skill_level = fit_level(score(result.get("skillsMatch", 0)))
    edu_level = fit_level(score(result.get("educationMatch", 0)))

    matched = clean_list(result.get("matchedSkills", []))
    missing = clean_list(result.get("missingSkills", []))
    critical = clean_list(result.get("criticalMissingSkills", []))
    strengths = clean_list(result.get("strengths", []))
    weaknesses = clean_list(result.get("weaknesses", []))

    gaps = critical or missing
    items = []

    # Overall impression
    overall_text = {
        "strong": "The resume lines up well with this role. The candidate looks like a credible fit and is worth moving forward to a conversation.",
        "moderate": "The resume shows a partial fit. There is relevant material, but some parts of the role are not clearly covered, so a conversation would be needed to judge the fit properly.",
        "limited": "The resume does not currently show a close fit with this role. Most of the core requirements are either missing or not evident from what was submitted.",
    }[overall]
    items.append(("Overall impression", overall_text))

    # Skills
    if matched:
        skill_tail = {
            "strong": "Together these cover most of the technical needs of the role.",
            "moderate": "These cover part of the role, but the technical depth still needs to be confirmed.",
            "limited": "These are relevant, but they cover only a small part of what the role requires.",
        }[skill_level]
        items.append(("Relevant skills", f"The resume shows {join_natural(matched[:6])}. {skill_tail}"))
    else:
        items.append(("Relevant skills", "No clear overlap with the required skills could be identified from the resume."))

    # Gaps
    if gaps:
        items.append((
            "Skill gaps",
            f"The following were not evident on the resume: {join_natural(gaps[:6])}. "
            "Check whether these are genuinely missing or simply not described, and whether they could be learned on the job.",
        ))
    else:
        items.append(("Skill gaps", "No significant skill gaps were identified against the job description."))

    # Experience
    exp_text = {
        "strong": "The experience described appears relevant to the responsibilities of the role. Confirm the scope of the work and the candidate's own contribution.",
        "moderate": "Some of the experience is relevant, but it is not a direct match for the role. Ask how the candidate's past work would carry over to these responsibilities.",
        "limited": "The experience described has little overlap with this role. Look for projects, internships or self-directed work that could make up for it.",
    }[exp_level]
    items.append(("Experience", exp_text))

    # Education
    edu_text = {
        "strong": "The educational background meets what the role asks for.",
        "moderate": "The educational background is reasonably related to the role, though the fit is not exact. Weigh it against practical experience.",
        "limited": "The educational background does not clearly match the stated requirements. Consider whether the qualification is truly essential for the role.",
    }[edu_level]
    items.append(("Education", edu_text))

    # Strengths and concerns from the AI analysis (when provided)
    if strengths:
        items.append(("Notable strengths", join_natural(strengths[:3]) + "."))
    if weaknesses:
        items.append(("Points of concern", join_natural(weaknesses[:3]) + "."))

    # Interview focus
    focus = []
    if matched:
        focus.append(f"ask for a concrete example of work involving {join_natural(matched[:2])}")
    if gaps:
        focus.append(f"explore how the candidate would approach {join_natural(gaps[:2])}")
    if not focus:
        focus.append("ask the candidate to walk through their most relevant project and what they personally delivered")
    items.append(("Interview focus", "In a screening conversation, " + " and ".join(focus) + "."))

    # Suggested next step (decision support only)
    next_step = {
        "strong": "Shortlist the candidate and arrange a screening interview.",
        "moderate": "Keep the candidate under review. A short screening call is worthwhile if the missing skills are trainable or the applicant pool is small.",
        "limited": "This resume is not a strong match for this opening as submitted. Consider other roles, or revisit if the candidate can show more relevant experience.",
    }[overall]
    items.append(("Suggested next step", next_step + " The final decision rests with the hiring team."))

    return items


def make_html_report(result, resume_name):
    match_score = score(result.get("matchScore", 0))
    experience = score(result.get("experienceMatch", 0))
    skills = score(result.get("skillsMatch", 0))
    education = score(result.get("educationMatch", 0))
    ats_score = score(result.get("atsScore", result.get("ATSScore", 0)))

    verdict = html.escape(clean_display_text(result.get("verdict", "Analysis complete")) or "Analysis complete")
    summary = html.escape(clean_display_text(result.get("summary", "No summary available.")) or "No summary available.")
    recommendations = clean_list(result.get("recommendations", []))

    rec_html = "".join(f"<li>{html.escape(item)}</li>" for item in recommendations)
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")

    hiring_html = "".join(
        f"<p><b>{html.escape(title)}:</b> {html.escape(text)}</p>"
        for title, text in build_hiring_perspective(result)
    )

    ats_html = (
        f'<div class="box"><span class="muted">ATS Score</span><br><b>{ats_score:.0f}%</b></div>'
        if ats_score > 0 else ""
    )
    ats_line = (
        f"ATS score is {ats_score:.0f}%; review parsing and keyword coverage."
        if ats_score > 0
        else "No ATS score was provided; review resume readability and relevant terminology manually."
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ResumeIQ Report</title>
<style>
body{{font-family:Arial,sans-serif;background:#f6f7fb;color:#111827;padding:40px;}}
.container{{max-width:900px;margin:auto;background:white;padding:42px;border-radius:24px;}}
h1{{margin-bottom:4px;}}
.muted{{color:#6b7280;}}
.score{{font-size:56px;font-weight:800;color:#635bff;margin:20px 0 4px;}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:25px 0;}}
.box{{padding:18px;border:1px solid #e5e7eb;border-radius:16px;}}
.box b{{font-size:28px;}}
ul{{line-height:1.7;}}
.section{{margin-top:30px;}}
p{{line-height:1.7;}}
</style>
</head>
<body>
<div class="container">
<h1>ResumeIQ - Resume Analysis Report</h1>
<div class="muted">Generated {now}</div>
<div class="section"><b>Resume:</b> {html.escape(resume_name or "Uploaded resume")}</div>
<div class="score">{match_score:.0f}%</div>
<div><b>{verdict}</b></div>
<div class="grid">
<div class="box"><span class="muted">Experience</span><br><b>{experience:.0f}%</b></div>
<div class="box"><span class="muted">Skills</span><br><b>{skills:.0f}%</b></div>
<div class="box"><span class="muted">Education</span><br><b>{education:.0f}%</b></div>
{ats_html}
</div>
<div class="section"><h2>Summary</h2><p>{summary}</p></div>
<div class="section"><h2>Recommendations</h2><ul>{rec_html or "<li>None returned</li>"}</ul></div>
<div class="section">
<h2>Hiring Manager Perspective</h2>
{hiring_html}
</div>
</div>
</body>
</html>"""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    render_html(
        """
        <div style="font-family:'Plus Jakarta Sans';font-size:1.35rem;font-weight:800;color:#111827;padding:.35rem 0 .7rem;">ResumeIQ</div>
        <div style="color:#6b7280;font-size:.82rem;line-height:1.5;">AI workspace for resume-to-job matching.</div>
        """
    )

    st.divider()

    page = st.radio(
        "Workspace",
        ["Resume Analysis", "Analysis History", "About"],
        label_visibility="collapsed",
    )

    st.divider()

    if st.session_state.history:
        st.caption(f"{len(st.session_state.history)} analysis(es) this session")

    render_html('<div class="small-muted">Streamlit · n8n · Ollama AI</div>')

# ============================================================
# ABOUT
# ============================================================

if page == "About":
    render_html('<div class="hero-title">ResumeIQ</div>')
    render_html('<div class="hero-subtitle">AI-powered resume and job description analysis with practical candidate insights.</div>')
    st.divider()

    cols = st.columns(4)
    cards = [
        ("🎯", "Match Score", "Overall alignment from n8n"),
        ("📊", "Match Breakdown", "Experience, skills and education"),
        ("💡", "AI Insights", "Practical analysis and recommendations"),
        ("📥", "Report Export", "Download the analysis report"),
    ]
    for col, (icon, title, body) in zip(cols, cards):
        with col:
            render_html(
                f"""
                <div class="card">
                    <div style="font-size:1.5rem;">{icon}</div>
                    <b>{title}</b><br>
                    <span style="color:#6b7280;font-size:.82rem;">{body}</span>
                </div>
                """
            )
    st.stop()

# ============================================================
# HISTORY
# ============================================================

if page == "Analysis History":
    render_html('<div class="hero-title">Analysis History</div>')
    render_html('<div class="hero-subtitle">Your recent analyses are stored only for this Streamlit session.</div>')
    st.divider()

    if not st.session_state.history:
        st.info("No analyses yet. Run your first resume analysis from the Resume Analysis page.")
    else:
        for item in reversed(st.session_state.history):
            result = item["result"]
            current_score = score(result.get("matchScore", 0))
            verdict_text = clean_display_text(result.get("verdict", "Analysis complete"))

            render_html(
                f"""
                <div class="card" style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;gap:1rem;">
                        <div>
                            <b>{html.escape(item["resume_name"])}</b>
                            <div class="small-muted">{html.escape(item["time"])}</div>
                        </div>
                        <div style="font-size:1.35rem;font-weight:800;color:#635bff;">{current_score:.0f}%</div>
                    </div>
                    <div style="margin-top:.5rem;color:#6b7280;">{html.escape(verdict_text)}</div>
                </div>
                """
            )

        if st.button("Clear session history"):
            st.session_state.history = []
            st.rerun()

    st.stop()

# ============================================================
# MAIN HEADER
# ============================================================

top1, top2 = st.columns([5, 1])

with top1:
    render_html('<div class="hero-title">ResumeIQ</div>')
    render_html('<div class="hero-subtitle">Turn a resume and job description into a clear visual AI analysis report.</div>')

with top2:
    render_html('<div style="text-align:right;padding-top:.35rem;"><span class="small-muted">● Local AI</span></div>')

# ============================================================
# INPUT
# ============================================================

render_html('<div class="section-title">Analyze a candidate</div>')

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    render_html(
        '<div class="input-card"><b>📄 Resume</b><br>'
        '<span style="color:#6b7280;font-size:.82rem;">PDF resume • sent directly to n8n for AI matching</span></div>'
    )
    resume = st.file_uploader("Upload resume", type=["pdf"], label_visibility="collapsed")
    if resume:
        st.success(f"Resume uploaded: {resume.name}")

with col2:
    render_html(
        '<div class="input-card"><b>💼 Job Description</b><br>'
        '<span style="color:#6b7280;font-size:.82rem;">Paste the complete job requirements</span></div>'
    )
    job_description = st.text_area(
        "Job description",
        height=175,
        placeholder="Example: Looking for a Python Developer with SQL, REST API, Git and data analysis experience...",
        label_visibility="collapsed",
    )

st.write("")

run_col, reset_col = st.columns([5, 1])
with run_col:
    analyze = st.button("Analyze Resume", type="primary", use_container_width=True)
with reset_col:
    reset = st.button("Reset", use_container_width=True)

# ============================================================
# RESET
# ============================================================

if reset:
    st.session_state.analysis_result = None
    st.session_state.job_description = ""
    st.session_state.resume_name = ""
    st.rerun()

# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze:
    if resume is None:
        st.warning("Please upload a PDF resume.")
        st.stop()

    if not job_description.strip():
        st.warning("Please enter the job description.")
        st.stop()

    st.session_state.job_description = job_description
    st.session_state.resume_name = resume.name

    with st.spinner("Sending resume to n8n Cloud → AI Agent..."):
        try:
            files = {"resume": (resume.name, resume.getvalue(), "application/pdf")}
            data = {"job_description": job_description}

            response = requests.post(N8N_WEBHOOK_URL, files=files, data=data, timeout=180)

            if response.status_code >= 400:
                st.error(f"n8n returned HTTP {response.status_code}")
                with st.expander("View n8n response"):
                    st.code(response.text)
                st.stop()

            try:
                raw = response.json()
            except ValueError:
                st.error("n8n did not return valid JSON.")
                with st.expander("View n8n response"):
                    st.code(response.text)
                st.stop()

            result = normalize_n8n_response(raw)

            if not result:
                st.error("n8n returned an empty result.")
                st.json(raw)
                st.stop()

            st.session_state.analysis_result = result
            st.session_state.history.append(
                {
                    "resume_name": resume.name,
                    "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "result": result,
                }
            )
            st.success("Analysis completed successfully.")

        except requests.exceptions.Timeout:
            st.error("n8n took too long to respond. Check the n8n Cloud workflow and AI Agent execution.")
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to n8n at {N8N_WEBHOOK_URL}. Check that the workflow is active.")
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")

# ============================================================
# RESULTS
# ============================================================

result = st.session_state.analysis_result

if result:
    match_score = score(result.get("matchScore", 0))
    experience = score(result.get("experienceMatch", 0))
    skills = score(result.get("skillsMatch", 0))
    education = score(result.get("educationMatch", 0))

    verdict = clean_display_text(result.get("verdict", "Analysis complete")) or "Analysis complete"
    summary = clean_display_text(result.get("summary", "No summary available.")) or "No summary available."

    recommendations = clean_list(result.get("recommendations", []))
    matched = clean_list(result.get("matchedSkills", []))
    missing = clean_list(result.get("missingSkills", []))

    insights = build_insights(match_score, experience, skills, education)

    st.divider()

    # ---------------- HERO ----------------
    render_html(
        f"""
        <div class="result-hero">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:2rem;flex-wrap:wrap;">
                <div style="flex:1;min-width:280px;">
                    <div style="font-size:.75rem;font-weight:800;letter-spacing:1.4px;color:#8b90a0;text-transform:uppercase;">AI MATCH REPORT</div>
                    <div style="font-family:'Plus Jakarta Sans';font-size:1.8rem;font-weight:800;color:#111827;margin-top:.4rem;">Candidate compatibility</div>
                    <div style="color:#6b7280;margin-top:.55rem;line-height:1.6;">Score and match metrics are read directly from your n8n + AI model workflow.</div>
                    <div class="verdict-pill">{html.escape(verdict)}</div>
                </div>
                <div style="width:190px;">
                    <div class="score-ring" style="--score:{match_score:.0f};">
                        <div class="score-inner">
                            <div class="score-value">{match_score:.0f}%</div>
                            <div class="score-caption">Match score</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    )

    # ---------------- BREAKDOWN ----------------
    render_html('<div class="section-title">Match Breakdown</div>')

    m1, m2, m3 = st.columns(3)
    metric_data = [
        ("Experience", experience, "💼"),
        ("Skills", skills, "🛠️"),
        ("Education", education, "🎓"),
    ]
    for col, (label, value, icon) in zip([m1, m2, m3], metric_data):
        with col:
            render_html(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{icon} {html.escape(label)}</div>
                    <div class="metric-value">{value:.0f}%</div>
                    <div class="mini-track"><div class="mini-fill" style="width:{value:.0f}%"></div></div>
                </div>
                """
            )

    # ---------------- ATS ----------------
    ats_score = score(result.get("atsScore", result.get("ATSScore", 0)))

    if ats_score > 0:
        render_html('<div class="section-title">ATS Compatibility</div>')
        st.progress(int(ats_score))
        st.caption(f"ATS Score: {ats_score:.0f}%")

    # ---------------- EXTRA ----------------
    critical_missing = clean_list(result.get("criticalMissingSkills", []))
    keyword_gaps = clean_list(result.get("keywordGaps", []))

    if critical_missing or keyword_gaps:
        extra1, extra2 = st.columns(2, gap="large")

        with extra1:
            if critical_missing:
                render_html('<div class="section-title">Critical Missing Skills</div>')
                for item in critical_missing:
                    render_html(f'<div class="insight-bad">{html.escape(item)}</div>')

        with extra2:
            if keyword_gaps:
                render_html('<div class="section-title">Keyword Gaps</div>')
                for item in keyword_gaps:
                    render_html(f'<div class="insight-warn">{html.escape(item)}</div>')

    # ---------------- TABS ----------------
    tab_overview, tab_actions, tab_interview, tab_export = st.tabs(
        ["Overview", "Action Plan", "Interview Prep", "Export"]
    )

    # ---- OVERVIEW ----
    with tab_overview:
        render_html('<div class="section-title">Executive Summary</div>')
        render_html(f'<div class="summary-card">{html.escape(summary)}</div>')

        st.write("")
        skills_col1, skills_col2 = st.columns(2, gap="large")

        with skills_col1:
            matched_html = "".join(
                f'<span class="skill-pill skill-match">{html.escape(item)}</span>' for item in matched
            ) or '<span class="small-muted">No matched skills were returned by n8n.</span>'

            render_html(
                f"""
                <div class="card">
                    <div style="font-weight:800;font-size:1rem;">✓ Matched Skills</div>
                    <div style="margin-top:.7rem;">{matched_html}</div>
                </div>
                """
            )

        with skills_col2:
            missing_html = "".join(
                f'<span class="skill-pill skill-missing">{html.escape(item)}</span>' for item in missing
            ) or '<span style="color:#047857;font-weight:700;">There are no missing skills</span>'

            render_html(
                f"""
                <div class="card">
                    <div style="font-weight:800;font-size:1rem;">⚠ Missing Skills</div>
                    <div style="margin-top:.7rem;">{missing_html}</div>
                </div>
                """
            )

        render_html('<div class="section-title">AI Insights</div>')

        css_map = {"good": "insight-good", "warn": "insight-warn", "bad": "insight-bad"}
        for kind, message in insights:
            render_html(f'<div class="{css_map.get(kind, "insight-warn")}">{html.escape(message)}</div>')

        strengths = clean_list(result.get("strengths", []))
        weaknesses = clean_list(result.get("weaknesses", []))
        tailored_summary = clean_display_text(result.get("tailoredSummary", ""))
        resume_improvements = clean_list(result.get("resumeImprovements", []))

        if strengths:
            render_html('<div class="section-title">Strengths</div>')
            for item in strengths:
                render_html(f'<div class="insight-good"><b>Strength:</b> {html.escape(item)}</div>')

        if weaknesses:
            render_html('<div class="section-title">Areas to Improve</div>')
            for item in weaknesses:
                render_html(f'<div class="insight-warn"><b>Improve:</b> {html.escape(item)}</div>')

        if tailored_summary:
            render_html('<div class="section-title">Tailored Summary</div>')
            render_html(f'<div class="summary-card">{html.escape(tailored_summary)}</div>')

        if resume_improvements:
            render_html('<div class="section-title">Resume Improvement Suggestions</div>')
            for idx, item in enumerate(resume_improvements, 1):
                render_html(rec_card_html(idx, item))

    # ---- ACTION PLAN ----
    with tab_actions:
        render_html('<div class="section-title">Recommended Action Plan</div>')

        if recommendations:
            for idx, item in enumerate(recommendations, 1):
                render_html(rec_card_html(idx, item))
        else:
            st.info("No recommendations were returned by the AI workflow.")

        render_html('<div class="section-title">Practical Next Steps</div>')

        priorities = []
        if skills < 70:
            priorities.append("Review the skills requirements and make your relevant skills more visible in the resume.")
        if experience < 70:
            priorities.append("Strengthen project or internship descriptions with concrete responsibilities and outcomes.")
        if education < 70:
            priorities.append("Present your education and qualifications clearly against the role requirements.")
        if not priorities:
            priorities.append("Tailor the wording of the resume to the job description and add measurable achievements where possible.")

        for idx, item in enumerate(priorities, 1):
            render_html(rec_card_html(idx, item))

    # ---- INTERVIEW PREP ----
    with tab_interview:
        render_html('<div class="section-title">Interview Preparation</div>')
        render_html(
            '<div class="small-muted">Starter questions based on the analysis. '
            'These questions do not require another API call.</div>'
        )

        ai_questions = clean_list(result.get("interviewQuestions", []))
        questions = ai_questions or create_interview_questions(matched=matched, missing=missing)

        for idx, question in enumerate(questions[:12], 1):
            render_html(rec_card_html(idx, question))

    # ---- EXPORT ----
    with tab_export:
        render_html('<div class="section-title">Export Report</div>')

        report_html = make_html_report(result, st.session_state.resume_name)

        st.download_button(
            "Download Report",
            data=report_html,
            file_name="resumeiq_report.html",
            mime="text/html",
            use_container_width=True,
        )

    # ---------------- DEBUG ----------------
    with st.expander("Developer: View n8n Response"):
        st.json(result)

    render_html(
        '<div style="text-align:center;color:#9ca3af;font-size:.75rem;margin-top:2.5rem;">'
        'ResumeIQ · Streamlit + n8n Cloud + AI Agent</div>'
    )