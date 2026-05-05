import datasets

def format_list(l):
    return ",".join(map(str, l))

def get_t_test_samples():
    """
    Returns sample data specifically for two-group t-tests.
    """
    return [
        {
            "name": "Clinical Trial (Effectiveness)",
            "data": "Experimental: 18.5, 21.2, 19.8, 22.1, 20.5; Control: 15.2, 16.8, 14.9, 17.1, 15.8"
        },
        {
            "name": "Education (Test Scores)",
            "data": "Method A: 85, 92, 88, 95, 90, 87; Method B: 78, 82, 80, 85, 79, 81"
        },
        {
            "name": "Manufacturing (Durability)",
            "data": "Factory A: 120, 125, 118, 122; Factory B: 112, 115, 110, 114"
        }
    ]

def get_anova_samples():
    samples = []
    for i, data in enumerate(datasets.anova_set):
        # Format: "Group 1: 1, 2; Group 2: 3, 4"
        formatted = "; ".join([f"Group {j+1}: {format_list(group)}" for j, group in enumerate(data)])
        samples.append({"name": f"ANOVA Case {i+1}", "data": formatted})
    return samples

def get_linear_samples():
    samples = []
    for i, data in enumerate(datasets.linear_set):
        samples.append({
            "name": f"Regression Case {i+1}",
            "x": format_list(data[0]),
            "y": format_list(data[1])
        })
    return samples

def get_descriptive_samples():
    samples = []
    for i, data in enumerate(datasets.descriptive_set):
        samples.append({"name": f"Dataset {i+1}", "data": format_list(data)})
    return samples

def get_confidence_samples():
    # This tool has multiple modes, so we'll provide samples for each
    return {
        "two_pop": [
            {"name": "Compare A vs B", "n1": d[0][0], "x1": d[0][1], "s1": d[0][2], "n2": d[1][0], "x2": d[1][1], "s2": d[1][2], "t": d[2], "var": d[3]}
            for d in datasets.two_pops
        ],
        "dep_data": [
            {"name": "Pre vs Post", "before": format_list(d[0]), "after": format_list(d[1])}
            for d in datasets.dep_data_set
        ],
        "two_samp_prop": [
            {"name": "Prop A vs B", "n1": d[0][0], "p1": d[0][1], "n2": d[1][0], "p2": d[1][1]}
            for d in datasets.two_samp_prop_set
        ]
    }

def get_predictive_samples():
    """
    Returns sample data for ML predictive modeling.
    """
    return [
        {
            "name": "House Price Prediction (Regression)",
            "type": "linear",
            "data": "Price: 300, 450, 280, 520, 390, 610, 420; Sqft: 1500, 2200, 1400, 2500, 1800, 3000, 2100; Bedrooms: 3, 4, 2, 4, 3, 5, 4"
        },
        {
            "name": "Student Admission (Classification)",
            "type": "logistic",
            "data": "Admit: 1, 1, 0, 1, 0, 1, 0, 1; GPA: 3.8, 3.9, 2.9, 3.5, 3.1, 4.0, 3.0, 3.7; Score: 1400, 1550, 1100, 1300, 1150, 1590, 1200, 1450"
        }
    ]
