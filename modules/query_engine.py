def process_query(df, intent, year=None, region=None):

    data = df.copy()

    if year:
        data = data[data["year"] == year]

    if region:
        data = data[data["region"] == region]

    return data