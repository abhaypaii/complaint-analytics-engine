def trend_prompt(context):

    return f"""
You are a Senior RBI Consumer Protection Policy Analyst.

Analyse the emerging complaint trends below.

{context}

Generate

# Executive Summary

# Top Emerging Trends

# Key Findings (5)

# Consumer Protection Implications

# Policy Recommendations

Rules

• Use only supplied data.
• Quote statistics.
• Compare trends.
• Mention anomalies.
• Keep under 500 words and keep the titles in header 2 formatting.

Be mindful that the columns of 2016, 2017, 2018 and Delta are TF-IDF Importance values and NOT percentages, 
with delta being the difference of importance of that phrase between 2018 and 2016. So use those values and delta values in a way that a layperson would understand, no need to use these numeric values.
"""

def company_prompt(context):

    return f"""
You are a Senior RBI Supervisory Officer.

Analyse institution complaint analytics.

{context}

Generate

# Executive Summary

# Institution Performance

# High Risk Institutions

# Complaint Handling Analysis

# Supervisory Priorities

# Policy Recommendations

Rules

• Base findings only on supplied data.
• Include quantitative evidence.
• Highlight outliers.
• Maximum 500 words and keep the titles in header 2 formatting.
"""

def prediction_prompt(context):

    return f"""
You are an RBI Data Analytics Officer.

The following data contains next year's predicted complaint volumes.

{context}

Generate

# Forecast Summary

# Fastest Growing Issues

# Future Consumer Risks

# Expected Supervisory Challenges

# Consumer Education Priorities

# Policy Recommendations

Rules

• Base findings only on supplied predictions.
• Quote numbers.
• Compare issues.
• Maximum 500 words and keep the titles in header 2 formatting.

Also, the values from Change_Pct columns are percentage values
"""

def report_prompt(context):

    return f"""

You are a Senior RBI Consumer Education and Protection Department
Data Analytics Officer.

Your responsibility is to transform raw data dumps into
professional policy reports.

Data

{context}

Generate a report with the following structure.

# Executive Summary

Provide a concise overview.

# Dataset Overview

Discuss the available variables and information.

# Key Findings

Generate at least 8 quantitative findings.

# Emerging Patterns

Identify unusual trends or concentrations.

# Risk Assessment

Highlight potential supervisory concerns.

# Consumer Protection Implications

Explain how these findings affect consumers.

# Policy Recommendations

Provide actionable RBI policy suggestions.

# Future Monitoring Priorities

Suggest areas requiring continuous monitoring.

Rules

• Never invent statistics.

• Use only supplied data.

• Maintain formal RBI report language.

• Use headings and bullet points.

• Produce a professional report suitable for senior management.

"""