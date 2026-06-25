import json

def get_trend_context(trends):

    context = {
        "total_trends": len(trends),
        "top_emerging_issues": trends.sort_values(
            "PriorityScore",
            ascending=False
        ).head(15).to_dict(orient="records"),

        "fastest_growth": trends.sort_values(
            "DeltaPercentile",
            ascending=False
        ).head(10).to_dict(orient="records"),

        "highest_risk": trends.sort_values(
            "AverageRisk",
            ascending=False
        ).head(10).to_dict(orient="records"),
    }

    return json.dumps(context, indent=2)


def get_company_context(companies):

    context = {

        "top_complaint_volume": companies.sort_values(
            "Complaint_Count",
            ascending=False
        ).head(15).to_dict(orient="records"),

        "highest_risk": companies.sort_values(
            "Avg_Risk",
            ascending=False
        ).head(15).to_dict(orient="records"),

        "worst_handling": companies.sort_values(
            "Avg_Handling_Score"
        ).head(15).to_dict(orient="records"),

        "best_handling": companies.sort_values(
            "Avg_Handling_Score",
            ascending=False
        ).head(10).to_dict(orient="records"),

    }

    return json.dumps(context, indent=2)

def get_prediction_context(pred):

    context = {

        "predicted_issue_counts": pred.sort_values(
            "PredictedAnnual",
            ascending=False
        ).to_dict(orient="records"),

        "top_predicted_issues": pred.sort_values(
            "PredictedAnnual",
            ascending=False
        ).head(15).to_dict(orient="records"),

        'most_increased_issues': pred.sort_values(
            'Change_Pct',
            ascending=False
        ).head(10).to_dict(orient="records"),

        'most_decreased_issues': pred.sort_values(
            'Change_Pct',
            ascending=True
        ).head(10).to_dict(orient="records"),

    }

    return json.dumps(context, indent=2)

def get_report_context(df):

    context = {

        "rows": len(df),

        "columns": list(df.columns),

        "summary_statistics":

            df.describe(include="all")
            .fillna("")
            .to_dict(),

        "missing_values":

            df.isna().sum().to_dict(),

        "sample_records":

            df.head(15).to_dict("records"),

    }

    return json.dumps(context, indent=2)
