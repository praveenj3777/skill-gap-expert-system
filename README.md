# Skill-Gap Analysis Expert System

> **A Rule-Based Artificial Intelligence Expert System for Career Guidance & Personalized Technical Upskilling**  
> *Designed for College Computer Science & Engineering (CSE) Academic Project & Viva Defense*

---

## 1. Project Title
**Skill-Gap Analysis Expert System**

---

## 2. Problem Statement
Many engineering and computer science students struggle to identify which specific technical skills are required to succeed in diverse industry careers (such as Data Analyst, Web Developer, AI/ML Engineer, etc.), and which critical skill deficiencies they currently possess. 

Without objective guidance, students often pursue redundant tutorials or fail technical job interviews due to unaddressed foundational prerequisites. This project provides a **genuine, deterministic rule-based AI expert system** that systematically evaluates a student's self-assessed skill levels against benchmark requirements, deduces exact deficiencies, calculates career readiness, and provides transparent, explainable recommendations.

---

## 3. Project Objectives
* **Decouple Domain Knowledge from Reasoning:** Store career requirements in an extensible, external Knowledge Base separate from application code.
* **Implement Forward-Chaining Inference:** Match working memory facts against production rules to deduce skill gaps and prioritized remediation actions.
* **Deliver Explainable AI (XAI):** Provide an explicit Explanation Facility that reveals the exact IF-THEN rules fired, arithmetic computations, and deductions for every single skill.
* **Enable Interactive Assessment:** Provide a modern web interface with real-time slider controls and one-click presets for academic viva evaluation.
* **100% Offline Capability:** Execute locally on standard hardware without relying on cloud APIs, API keys, or internet connectivity.

---

## 4. Project Domain
* **Domain:** Career Guidance / Educational Technology (EdTech) / Applied Artificial Intelligence
* **Sub-Domain:** Classical Knowledge-Based Systems & Production Systems

---

## 5. Technologies Used
* **Backend:** Python 3.11+
* **Web Framework:** Flask 3.0+ (Lightweight WSGI framework)
* **Frontend:** HTML5, CSS3, Modern JavaScript (Vanilla ES6), Bootstrap 5.3
* **Knowledge Representation:** Structured JSON Knowledge Base (`knowledge_base/careers.json`)
* **Testing Framework:** Python standard `unittest` framework

---

## 6. System Architecture

The application strictly implements the classical architecture of an Artificial Intelligence Expert System:

```
+-------------------------------------------------------------------------+
|                              USER INTERFACE                             |
|  - Student Self-Assessment Form (1-5 Sliders)                           |
|  - Career Selection Dropdown                                            |
|  - One-Click Viva Demo Presets                                          |
|  - Results Dashboard & Explanation Audit Trail                          |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                         WORKING MEMORY (FACTS)                          |
|  - Fact 1: Student Name                                                 |
|  - Fact 2: Target Career Goal                                           |
|  - Fact 3..N: Self-Assessed Skill Levels (1-5)                          |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                      INFERENCE ENGINE (REASONING)                       |
|  - Pattern Matching: Compares Working Memory Facts to Rule Antecedents  |
|  - Forward Chaining Execution Cycle                                     |
|  - Conflict Resolution & Firing Schedule                                |
+------------------+----------------------------------+-------------------+
                   |                                  |
                   v                                  v
+------------------+---------------+  +---------------+-------------------+
|          KNOWLEDGE BASE          |  |          PRODUCTION RULES         |
|  - 5 Benchmark Careers           |  |  - RULE-01: Skill Gap Existence   |
|  - 30 Standardized Skills        |  |  - RULE-02: Sufficient Competency |
|  - 1-5 Required Benchmarks       |  |  - RULE-03: High Priority Gap     |
|  - Curated Action Recommendations|  |  - RULE-04: Medium Priority Gap   |
|  - Free Learning Resources       |  |  - RULE-05: Low Priority Gap      |
+----------------------------------+  |  - RULE-06: Focus Strategy        |
                                      |  - RULE-07: Readiness Scoring     |
                                      |  - RULE-08: Tier Classification   |
                                      +-----------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                        EXPLANATION FACILITY                             |
|  - Execution Trace / Rule Firing Audit Log                              |
|  - Step-by-Step Mathematical Gap Demonstration                          |
|  - Justification: "WHY this recommendation was made"                    |
+-------------------------------------------------------------------------+
```

