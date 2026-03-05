def suggest_followups(intent):

    if intent == "ranking":
        return [
            "Show revenue trend for these products",
            "Compare regions",
            "Forecast next month revenue"
        ]

    return []