import plotly.express as px

def histogram_plot(df, col):
    return px.histogram(df, x=col, template="plotly_dark")

def scatter_plot(df, x, y):
    return px.scatter(df, x=x, y=y, template="plotly_dark")

def heatmap_plot(df):
    return px.imshow(df.corr(numeric_only=True), text_auto=True, template="plotly_dark")
