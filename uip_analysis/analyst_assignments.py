"""Case assignments of the analyst-derived tables of the paper (Tables 7, 9, 10 and 11).

These tables list, for each category, the exemplars that the authors assigned to it after reading the
characterisation answers. The scripts take the assignments as input and show, for every assigned case,
the text of the exemplar that supports it.
"""
DOMAINS = ["Automotive", "IT/Cloud", "Robotics", "Healthcare", "Smart City", "Aerospace"]

# Table 7 - affected quality dimensions
TABLE7 = {
    "Safety": ["CS11", "CS12", "CS16", "CS17", "CS18"],
    "Performance": ["CS1", "CS3", "CS8", "CS18"],
    "Reliability & Availability": ["CS2", "CS13", "CS15"],
    "Mission Success": ["CS5", "CS11", "CS12"],
    "Human Factors & Trust": ["CS5", "CS17"],
    "Resource Efficiency / Cost": ["CS1", "CS3", "CS13", "CS18"],
}

# Table 9 - applicability conditions
TABLE9 = {
    "Architectural Assumptions": ["CS1", "CS12", "CS13", "CS15"],
    "Infrastructure Requirements": ["CS2", "CS11", "CS12"],
    "Observability Requirements": ["CS11", "CS12", "CS16", "CS18"],
    "Model Availability": ["CS5", "CS16"],
    "Adaptation Capability": ["CS5", "CS13", "CS16", "CS18"],
    "Operational Scope": ["CS4", "CS7", "CS13"],
}

# Table 10 - lifecycle activities
TABLE10 = {
    "Modeling": ["CS5", "CS13", "CS15", "CS16"],
    "Analysis & Verification": ["CS1", "CS5", "CS13", "CS15", "CS16"],
    "Monitoring": ["CS1", "CS2", "CS4", "CS7", "CS9", "CS11", "CS12", "CS15", "CS18"],
    "Runtime Decision-Making": ["CS5", "CS11", "CS12", "CS13", "CS16", "CS18"],
    "Mitigation & Adaptation": ["CS1", "CS2", "CS4", "CS5", "CS7", "CS11", "CS12", "CS13", "CS15", "CS16", "CS18"],
}

# Table 11 - trade-offs
TABLE11 = {
    "Robustness vs Resource Consumption": ["CS1", "CS2", "CS12", "CS13"],
    "Safety vs Performance": ["CS12", "CS16", "CS18"],
    "Responsiveness vs Stability": ["CS1", "CS13", "CS16"],
    "Autonomy vs Assurance": ["CS5", "CS15"],
    "Sensitivity vs False Positives": ["CS11"],
}
