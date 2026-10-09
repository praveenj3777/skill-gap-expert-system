"""
test_server.py - Integration and HTTP Verification Suite.

Tests all Flask endpoints, form submissions, JSON API inference, and offline chatbot.
"""

import urllib.request
import urllib.parse
import json
import unittest


class TestSkillGapServer(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"

    def test_homepage(self):
        with urllib.request.urlopen(f"{self.BASE_URL}/") as response:
            self.assertEqual(response.status, 200)
            html = response.read().decode("utf-8")
            self.assertIn("Find the skills you need for your career.", html)
            self.assertIn("Assess your current skills, discover your gaps", html)
            self.assertIn("Start Skill Assessment", html)
            self.assertIn("Explore Careers", html)

    def test_assessment_page_default_empty_name(self):
        with urllib.request.urlopen(f"{self.BASE_URL}/assessment") as response:
            self.assertEqual(response.status, 200)
            html = response.read().decode("utf-8")
            self.assertIn("Student Skill Assessment", html)
            self.assertIn('placeholder="Enter your name"', html)
            # Ensure name input is empty by default
            self.assertIn('value=""', html)
            self.assertNotIn('value="Rahul Sharma"', html)
            self.assertIn("Analyze My Skill Gap", html)

    def test_knowledge_base_page(self):
        with urllib.request.urlopen(f"{self.BASE_URL}/knowledge-base") as response:
            self.assertEqual(response.status, 200)
            html = response.read().decode("utf-8")
            self.assertIn("Knowledge Base", html)
            self.assertIn("Data Analyst", html)
            self.assertIn("AI/ML Engineer", html)

    def test_rules_and_how_it_works_page(self):
        # Test both /rules and /how-it-works
        for endpoint in ["/rules", "/how-it-works"]:
            with urllib.request.urlopen(f"{self.BASE_URL}{endpoint}") as response:
                self.assertEqual(response.status, 200)
                html = response.read().decode("utf-8")
                self.assertIn("How the Expert System Works", html)
                self.assertIn("RULE-01", html)
                self.assertIn("RULE-03", html)

    def test_api_careers(self):
        with urllib.request.urlopen(f"{self.BASE_URL}/api/careers") as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["status"], "success")
            self.assertIn("data_analyst", data["careers"])
            self.assertIn("web_developer", data["careers"])
            self.assertIn("software_developer", data["careers"])
            self.assertIn("ai_ml_engineer", data["careers"])
            self.assertIn("cybersecurity_analyst", data["careers"])

    def test_json_analyze_endpoint(self):
        payload = {
            "student_name": "Test User",
            "career_id": "data_analyst",
            "Python": 4,
            "SQL": 2,
            "Excel": 2,
            "Statistics": 3,
            "Data Visualization": 3,
            "Power BI": 1
        }
        req = urllib.request.Request(
            f"{self.BASE_URL}/analyze",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            result = json.loads(response.read().decode("utf-8"))
            self.assertEqual(result["student_name"], "Test User")
            self.assertEqual(result["career_name"], "Data Analyst")
            self.assertGreater(result["readiness_percentage"], 50)
            self.assertIn("inference_trace", result)
            self.assertIn("recommendations", result)

            # Check that SQL has gap 2 and medium priority
            sql_item = next(item for item in result["skills_analysis"] if item["skill"] == "SQL")
            self.assertEqual(sql_item["gap"], 2)
            self.assertEqual(sql_item["priority"], "MEDIUM")

    def test_form_submission_and_results_page(self):
        form_data = urllib.parse.urlencode({
            "student_name": "Priya",
            "career_id": "web_developer",
            "skill_HTML": 4,
            "skill_CSS": 3,
            "skill_JavaScript": 2,
            "skill_Git": 3,
            "skill_Responsive Design": 1,
            "skill_Backend Basics": 1
        }).encode("utf-8")
        req = urllib.request.Request(f"{self.BASE_URL}/analyze", data=form_data)
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            html = response.read().decode("utf-8")
            self.assertIn("Priya's Skill-Gap Report", html)
            self.assertIn("Why did the system recommend this?", html)
            self.assertIn("JavaScript", html)
            self.assertIn("RULE-01", html)

    def test_offline_chatbot(self):
        payload = {"message": "What skills do I need for Data Analyst?"}
        req = urllib.request.Request(
            f"{self.BASE_URL}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            res = json.loads(response.read().decode("utf-8"))
            self.assertIn("SQL", res["reply"])
            self.assertIn("Python", res["reply"])


if __name__ == "__main__":
    unittest.main()
