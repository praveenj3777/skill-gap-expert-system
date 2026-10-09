"""
test_inference.py - Comprehensive Unit Tests for Skill-Gap Expert System.

Verifies the 5 core test cases required by the specification, plus rule execution,
inference tracing, and explainability verification.
"""

import unittest
import os
import sys

# Ensure parent directory is in python search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.inference_engine import SkillGapInferenceEngine


class TestSkillGapExpertSystem(unittest.TestCase):
    """Test suite verifying expert system rules, gap calculations, and explainability."""

    @classmethod
    def setUpClass(cls):
        cls.engine = SkillGapInferenceEngine()

    def test_knowledge_base_loading(self):
        """Verifies that the knowledge base loads with at least 5 careers and valid schema."""
        careers = self.engine.get_careers()
        self.assertGreaterEqual(len(careers), 5)
        expected_careers = ["data_analyst", "web_developer", "software_developer", "ai_ml_engineer", "cybersecurity_analyst"]
        for c in expected_careers:
            self.assertIn(c, careers, f"Career '{c}' must exist in knowledge base")
            self.assertGreater(len(careers[c]["skills"]), 0, f"Career '{c}' must have defined skills")

    def test_case_1_data_analyst_low_skills(self):
        """
        Test Case 1: Data Analyst + mostly low skills.
        Expected: Multiple skill gaps with appropriate priorities (HIGH, MEDIUM),
        readiness percentage is low (tier = Foundational or Developing).
        """
        student_name = "Alice (Beginner)"
        student_skills = {
            "Python": 1,              # Required: 4 -> Gap = 3 -> HIGH
            "SQL": 1,                 # Required: 4 -> Gap = 3 -> HIGH
            "Excel": 2,               # Required: 4 -> Gap = 2 -> MEDIUM
            "Statistics": 1,          # Required: 3 -> Gap = 2 -> MEDIUM
            "Data Visualization": 1,  # Required: 3 -> Gap = 2 -> MEDIUM
            "Power BI": 1             # Required: 3 -> Gap = 2 -> MEDIUM
        }

        result = self.engine.analyze(student_name, "data_analyst", student_skills)

        # Assertions
        self.assertEqual(result["career_id"], "data_analyst")
        self.assertGreater(result["counts"]["high"], 0, "Should have at least one HIGH priority gap")
        self.assertGreater(result["counts"]["medium"], 0, "Should have MEDIUM priority gaps")
        self.assertLess(result["readiness_percentage"], 50.0, "Readiness should be low for all-low skills")
        self.assertIn("RULE-06", result["focus_strategy"]["rule_fired"], "Multi-gap focus rule should fire")

        # Verify specific gap priorities
        skills_map = {item["skill"]: item for item in result["skills_analysis"]}
        self.assertEqual(skills_map["Python"]["gap"], 3)
        self.assertEqual(skills_map["Python"]["priority"], "HIGH")
        self.assertEqual(skills_map["SQL"]["gap"], 3)
        self.assertEqual(skills_map["SQL"]["priority"], "HIGH")
        self.assertEqual(skills_map["Excel"]["gap"], 2)
        self.assertEqual(skills_map["Excel"]["priority"], "MEDIUM")

    def test_case_2_data_analyst_high_skills(self):
        """
        Test Case 2: Data Analyst + high skills.
        Expected: High career readiness (100% or close), tier = Job Ready,
        all skills SUFFICIENT, zero high or medium gaps.
        """
        student_name = "Bob (Expert)"
        student_skills = {
            "Python": 5,              # Required: 4 -> Gap = 0 -> SUFFICIENT
            "SQL": 5,                 # Required: 4 -> Gap = 0 -> SUFFICIENT
            "Excel": 4,               # Required: 4 -> Gap = 0 -> SUFFICIENT
            "Statistics": 4,          # Required: 3 -> Gap = 0 -> SUFFICIENT
            "Data Visualization": 4,  # Required: 3 -> Gap = 0 -> SUFFICIENT
            "Power BI": 4             # Required: 3 -> Gap = 0 -> SUFFICIENT
        }

        result = self.engine.analyze(student_name, "data_analyst", student_skills)

        # Assertions
        self.assertEqual(result["readiness_percentage"], 100.0)
        self.assertEqual(result["readiness_tier"], "Job Ready")
        self.assertEqual(result["counts"]["high"], 0)
        self.assertEqual(result["counts"]["medium"], 0)
        self.assertEqual(result["counts"]["low"], 0)
        self.assertEqual(result["counts"]["sufficient"], 6)
        self.assertEqual(len(result["recommendations"]), 0)

        # Verify every skill received SUFFICIENT status
        for item in result["skills_analysis"]:
            self.assertEqual(item["gap"], 0)
            self.assertEqual(item["status"], "SUFFICIENT")
            self.assertEqual(item["priority"], "SUFFICIENT")

    def test_case_3_web_developer_mixed_skills(self):
        """
        Test Case 3: Web Developer + mixed skills.
        Expected: Mixed gaps spanning High, Medium, Low, and Sufficient.
        """
        student_name = "Charlie (Mixed)"
        student_skills = {
            "HTML": 4,               # Required: 4 -> Gap = 0 -> SUFFICIENT
            "CSS": 3,                # Required: 4 -> Gap = 1 -> LOW
            "JavaScript": 2,         # Required: 4 -> Gap = 2 -> MEDIUM
            "Git": 3,                # Required: 3 -> Gap = 0 -> SUFFICIENT
            "Responsive Design": 1,  # Required: 3 -> Gap = 2 -> MEDIUM
            "Backend Basics": 1      # Required: 3 -> Gap = 2 -> MEDIUM
        }

        result = self.engine.analyze(student_name, "web_developer", student_skills)

        # Assertions
        self.assertEqual(result["career_id"], "web_developer")
        self.assertGreater(result["counts"]["sufficient"], 0)
        self.assertGreater(result["counts"]["medium"], 0)
        self.assertGreater(result["counts"]["low"], 0)

        skills_map = {item["skill"]: item for item in result["skills_analysis"]}
        self.assertEqual(skills_map["HTML"]["status"], "SUFFICIENT")
        self.assertEqual(skills_map["CSS"]["priority"], "LOW")
        self.assertEqual(skills_map["CSS"]["gap"], 1)
        self.assertEqual(skills_map["JavaScript"]["priority"], "MEDIUM")
        self.assertEqual(skills_map["JavaScript"]["gap"], 2)

    def test_case_4_aiml_weak_python(self):
        """
        Test Case 4: AI/ML Engineer + weak Python.
        Expected: Python identified as major HIGH priority gap (Req: 5, Stud: 1 -> Gap: 4 >= 3).
        """
        student_name = "Diana (AI Aspirant)"
        student_skills = {
            "Python": 1,                         # Required: 5 -> Gap = 4 -> HIGH
            "Mathematics & Linear Algebra": 4,   # Required: 4 -> Gap = 0 -> SUFFICIENT
            "Machine Learning Algorithms": 3,    # Required: 4 -> Gap = 1 -> LOW
            "Deep Learning": 2,                  # Required: 3 -> Gap = 1 -> LOW
            "Data Preprocessing": 3,             # Required: 4 -> Gap = 1 -> LOW
            "Model Evaluation": 3                # Required: 3 -> Gap = 0 -> SUFFICIENT
        }

        result = self.engine.analyze(student_name, "ai_ml_engineer", student_skills)

        # Assertions
        skills_map = {item["skill"]: item for item in result["skills_analysis"]}
        self.assertIn("Python", skills_map)
        self.assertEqual(skills_map["Python"]["gap"], 4)
        self.assertEqual(skills_map["Python"]["priority"], "HIGH")
        self.assertIn("Python", result["focus_strategy"]["primary_focus"])

    def test_case_5_cybersecurity_mixed_skills(self):
        """
        Test Case 5: Cybersecurity Analyst + mixed skill levels.
        Expected: Cybersecurity-specific gaps identified with appropriate priorities.
        """
        student_name = "Evan (Cyber Sec Student)"
        student_skills = {
            "Network Security": 2,            # Required: 4 -> Gap = 2 -> MEDIUM
            "Linux & Operating Systems": 3,   # Required: 4 -> Gap = 1 -> LOW
            "Cryptography Basics": 1,         # Required: 3 -> Gap = 2 -> MEDIUM
            "Vulnerability Assessment": 1,    # Required: 3 -> Gap = 2 -> MEDIUM
            "Threat Intelligence & SIEM": 2,  # Required: 3 -> Gap = 1 -> LOW
            "Security Protocols": 4           # Required: 4 -> Gap = 0 -> SUFFICIENT
        }

        result = self.engine.analyze(student_name, "cybersecurity_analyst", student_skills)

        # Assertions
        self.assertEqual(result["career_id"], "cybersecurity_analyst")
        skills_map = {item["skill"]: item for item in result["skills_analysis"]}
        self.assertEqual(skills_map["Network Security"]["priority"], "MEDIUM")
        self.assertEqual(skills_map["Linux & Operating Systems"]["priority"], "LOW")
        self.assertEqual(skills_map["Security Protocols"]["status"], "SUFFICIENT")
        self.assertEqual(result["counts"]["sufficient"], 1)

    def test_inference_trace_and_explanation_soundness(self):
        """
        Verifies that every skill produces an audit trace with:
        - Math step
        - Rules fired
        - Conclusion
        - Human-readable explainability justification
        """
        student_skills = {"SQL": 2, "Python": 4, "Excel": 1, "Statistics": 3, "Data Visualization": 3, "Power BI": 2}
        result = self.engine.analyze("Test Student", "data_analyst", student_skills)

        trace = result["inference_trace"]
        self.assertEqual(len(trace), 6, "Each required skill must produce an inference trace entry")

        # Locate SQL trace
        sql_trace = next(t for t in trace if t["skill"] == "SQL")
        self.assertIn("4 (Required) - 2 (Student) = 2", sql_trace["math_step"])
        self.assertIn("RULE-01", sql_trace["rules_fired"])
        self.assertIn("RULE-04", sql_trace["rules_fired"])
        self.assertIn("Priority: MEDIUM", sql_trace["conclusion"])
        self.assertIn("Rule RULE-04 fired", sql_trace["explanation"])


if __name__ == "__main__":
    unittest.main()
