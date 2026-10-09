"""
rules.py - Production Rules Definition for the Skill-Gap Expert System.

This module formalizes the IF-THEN production rules used by the inference engine.
In expert system terminology:
- An ANTECEDENT (IF condition) evaluates facts asserted in working memory.
- A CONSEQUENT (THEN action) asserts new derived facts, priorities, and conclusions.
"""

# Proficiency labels for scale 1-5
PROFICIENCY_LABELS = {
    1: "Beginner",
    2: "Basic",
    3: "Intermediate",
    4: "Advanced",
    5: "Expert"
}


class ProductionRule:
    """Represents an individual production rule in the knowledge base."""

    def __init__(self, rule_id, name, description, antecedent_desc, consequent_desc):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.antecedent_desc = antecedent_desc
        self.consequent_desc = consequent_desc

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "if_condition": self.antecedent_desc,
            "then_action": self.consequent_desc
        }


# Formal Rule Catalog
SYSTEM_RULES = [
    ProductionRule(
        rule_id="RULE-01",
        name="Skill Gap Existence Rule",
        description="Identifies whether a student possesses a deficiency in a required career competency.",
        antecedent_desc="IF Student Skill Level < Required Skill Level",
        consequent_desc="THEN Assert Fact(Skill Gap = Required - Student) AND Status = 'Needs Improvement'"
    ),
    ProductionRule(
        rule_id="RULE-02",
        name="Sufficient Competency Rule",
        description="Fires when a student meets or exceeds the industry benchmark proficiency.",
        antecedent_desc="IF Student Skill Level >= Required Skill Level (Skill Gap <= 0)",
        consequent_desc="THEN Assert Fact(Skill Gap = 0) AND Status = 'SUFFICIENT' AND Priority = 'SUFFICIENT'"
    ),
    ProductionRule(
        rule_id="RULE-03",
        name="High Priority Critical Gap Rule",
        description="Flags a severe deficiency spanning 3 or more proficiency tiers.",
        antecedent_desc="IF Skill Gap >= 3",
        consequent_desc="THEN Priority = 'HIGH' AND Urgency = 'Critical Career Blocker' AND Action = 'Immediate Focus'"
    ),
    ProductionRule(
        rule_id="RULE-04",
        name="Medium Priority Moderate Gap Rule",
        description="Flags a 2-level deficiency requiring structured upskilling.",
        antecedent_desc="IF Skill Gap == 2",
        consequent_desc="THEN Priority = 'MEDIUM' AND Urgency = 'Important Competency' AND Action = 'Scheduled Learning'"
    ),
    ProductionRule(
        rule_id="RULE-05",
        name="Low Priority Minor Gap Rule",
        description="Flags a minor 1-level deficiency easily bridgeable with quick review.",
        antecedent_desc="IF Skill Gap == 1",
        consequent_desc="THEN Priority = 'LOW' AND Urgency = 'Refinement' AND Action = 'Practice & Polish'"
    ),
    ProductionRule(
        rule_id="RULE-06",
        name="Multi-Gap Focus Strategy Rule",
        description="Prioritizes remediation sequencing when a student exhibits multiple critical deficiencies.",
        antecedent_desc="IF Count(HIGH Priority Gaps) > 1",
        consequent_desc="THEN Recommend focusing on foundational core skills first before secondary tools"
    ),
    ProductionRule(
        rule_id="RULE-07",
        name="Career Readiness Evaluation Rule",
        description="Computes the normalized aggregate readiness index as a percentage of requirements satisfied.",
        antecedent_desc="IF all skills evaluated against Career Benchmarks",
        consequent_desc="THEN Readiness % = (Sum of Effective Skill Points / Sum of Required Points) * 100"
    ),
    ProductionRule(
        rule_id="RULE-08",
        name="Career Readiness Tier Classification Rule",
        description="Categorizes the student into readiness bands based on the aggregate readiness score.",
        antecedent_desc="IF Readiness % is calculated",
        consequent_desc="THEN Assign Tier: >=80% 'Job Ready', 60-79% 'Near Ready', 40-59% 'Developing', <40% 'Foundational'"
    )
]