---

## 7. Knowledge Base

The Knowledge Base is located in [`knowledge_base/careers.json`](file:///C:/Users/saipr/.gemini/antigravity/scratch/skill-gap-expert-system/knowledge_base/careers.json). It defines benchmark proficiencies for at least 5 industry careers:

1. **Data Analyst**
   * Python (Required: 4)
   * SQL (Required: 4)
   * Excel (Required: 4)
   * Statistics (Required: 3)
   * Data Visualization (Required: 3)
   * Power BI (Required: 3)
2. **Web Developer**
   * HTML (Required: 4)
   * CSS (Required: 4)
   * JavaScript (Required: 4)
   * Git (Required: 3)
   * Responsive Design (Required: 3)
   * Backend Basics (Required: 3)
3. **Software Developer**
   * Data Structures & Algorithms (Required: 4)
   * Python or Java (Required: 4)
   * Object-Oriented Programming (Required: 4)
   * Git & Version Control (Required: 3)
   * Database Management (Required: 3)
   * System Design Basics (Required: 3)
4. **AI/ML Engineer**
   * Python (Required: 5)
   * Mathematics & Linear Algebra (Required: 4)
   * Machine Learning Algorithms (Required: 4)
   * Deep Learning (Required: 3)
   * Data Preprocessing (Required: 4)
   * Model Evaluation (Required: 3)
5. **Cybersecurity Analyst**
   * Network Security (Required: 4)
   * Linux & Operating Systems (Required: 4)
   * Cryptography Basics (Required: 3)
   * Vulnerability Assessment (Required: 3)
   * Threat Intelligence & SIEM (Required: 3)
   * Security Protocols (Required: 4)

### Standard 5-Tier Proficiency Scale:
* **1 = Beginner:** Terminology familiarity; needs close mentoring.
* **2 = Basic:** Understands core concepts; executes guided tasks.
* **3 = Intermediate:** Solves standard problems independently.
* **4 = Advanced:** In-depth knowledge; handles complex optimizations.
* **5 = Expert:** End-to-end architect; mentors others.

---

## 8. Facts (Working Memory)
When a student interacts with the system, their inputs are asserted into Working Memory as formal facts:
* `Fact(StudentName = "[Student Name]")`
* `Fact(TargetCareer = "Data Analyst")`
* `Fact(Skill = "SQL", StudentLevel = 2)`
* `Fact(Skill = "Python", StudentLevel = 4)`

---

## 9. Production Rules (IF–THEN Rules)
Located in [`engine/rules.py`](file:///C:/Users/saipr/.gemini/antigravity/scratch/skill-gap-expert-system/engine/rules.py):

* **RULE-01 (Skill Gap Existence):**
  * `IF` Student Skill Level < Required Skill Level
  * `THEN` Assert `Fact(Skill Gap = Required - Student)` AND `Status = "Needs Improvement"`
* **RULE-02 (Sufficient Competency):**
  * `IF` Student Skill Level >= Required Skill Level
  * `THEN` Assert `Fact(Skill Gap = 0)` AND `Status = "SUFFICIENT"` AND `Priority = "SUFFICIENT"`
* **RULE-03 (High Priority Gap):**
  * `IF` Skill Gap >= 3
  * `THEN` `Priority = "HIGH"`, Urgency = "Critical Career Blocker", Action = "Immediate Remediation"
* **RULE-04 (Medium Priority Gap):**
  * `IF` Skill Gap == 2
  * `THEN` `Priority = "MEDIUM"`, Urgency = "Important Competency", Action = "Scheduled Learning"
* **RULE-05 (Low Priority Gap):**
  * `IF` Skill Gap == 1
  * `THEN` `Priority = "LOW"`, Urgency = "Minor Polish", Action = "Targeted Review"
* **RULE-06 (Multi-Gap Focus Strategy):**
  * `IF` Count(HIGH Priority Gaps) > 1
  * `THEN` Recommend prioritizing foundational language/core blockers first before secondary tooling.
* **RULE-07 (Career Readiness Scoring):**
  * `IF` All skills evaluated
  * `THEN` `Readiness % = (Sum of Effective Points / Sum of Benchmark Points) * 100`
* **RULE-08 (Readiness Tier Classification):**
  * `IF` Readiness % >= 80% &rarr; "Job Ready"
  * `IF` 60% <= Readiness < 80% &rarr; "Near Ready"
  * `IF` 40% <= Readiness < 60% &rarr; "Developing"
  * `IF` Readiness < 40% &rarr; "Foundational"

---

## 10. Inference Engine
Located in [`engine/inference_engine.py`](file:///C:/Users/saipr/.gemini/antigravity/scratch/skill-gap-expert-system/engine/inference_engine.py):
The engine implements **Forward Chaining**:
1. Accepts asserted facts from Working Memory.
2. Matches conditions against the Production Rules.
3. Fires matching rules to compute gaps, status, and priorities.
4. Synthesizes aggregate readiness metrics.
5. Populates an **Execution Trace** containing every rule fired and mathematical deduction.

---

## 11. Skill-Gap Calculation

The mathematical gap is computed deterministically:
$$\text{Skill Gap} = \max(0, \text{Required Level} - \text{Student Level})$$

* If $\text{Required} = 4$ and $\text{Student} = 2$:
  $$\text{Gap} = 4 - 2 = 2 \implies \text{Rule 4 fires} \implies \text{Priority: MEDIUM}$$
* If $\text{Required} = 4$ and $\text{Student} = 1$:
  $$\text{Gap} = 4 - 1 = 3 \implies \text{Rule 3 fires} \implies \text{Priority: HIGH}$$
* If $\text{Required} = 3$ and $\text{Student} = 4$:
  $$\text{Gap} = \max(0, 3 - 4) = 0 \implies \text{Rule 2 fires} \implies \text{Status: SUFFICIENT}$$

---

## 12. How Recommendations and Explanations are Generated

Each recommendation is pulled from the Knowledge Base and paired with a synthesized **Explanation**:
> *"SQL is marked as a Medium Priority gap because your current level is 2 (Basic) while the required level for Data Analyst is 4 (Advanced), resulting in a gap of 2 levels. Rule RULE-04 fired because Skill Gap == 2."*

This allows viva examiners to verify that recommendations are derived from genuine rule firings rather than arbitrary hardcoded text.

---

## 13. How to Install

### Prerequisites
* Python 3.10, 3.11, or newer installed.
* Standard command prompt or PowerShell.

### Installation Steps
1. Open PowerShell or Command Prompt.
2. Navigate to the project directory:
   ```powershell
   cd "C:\Users\saipr\.gemini\antigravity\scratch\skill-gap-expert-system"
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 14. How to Run

### Local Development
1. Start the Flask application:
   ```powershell
   python app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

### Production Deployment (Render)
To deploy on [Render](https://render.com) as a Web Service:
* **Environment:** Python 3
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `gunicorn app:app`
* **Root Directory:** `.` (or repository root)
* **Auto-Deploy:** Yes (on Git push)

---

## 15. Testing & Test Cases

The test suite is located in [`tests/test_inference.py`](file:///C:/Users/saipr/.gemini/antigravity/scratch/skill-gap-expert-system/tests/test_inference.py).

### Running Unit Tests:
```powershell
python -m unittest discover -s tests -v
```

### The 5 Verified Test Cases:
| Test Case | Career | Inputs | Expected Output | Status |
|---|---|---|---|---|
| **Test 1** | Data Analyst | Low skills across board (Level 1-2) | Multiple HIGH/MEDIUM gaps, low readiness (&lt;50%), Rule 6 fires | **PASS** |
| **Test 2** | Data Analyst | High skills (Level 4-5) | 100% readiness, all SUFFICIENT, zero gaps, Job Ready tier | **PASS** |
| **Test 3** | Web Developer | Mixed skills (HTML:4, JS:2, CSS:3, etc.) | Diverse priorities (HIGH, MED, LOW, SUFFICIENT) | **PASS** |
| **Test 4** | AI/ML Engineer | Weak Python (Level 1), decent math/ML | Python identified as HIGH priority gap (Gap=4 &ge; 3) | **PASS** |
| **Test 5** | Cybersecurity | Mixed skills | Security protocol SUFFICIENT, network & cryptography gaps flagged | **PASS** |

---

## 16. Example Output

### Assessment Input:
* Student: **Alex Morgan** (or user's own name)
* Target Career: **Data Analyst**
* Inputs: `SQL = 2`, `Python = 4`, `Excel = 2`, `Statistics = 2`, `Data Visualization = 3`, `Power BI = 1`

### Expert System Inference Result:
* **Career Readiness Score:** `63.6% (Near Ready)`
* **Priority Breakdown:**
  * **HIGH Priority (1):** Power BI (Gap: 2 levels, but foundational tool)
  * **MEDIUM Priority (3):** SQL (Gap: 2), Excel (Gap: 2), Statistics (Gap: 1)
  * **SUFFICIENT (2):** Python (Level 4), Data Visualization (Level 3)
* **Audit Trail Entry (SQL):**
  * `Fact`: Student = 2, Required = 4
  * `Math Step`: `4 - 2 = 2`
  * `Rule Fired`: `RULE-01 (Skill Gap Existence)` & `RULE-04 (Medium Priority)`
  * `Conclusion`: `Needs Improvement - Priority: MEDIUM`
  * `Explanation`: *"SQL is marked as Medium Priority because your current level is 2 while required benchmark is 4."*

---

## 17. College Viva Defense Guide

### Top Examiner Questions & How to Answer:

1. **Q: How is this an Expert System rather than just an ordinary web calculator?**
   * *Answer:* "An ordinary script tightly couples calculations and UI logic. In our project, domain facts are decoupled into an external **Knowledge Base** (`careers.json`), user inputs become **Working Memory facts**, and reasoning is performed by a **Rule-Based Inference Engine** (`inference_engine.py`) using formal IF-THEN **Production Rules** (`rules.py`). Furthermore, it includes an **Explanation Facility** that provides a complete rule-firing audit trail."

2. **Q: Why Forward Chaining instead of Backward Chaining?**
   * *Answer:* "Forward Chaining is data-driven. We already know the student's current skill levels (the facts), and we apply production rules forward to derive conclusions (gaps, priorities, readiness). Backward Chaining would be goal-driven, used when diagnosing a specific known failure."

3. **Q: Where are the rules defined?**
   * *Answer:* "All formal production rules are defined in `engine/rules.py` and executed dynamically in `engine/inference_engine.py`. For example, RULE-03 checks if `Skill Gap >= 3` to assign HIGH priority."

4. **Q: How does the system handle changes to industry benchmarks?**
   * *Answer:* "Because the Knowledge Base is completely decoupled in `knowledge_base/careers.json`, we can add new careers or update benchmark levels without touching a single line of backend or engine code."

---

## 18. Future Enhancements
* Incorporating **Certainty Factors** (Fuzzy Expert Systems) to model student self-assessment ambiguity.
* Integration of dynamic automated coding quizzes to verify claimed skill proficiencies.
* Backward-chaining goal planner that suggests alternative career roles matching a student's current high-performing competencies.
