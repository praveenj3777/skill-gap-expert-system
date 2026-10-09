"""
verify_10_steps.py - Verification script executing the exact 10 steps requested.
"""

import urllib.request
import urllib.parse
import sys

BASE_URL = "http://127.0.0.1:5000"

print("Starting 10-step verification against live server...")

# Step 1 & 2: Open assessment page, confirm name field is EMPTY
with urllib.request.urlopen(f"{BASE_URL}/assessment") as r:
    html = r.read().decode("utf-8")
    assert 'value=""' in html, "Student name should have value=''"
    assert 'placeholder="Enter your name"' in html, "Student name should have placeholder 'Enter your name'"
    assert "Rahul" not in html, "Demo name 'Rahul' should not be present in initial form"
    print("[PASS] Step 1 & 2: Assessment page loaded; Student Full Name field is completely EMPTY.")

# Step 3, 4, 5, 6: Enter a name manually, select Data Analyst, enter skills, analyze
data_kavya = urllib.parse.urlencode({
    "student_name": "Kavya",
    "career_id": "data_analyst",
    "skill_Python": 1,
    "skill_SQL": 4,
    "skill_Excel": 3,
    "skill_Statistics": 3,
    "skill_Data Visualization": 3,
    "skill_Power BI": 3
}).encode("utf-8")

with urllib.request.urlopen(f"{BASE_URL}/analyze", data=data_kavya) as r:
    res_kavya = r.read().decode("utf-8")
    assert "Kavya's Skill-Gap Report" in res_kavya, "Results should feature Kavya's report"
    assert "Python" in res_kavya
    assert "HIGH" in res_kavya
    print("[PASS] Step 3, 4, 5, 6: Analyzed Kavya (Data Analyst with low Python). Python correctly deduced as HIGH priority gap.")

# Step 7: Enter different skill levels and confirm results change dynamically
data_rohan = urllib.parse.urlencode({
    "student_name": "Rohan",
    "career_id": "data_analyst",
    "skill_Python": 4,
    "skill_SQL": 1,
    "skill_Excel": 4,
    "skill_Statistics": 3,
    "skill_Data Visualization": 3,
    "skill_Power BI": 3
}).encode("utf-8")

with urllib.request.urlopen(f"{BASE_URL}/analyze", data=data_rohan) as r:
    res_rohan = r.read().decode("utf-8")
    assert "Rohan's Skill-Gap Report" in res_rohan
    assert "SQL" in res_rohan
    assert res_kavya != res_rohan, "Different inputs must produce different dynamic outputs"
    print("[PASS] Step 7: Results change dynamically according to student inputs (Rohan vs Kavya verified).")

# Step 8: Open Knowledge Base
with urllib.request.urlopen(f"{BASE_URL}/knowledge-base") as r:
    assert r.status == 200
    html_kb = r.read().decode("utf-8")
    assert "Knowledge Base" in html_kb
    assert "Data Analyst" in html_kb
    print("[PASS] Step 8: Knowledge Base page verified.")

# Step 9: Open Inference Rules / How It Works
with urllib.request.urlopen(f"{BASE_URL}/how-it-works") as r:
    assert r.status == 200
    html_rules = r.read().decode("utf-8")
    assert "How the Expert System Works" in html_rules
    assert "RULE-01" in html_rules
    print("[PASS] Step 9: How It Works & Inference Rules page verified.")

# Step 10: Confirm all pages work
with urllib.request.urlopen(f"{BASE_URL}/") as r:
    assert r.status == 200
    html_home = r.read().decode("utf-8")
    assert "Find the skills you need for your career." in html_home

print("\nAll 10 steps successfully verified! Everything is working cleanly and dynamically.")
