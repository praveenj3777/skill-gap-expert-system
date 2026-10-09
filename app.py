"""
app.py - Main Flask Application for Skill-Gap Analysis Expert System.

Integrates the Knowledge Base, Forward-Chaining Inference Engine, and
Explainable Web Interface. Runs 100% locally with zero external API dependencies.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from engine.inference_engine import SkillGapInferenceEngine
from engine.rules import PROFICIENCY_LABELS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "skill-gap-expert-system-viva-secret-key")

# Instantiate the Expert System Inference Engine
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_FILE = os.path.join(BASE_DIR, "knowledge_base", "careers.json")
engine = SkillGapInferenceEngine(kb_path=KB_FILE)

# In-memory storage for latest session result (for easy display and demo)
latest_analysis = {}


@app.route("/")
def index():
    """Home landing page explaining the Expert System architecture and core flow."""
    careers = engine.get_careers()
    rules = engine.get_system_rules()
    return render_template(
        "index.html",
        career_count=len(careers),
        rule_count=len(rules),
        careers=careers
    )


@app.route("/assessment")
def assessment():
    """Interactive assessment page where students input name, select career, and rate skills."""
    careers = engine.get_careers()
    return render_template(
        "assessment.html",
        careers=careers,
        proficiency_scale=PROFICIENCY_LABELS
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Receives student inputs, executes the forward-chaining inference engine,
    and returns or displays the explainable results dashboard.
    """
    global latest_analysis

    # Support both JSON requests and HTML form submissions
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    student_name = data.get("student_name", "Student").strip()
    if not student_name:
        student_name = "Student"

    career_id = data.get("career_id", "data_analyst")

    # Extract skill ratings
    student_skills = {}
    career_spec = engine.get_career_details(career_id)

    for skill_name in career_spec["skills"].keys():
        # Field may be named like "skill_Python" or directly "Python"
        val = data.get(f"skill_{skill_name}", data.get(skill_name, 1))
        try:
            student_skills[skill_name] = int(val)
        except (ValueError, TypeError):
            student_skills[skill_name] = 1

    # Execute Forward-Chaining Inference
    analysis_result = engine.analyze(student_name, career_id, student_skills)
    latest_analysis = analysis_result

    if request.is_json:
        return jsonify(analysis_result)

    return render_template(
        "results.html",
        result=analysis_result,
        proficiency_scale=PROFICIENCY_LABELS
    )


@app.route("/results")
def results():
    """Direct results page display. If no recent analysis exists, redirects to assessment."""
    global latest_analysis
    if not latest_analysis:
        return redirect(url_for("assessment"))

    return render_template(
        "results.html",
        result=latest_analysis,
        proficiency_scale=PROFICIENCY_LABELS
    )


@app.route("/knowledge-base")
def knowledge_base():
    """Knowledge Base explorer displaying all careers, required skills, and recommendations."""
    careers = engine.get_careers()
    return render_template(
        "knowledge_base.html",
        careers=careers,
        proficiency_scale=PROFICIENCY_LABELS
    )


@app.route("/how-it-works")
@app.route("/rules")
def rules_page():
    """How It Works & Production Rules viewer explaining inference cycles."""
    rules = engine.get_system_rules()
    return render_template(
        "rules.html",
        rules=rules,
        proficiency_scale=PROFICIENCY_LABELS
    )


# --- REST API Endpoints for Frontend Dynamic Interactions ---

@app.route("/api/careers")
def api_careers():
    """Returns JSON listing of all careers and their skills."""
    return jsonify({
        "status": "success",
        "careers": engine.get_careers(),
        "proficiency_scale": PROFICIENCY_LABELS
    })


@app.route("/api/rules")
def api_rules():
    """Returns JSON listing of all production rules."""
    return jsonify({
        "status": "success",
        "rules": engine.get_system_rules()
    })


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Offline Rule-Based Query Assistant (Chatbot).
    Processes user questions against the Knowledge Base and latest inference results.
    100% offline, deterministic, and educational.
    """
    global latest_analysis
    data = request.get_json() or {}
    message = data.get("message", "").strip().lower()

    if not message:
        return jsonify({"reply": "Please enter a question regarding career skills, gap analysis, or inference rules."})

    careers = engine.get_careers()

    # Query 1: What skills do I need for <career>?
    for cid, cinfo in careers.items():
        cname_lower = cinfo["name"].lower()
        if cname_lower in message or cid in message:
            skills_list = [f"• <b>{s}</b>: Level {spec['required_level']} ({PROFICIENCY_LABELS.get(spec['required_level'])})" for s, spec in cinfo["skills"].items()]
            skills_str = "<br>".join(skills_list)
            return jsonify({
                "reply": f"For <b>{cinfo['name']}</b>, the Knowledge Base requires the following proficiencies:<br><br>{skills_str}"
            })

    # Query 2: Biggest skill gap
    if "biggest" in message or "largest" in message or "top gap" in message:
        if latest_analysis and latest_analysis.get("recommendations"):
            top = latest_analysis["recommendations"][0]
            return jsonify({
                "reply": f"Based on your latest assessment for <b>{latest_analysis['career_name']}</b>, your largest gap is in <b>{top['skill']}</b> with a gap of <b>{top['gap']} levels</b> (Current: {top['student_level']}, Required: {top['required_level']}). Priority: <b>{top['priority']}</b>.<br><br><b>Recommendation:</b> {top['learning_recommendation']}"
            })
        else:
            return jsonify({
                "reply": "No assessment has been run yet. Please complete the <a href='/assessment'>Skill Assessment</a> first so I can identify your largest skill gap!"
            })

    # Query 3: How to improve specific skill (e.g., SQL, Python, Excel, etc.)
    all_known_skills = {}
    for c in careers.values():
        for sk, spec in c["skills"].items():
            all_known_skills[sk.lower()] = (sk, spec)

    for sk_lower, (sk_formal, spec) in all_known_skills.items():
        if sk_lower in message:
            resources_str = ", ".join(spec.get("resources", []))
            return jsonify({
                "reply": f"<b>How to improve {sk_formal}:</b><br><br>{spec['recommendation']}<br><br><b>Recommended Resources:</b> {resources_str}"
            })

    # Query 4: Explain rules or priority
    if "rule" in message or "priority" in message or "how it works" in message:
        return jsonify({
            "reply": "The Expert System uses IF-THEN rules:<br>• <b>Rule 1:</b> IF Student &lt; Required THEN Gap exists.<br>• <b>Rule 3:</b> IF Gap &ge; 3 THEN Priority = HIGH.<br>• <b>Rule 4:</b> IF Gap == 2 THEN Priority = MEDIUM.<br>• <b>Rule 5:</b> IF Gap == 1 THEN Priority = LOW.<br>• <b>Rule 2:</b> IF Gap == 0 THEN Status = SUFFICIENT.<br>Visit the <a href='/rules'>Inference Rules</a> page to inspect the complete formal rule set."
        })

    # Default fallback response
    return jsonify({
        "reply": "I can help with questions like:<br>"
                 "• <i>'What skills do I need for Data Analyst?'</i><br>"
                 "• <i>'What is my biggest skill gap?'</i><br>"
                 "• <i>'How can I improve my SQL?'</i><br>"
                 "• <i>'How does the priority rule work?'</i>"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    print("\n" + "=" * 60)
    print("  SKILL-GAP ANALYSIS EXPERT SYSTEM")
    print(f"  Running on port {port} (debug={debug_mode})")
    print(f"  URL: http://127.0.0.1:{port}")
    print("=" * 60 + "\n")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
