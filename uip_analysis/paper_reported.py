"""Values reported in the manuscript (current version), used only for cross-validation of the scripts."""
DOMAINS = ["Automotive", "IT/Cloud", "Robotics", "Healthcare", "Smart City", "Aerospace"]

# RQ1 -- text (Sec. 6.1.1 / 6.1.2)
RQ1_TEXT = {"dominance": 11, "conflict": 14, "augmentation": 14, "independence": 4}
RQ1_NATURE_TEXT = {"Heterogeneous": 16, "Homogeneous/Mixed": 2}
# RQ1 -- pgfplots data of Fig. 3 (MetaAnalysis.tex), in DOMAINS order
RQ1_FIG3 = {
    "dominance":    dict(zip(DOMAINS, [2, 4, 3, 0, 1, 1])),
    "conflict":     dict(zip(DOMAINS, [4, 5, 2, 1, 1, 1])),
    "augmentation": dict(zip(DOMAINS, [4, 4, 3, 1, 1, 1])),
}
# RQ1 -- Table 4 (het, hom/mixed)
RQ1_TABLE4 = dict(zip(DOMAINS, [(5, 0), (5, 2), (3, 0), (1, 0), (1, 0), (1, 0)]))

# RQ2 -- Table 5 (cross, same/partial) and the .tex comment
RQ2_TABLE5 = dict(zip(DOMAINS, [(3, 2), (6, 1), (3, 0), (1, 0), (0, 1), (1, 0)]))
RQ2_CROSS_COMMENT = ["CS1", "CS2", "CS3", "CS5", "CS8", "CS9", "CS11", "CS12", "CS13",
                     "CS14", "CS15", "CS16", "CS17", "CS18"]
RQ2_SAME_COMMENT = ["CS4", "CS6", "CS7", "CS10"]
RQ2_MECHANISMS = {  # Sec. 6.2.3
    "Propagation": ["CS1", "CS13", "CS15", "CS18"],
    "Amplification": ["CS5", "CS11", "CS16", "CS18"],
    "Dominance": ["CS2", "CS5", "CS12", "CS15"],
    "Trade-off / Conflict": ["CS1", "CS7", "CS13", "CS16", "CS17"],
}

# RQ3 -- text and Table 6 (multi, generic) + Table 7
RQ3_TEXT = {"Multi-dimensional": 15, "Generic/Template": 3}
RQ3_TABLE6 = dict(zip(DOMAINS, [(4, 1), (5, 2), (3, 0), (1, 0), (1, 0), (1, 0)]))
RQ3_TABLE7 = {
    "Safety": ["CS11", "CS12", "CS16", "CS17", "CS18"],
    "Performance": ["CS1", "CS3", "CS8", "CS18"],
    "Reliability & Availability": ["CS2", "CS13", "CS15"],
    "Mission Success": ["CS5", "CS11", "CS12"],
    "Human Factors & Trust": ["CS5", "CS17"],
    "Resource Efficiency / Cost": ["CS1", "CS3", "CS13", "CS18"],
}

# RQ4 -- Tables 8-12
RQ4_TABLE8 = {
    "Awareness": ["CS1", "CS4", "CS5", "CS6", "CS7", "CS9", "CS11", "CS12", "CS13", "CS15", "CS16", "CS18"],
    "Detectability": ["CS1", "CS2", "CS4", "CS5", "CS7", "CS9", "CS11", "CS12", "CS15", "CS16", "CS18"],
    "Representation": ["CS1", "CS2", "CS4", "CS5", "CS11", "CS12", "CS13", "CS15", "CS16", "CS18"],
    "Prevention": ["CS1", "CS4", "CS7", "CS11", "CS12", "CS13", "CS16"],
    "Understanding": ["CS1", "CS5", "CS11", "CS12", "CS13", "CS15", "CS16", "CS18"],
    "Mitigation": ["CS1", "CS2", "CS4", "CS5", "CS7", "CS11", "CS12", "CS13", "CS15", "CS16", "CS18"],
}
RQ4_TABLE9 = {
    "Architectural Assumptions": ["CS1", "CS12", "CS13", "CS15"],
    "Infrastructure Requirements": ["CS2", "CS11", "CS12"],
    "Observability Requirements": ["CS11", "CS12", "CS16", "CS18"],
    "Model Availability": ["CS5", "CS16"],
    "Adaptation Capability": ["CS5", "CS13", "CS16", "CS18"],
    "Operational Scope": ["CS4", "CS7", "CS13"],
}
RQ4_TABLE11 = {
    "Robustness vs Resource Consumption": ["CS1", "CS2", "CS12", "CS13"],
    "Safety vs Performance": ["CS11", "CS12", "CS16"],
    "Responsiveness vs Stability": ["CS1", "CS16"],
    "Autonomy vs Assurance": ["CS5", "CS15"],
    "Sensitivity vs False Positives": ["CS11"],
}
RQ4_TABLE12 = {
    "Detection": ["CS1", "CS2", "CS5", "CS9", "CS11", "CS12", "CS15", "CS18"],
    "Representation": ["CS1", "CS2", "CS5", "CS11", "CS12", "CS13", "CS15", "CS16"],
    "Analysis": ["CS1", "CS5", "CS11", "CS12", "CS13", "CS15", "CS16", "CS18"],
    "Mitigation": ["CS1", "CS2", "CS4", "CS5", "CS7", "CS11", "CS12", "CS13", "CS15", "CS16", "CS18"],
}
RQ4_TABLE10 = {
    "Modeling": ["CS5", "CS13", "CS15", "CS16"],
    "Analysis & Verification": ["CS1", "CS5", "CS13", "CS15", "CS16"],
    "Monitoring": ["CS1", "CS2", "CS4", "CS7", "CS9", "CS11", "CS12", "CS15", "CS18"],
    "Runtime Decision-Making": ["CS5", "CS11", "CS12", "CS13", "CS16", "CS18"],
    "Mitigation & Adaptation": ["CS1", "CS2", "CS4", "CS5", "CS7", "CS11", "CS12", "CS13", "CS15", "CS16", "CS18"],
}
