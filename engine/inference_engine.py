"""
inference_engine.py - Forward-Chaining Inference Engine for Skill-Gap Analysis.

This module implements a genuine Rule-Based Expert System inference engine.
It matches facts asserted in Working Memory against the Production Rules in the
Knowledge Base and outputs:
1. Working Memory facts & derived assertions
2. Skill-by-skill gap calculations & priority rankings
3. An explicit execution trace (audit log) showing which rules fired and why
4. Explainable career guidance and sequenced remediation recommendations
"""

import json
import os
from typing import Dict, Any, List
from .rules import PROFICIENCY_LABELS, SYSTEM_RULES


class SkillGapInferenceEngine:
    """Rule-Based Inference Engine implementing Forward Chaining pattern matching."""

    def __init__(self, kb_path: str = None):
        """Initialize the inference engine and load the Knowledge Base."""
        if kb_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            kb_path = os.path.join(base_dir, "knowledge_base", "careers.json")

        self.kb_path = kb_path
        self.knowledge_base = self._load_knowledge_base()
        self.rules = SYSTEM_RULES

    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Loads and parses the external JSON Knowledge Base."""
        if not os.path.exists(self.kb_path):
            raise FileNotFoundError(f"Knowledge Base file not found at: {self.kb_path}")
        with open(self.kb_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_careers(self) -> Dict[str, Any]:
        """Returns the dictionary of all careers from the Knowledge Base."""
        return self.knowledge_base.get("careers", {})

    def get_career_details(self, career_id: str) -> Dict[str, Any]:
        """Fetches detailed specifications for a single career."""
        careers = self.get_careers()
        if career_id not in careers:
            raise ValueError(f"Unknown career '{career_id}' requested.")
        return careers[career_id]

    def get_system_rules(self) -> List[Dict[str, Any]]:
        """Returns the list of production rules in dictionary format."""
        return [rule.to_dict() for rule in self.rules]

    def analyze(self, student_name: str, career_id: str, student_skills: Dict[str, int]) -> Dict[str, Any]:
        """
        Executes Forward Chaining Inference over the student's input skills.

        Process:
        1. Assert Facts: (Student Name, Career, Self-Assessed Skill Levels) into Working Memory.
        2. Match Antecedents against Production Rules for each required skill.
        3. Fire Matching Rules and deduce Skill Gap, Status, and Priority.
        4. Record each rule execution in the Inference Trace (Explanation Facility).
        5. Aggregate results into Career Readiness % and Sequenced Action Plan.
        """
        career = self.get_career_details(career_id)
        career_name = career["name"]
        career_desc = career["description"]
        required_skills = career["skills"]

        # Working Memory tracking
        working_memory_facts = [
            f"Fact 01: Student asserted name is '{student_name}'.",
            f"Fact 02: Target career goal asserted as '{career_name}'.",
        ]

        skills_analysis = []
        inference_trace = []
        recommendations = []

        priority_groups = {
            "HIGH": [],
            "MEDIUM": [],
            "LOW": [],
            "SUFFICIENT": []
        }

        total_required_points = 0
        total_effective_points = 0

        # Step 1: Forward Chaining on each skill required by the target career
        for skill_name, skill_spec in required_skills.items():
            req_level = int(skill_spec["required_level"])
            # Student level defaults to 1 (Beginner) if not provided
            raw_student_val = student_skills.get(skill_name, 1)
            try:
                stud_level = max(1, min(5, int(raw_student_val)))
            except (ValueError, TypeError):
                stud_level = 1

            total_required_points += req_level
            total_effective_points += min(stud_level, req_level)

            req_label = PROFICIENCY_LABELS.get(req_level, "Unknown")
            stud_label = PROFICIENCY_LABELS.get(stud_level, "Unknown")

            # Mathematical gap computation: Skill Gap = Required - Student
            raw_gap = req_level - stud_level
            skill_gap = max(0, raw_gap)

            working_memory_facts.append(
                f"Fact: Skill '{skill_name}' - Student Level = {stud_level} ({stud_label}), Required = {req_level} ({req_label})."
            )

            # Rule Pattern Matching & Firing
            fired_rules = []
            math_step = f"{req_level} (Required) - {stud_level} (Student) = {raw_gap}"

            if stud_level < req_level:
                # Rule 1 Fired
                status = "Needs Improvement"
                fired_rules.append({
                    "rule_id": "RULE-01",
                    "name": "Skill Gap Existence Rule",
                    "fired_condition": f"Student ({stud_level}) < Required ({req_level})",
                    "deduction": f"Identified skill gap of {skill_gap} levels."
                })

                # Determine Priority Rules
                if skill_gap >= 3:
                    priority = "HIGH"
                    priority_badge = "danger"
                    fired_rules.append({
                        "rule_id": "RULE-03",
                        "name": "High Priority Critical Gap Rule",
                        "fired_condition": f"Gap ({skill_gap}) >= 3",
                        "deduction": "Priority set to HIGH (Urgent Career Blocker)."
                    })
                    why_explanation = (
                        f"'{skill_name}' is marked as HIGH PRIORITY because your current level is {stud_level} ({stud_label}) "
                        f"while the required benchmark for {career_name} is {req_level} ({req_label}), producing a severe gap of {skill_gap} levels. "
                        f"Rule RULE-03 fired because Skill Gap >= 3."
                    )
                elif skill_gap == 2:
                    priority = "MEDIUM"
                    priority_badge = "warning"
                    fired_rules.append({
                        "rule_id": "RULE-04",
                        "name": "Medium Priority Moderate Gap Rule",
                        "fired_condition": f"Gap ({skill_gap}) == 2",
                        "deduction": "Priority set to MEDIUM (Important Competency)."
                    })
                    why_explanation = (
                        f"'{skill_name}' is marked as MEDIUM PRIORITY because your current level is {stud_level} ({stud_label}) "
                        f"while {career_name} requires {req_level} ({req_label}), creating a moderate gap of {skill_gap} levels. "
                        f"Rule RULE-04 fired because Skill Gap == 2."
                    )
                else:  # skill_gap == 1
                    priority = "LOW"
                    priority_badge = "info"
                    fired_rules.append({
                        "rule_id": "RULE-05",
                        "name": "Low Priority Minor Gap Rule",
                        "fired_condition": f"Gap ({skill_gap}) == 1",
                        "deduction": "Priority set to LOW (Minor Refinement Needed)."
                    })
                    why_explanation = (
                        f"'{skill_name}' is marked as LOW PRIORITY because you are currently level {stud_level} ({stud_label}) "
                        f"and the target is {req_level} ({req_label}). With only 1 level gap, this is easily bridgeable with focused review. "
                        f"Rule RULE-05 fired because Skill Gap == 1."
                    )
            else:
                # Rule 2 Fired (Sufficient)
                status = "SUFFICIENT"
                priority = "SUFFICIENT"
                priority_badge = "success"
                fired_rules.append({
                    "rule_id": "RULE-02",
                    "name": "Sufficient Competency Rule",
                    "fired_condition": f"Student ({stud_level}) >= Required ({req_level}) (Gap <= 0)",
                    "deduction": "Proficiency benchmark achieved or exceeded; no immediate gap."
                })
                why_explanation = (
                    f"'{skill_name}' is marked as SUFFICIENT because your current level {stud_level} ({stud_label}) "
                    f"meets or surpasses the required benchmark {req_level} ({req_label}) for {career_name}. "
                    f"Rule RULE-02 fired (Skill Gap = 0)."
                )

            # Store in Priority Group
            priority_groups[priority].append({
                "skill": skill_name,
                "current": stud_level,
                "required": req_level,
                "gap": skill_gap
            })

            # Append to Skill Analysis table
            skills_analysis.append({
                "skill": skill_name,
                "student_level": stud_level,
                "student_label": stud_label,
                "required_level": req_level,
                "required_label": req_label,
                "gap": skill_gap,
                "status": status,
                "priority": priority,
                "priority_badge": priority_badge,
                "description": skill_spec.get("description", "")
            })

            # Record in Inference Trace (Execution Log for Viva)
            rule_names_fired = ", ".join([f"{r['rule_id']} ({r['name']})" for r in fired_rules])
            inference_trace.append({
                "skill": skill_name,
                "student_level": f"{stud_level} ({stud_label})",
                "required_level": f"{req_level} ({req_label})",
                "math_step": math_step,
                "gap_result": skill_gap,
                "rules_fired": rule_names_fired,
                "rule_details": fired_rules,
                "conclusion": f"{status} - Priority: {priority}",
                "explanation": why_explanation
            })

            # Build recommendation item
            if status != "SUFFICIENT":
                recommendations.append({
                    "skill": skill_name,
                    "student_level": stud_level,
                    "student_label": stud_label,
                    "required_level": req_level,
                    "required_label": req_label,
                    "gap": skill_gap,
                    "priority": priority,
                    "priority_badge": priority_badge,
                    "importance": skill_spec.get("importance", "Core Essential"),
                    "learning_recommendation": skill_spec.get("recommendation", "Review and practice regularly."),
                    "resources": skill_spec.get("resources", []),
                    "why_explanation": why_explanation
                })

        # Step 2: Global Career Readiness Calculation (RULE-07)
        if total_required_points > 0:
            readiness_percentage = round((total_effective_points / total_required_points) * 100, 1)
        else:
            readiness_percentage = 0.0

        # Step 3: Global Career Readiness Classification (RULE-08)
        if readiness_percentage >= 80.0:
            readiness_tier = "Job Ready"
            readiness_color = "success"
            readiness_summary = "Excellent competency match! You meet or are very close to standard industry expectations."
        elif readiness_percentage >= 60.0:
            readiness_tier = "Near Ready"
            readiness_color = "info"
            readiness_summary = "Solid baseline! You can bridge the remaining gaps with targeted practice in key areas."
        elif readiness_percentage >= 40.0:
            readiness_tier = "Developing"
            readiness_color = "warning"
            readiness_summary = "Foundational knowledge present, but moderate upskilling is necessary before applying."
        else:
            readiness_tier = "Foundational"
            readiness_color = "danger"
            readiness_summary = "Significant skill gaps identified across multiple core areas; systematic guided training recommended."

        # Step 4: Multi-Gap Focus Strategy (RULE-06)
        high_priority_count = len(priority_groups["HIGH"])
        medium_priority_count = len(priority_groups["MEDIUM"])
        low_priority_count = len(priority_groups["LOW"])
        sufficient_count = len(priority_groups["SUFFICIENT"])

        focus_strategy = {}
        if high_priority_count > 1:
            high_skill_names = [item["skill"] for item in priority_groups["HIGH"]]
            focus_strategy = {
                "rule_fired": "RULE-06 (Multi-Gap Focus Strategy Rule)",
                "action": "Multiple critical gaps detected. We strongly advise focusing first on these high-priority blockers before moving on to moderate or minor improvements.",
                "primary_focus": high_skill_names,
                "strategy_note": "Target one high-priority skill at a time. Building competence in core languages/tools will accelerate learning secondary tools."
            }
        elif high_priority_count == 1:
            single_high = priority_groups["HIGH"][0]["skill"]
            focus_strategy = {
                "rule_fired": "RULE-03 (High Priority Focus)",
                "action": f"Single critical blocker identified: '{single_high}'. Prioritize this immediately.",
                "primary_focus": [single_high],
                "strategy_note": "Eliminating this single high-priority gap will substantially boost your interview readiness."
            }
        elif medium_priority_count > 0:
            medium_skill_names = [item["skill"] for item in priority_groups["MEDIUM"]]
            focus_strategy = {
                "rule_fired": "RULE-04 (Medium Priority Focus)",
                "action": "No critical blockers found. Advance your moderate gap skills to reach advanced proficiency.",
                "primary_focus": medium_skill_names,
                "strategy_note": "Engage in hands-on projects and real-world exercises to solidify intermediate abilities into advanced mastery."
            }
        else:
            focus_strategy = {
                "rule_fired": "RULE-02 (Competency Attainment)",
                "action": "All required skills meet or exceed benchmark standards!",
                "primary_focus": [],
                "strategy_note": "Maintain your edge by building portfolio projects, contributing to open-source, and preparing for technical interviews."
            }

        # Sort recommendations: HIGH first, then MEDIUM, then LOW
        priority_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "SUFFICIENT": 3}
        recommendations.sort(key=lambda x: (priority_rank.get(x["priority"], 9), -x["gap"]))

        return {
            "student_name": student_name,
            "career_id": career_id,
            "career_name": career_name,
            "career_domain": career.get("domain", ""),
            "career_description": career_desc,
            "readiness_percentage": readiness_percentage,
            "readiness_tier": readiness_tier,
            "readiness_color": readiness_color,
            "readiness_summary": readiness_summary,
            "total_effective_points": total_effective_points,
            "total_required_points": total_required_points,
            "skills_analysis": skills_analysis,
            "priority_groups": priority_groups,
            "counts": {
                "high": high_priority_count,
                "medium": medium_priority_count,
                "low": low_priority_count,
                "sufficient": sufficient_count,
                "total": len(skills_analysis)
            },
            "recommendations": recommendations,
            "focus_strategy": focus_strategy,
            "inference_trace": inference_trace,
            "working_memory_facts": working_memory_facts
        }
