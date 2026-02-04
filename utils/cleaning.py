def clean_data(df):

    report = {}

    report["duplicates_removed"] = df.duplicated().sum()
    df = df.drop_duplicates()

    report["missing_before"] = df.isnull().sum().sum()
    df = df.fillna(df.mean(numeric_only=True))

    return df, report
