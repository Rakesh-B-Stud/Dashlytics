from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

def run_models(df, target):

    df = df.copy()
    le = LabelEncoder()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = le.fit_transform(df[col].astype(str))

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "KNN": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(),
        "Naive Bayes": GaussianNB()
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        results[name] = model.score(X_test, y_test)

    best = max(results, key=results.get)

    return results, best
