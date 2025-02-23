import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.linear_model import LinearRegression
import io
import numpy as np
from fetch import fetch_recall_data

def get_dataframe():
    data = fetch_recall_data()
    df = pd.json_normalize(data['results'])
    return df


def generate_component_chart():
    """Generates a bar chart for the top 10 most recalled components and returns a BytesIO image."""
    df = get_dataframe()
    # Get the top 10 most recalled components
    component_counts = df['Component'].value_counts()
    
    # Create a BytesIO buffer
    img_buffer = io.BytesIO()

    # Plot the figure
    plt.figure(figsize=(10, 5))
    sns.barplot(x=component_counts.index[:10], y=component_counts.values[:10])
    plt.xticks(rotation=45)
    plt.title("Top 10 Most Commonly Recalled Components")
    plt.xlabel("Component")
    plt.ylabel("Count")
    
    # Save the figure to the buffer
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the plot to free memory

    # Move to the beginning of the buffer
    img_buffer.seek(0)

    return img_buffer  # Return the image as BytesIO


def generate_manufacturer_chart():
    """Generates a bar chart for the top 10 manufacturers with most recalls and returns a BytesIO image."""
    df = get_dataframe()
    # Get the top 10 manufacturers with the most recalls
    manufacturer_counts = df['Manufacturer'].value_counts()
    
    # Create a BytesIO buffer
    img_buffer = io.BytesIO()

    # Plot the figure
    plt.figure(figsize=(10, 5))
    sns.barplot(x=manufacturer_counts.index[:10], y=manufacturer_counts.values[:10])
    plt.xticks(rotation=45)
    plt.title("Top 10 Manufacturers with Most Recalls")
    plt.xlabel("Manufacturer")
    plt.ylabel("Count")
    
    # Save the figure to the buffer
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the plot to free memory

    # Move to the beginning of the buffer
    img_buffer.seek(0)

    return img_buffer  # Return the image as BytesIO


def generate_severity_chart():
    """Generates a histogram for recall severity scores and returns a BytesIO image."""
    df = get_dataframe()
    # Compute Severity Score as text length of 'Consequence' column
    df['SeverityScore'] = df['Consequence'].apply(lambda x: len(str(x)))

    # Create a BytesIO buffer
    img_buffer = io.BytesIO()

    # Plot the figure
    plt.figure(figsize=(10, 5))
    sns.histplot(df['SeverityScore'], bins=20, kde=True)
    plt.title("Distribution of Recall Severity Scores")
    plt.xlabel("Severity Score (Text Length of Consequence)")
    plt.ylabel("Frequency")
    
    # Save the figure to the buffer
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the plot to free memory

    # Move to the beginning of the buffer
    img_buffer.seek(0)

    return img_buffer  # Return the image as BytesIO


def generate_recall_trend_chart():
    """Generates a line chart for recall reports over time and returns a BytesIO image."""
    df = get_dataframe()
    # Convert 'ReportReceivedDate' to datetime and extract the year
    df['ReportReceivedDate'] = pd.to_datetime(df['ReportReceivedDate'], errors='coerce')
    df['Year'] = df['ReportReceivedDate'].dt.year

    # Count the number of recalls per year
    trend_counts = df['Year'].value_counts().sort_index()

    # Create a BytesIO buffer
    img_buffer = io.BytesIO()

    # Plot the figure
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=trend_counts.index, y=trend_counts.values, marker='o')
    plt.title("Recall Reports Over Time")
    plt.xlabel("Year")
    plt.ylabel("Number of Recalls")
    
    # Save the figure to the buffer
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the plot to free memory

    # Move to the beginning of the buffer
    img_buffer.seek(0)

    return img_buffer


def generate_recall_forecast_chart(forecast_years=5):
    """Generates a recall forecast chart using Exponential Smoothing and returns a BytesIO image."""
    df = get_dataframe()
    # Convert 'ReportReceivedDate' to datetime and extract the year
    df['ReportReceivedDate'] = pd.to_datetime(df['ReportReceivedDate'], errors='coerce')
    df['Year'] = df['ReportReceivedDate'].dt.year

    # Count the number of recalls per year
    trend_counts = df['Year'].value_counts().sort_index()

    # Drop NaN values
    data = trend_counts.dropna()

    # Fit Exponential Smoothing Model
    model = ExponentialSmoothing(data, trend='add', seasonal=None).fit()
    
    # Predict next `forecast_years` years
    predictions = model.forecast(forecast_years)

    # Create a BytesIO buffer
    img_buffer = io.BytesIO()

    # Plot the figure
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.values, label='Historical Data', marker='o')
    plt.plot(predictions.index, predictions.values, label='Forecast', linestyle='dashed', marker='o')
    plt.title("Future Recall Prediction")
    plt.xlabel("Year")
    plt.ylabel("Number of Recalls")
    plt.legend()

    # Save the figure to the buffer
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the plot to free memory

    # Move to the beginning of the buffer
    img_buffer.seek(0)

    return img_buffer  # Return the image as BytesIO


def generate_impact_score_chart():
    """Generates a histogram for customer impact scores and returns a BytesIO image."""
    df = get_dataframe()
    # Compute Impact Score as text length of 'Summary' column
    df['ImpactScore'] = df['Summary'].apply(lambda x: len(str(x)))

    # Create a BytesIO buffer
    img_buffer = io.BytesIO()

    # Plot the figure
    plt.figure(figsize=(10, 5))
    sns.histplot(df['ImpactScore'], bins=20, kde=True)
    plt.title("Distribution of Customer Impact Scores")
    plt.xlabel("Impact Score (Text Length of Summary)")
    plt.ylabel("Frequency")
    
    # Save the figure to the buffer
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the plot to free memory

    # Move to the beginning of the buffer
    img_buffer.seek(0)

    return img_buffer  # Return the image as BytesIO


def generate_remedy_score_chart():
    """Generates a histogram for remedy effectiveness scores and returns a BytesIO image."""
    df = get_dataframe()
    # Compute Remedy Score as text length of 'Remedy' column
    df['RemedyScore'] = df['Remedy'].apply(lambda x: len(str(x)))

    # Create a BytesIO buffer
    img_buffer = io.BytesIO()

    # Plot the figure
    plt.figure(figsize=(10, 5))
    sns.histplot(df['RemedyScore'], bins=20, kde=True)
    plt.title("Distribution of Remedy Effectiveness Scores")
    plt.xlabel("Remedy Score (Text Length of Remedy)")
    plt.ylabel("Frequency")
    
    # Save the figure to the buffer
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the plot to free memory

    # Move to the beginning of the buffer
    img_buffer.seek(0)

    return img_buffer  # Return the image as BytesIO


def generate_recall_forecast_lr(forecast_years=5):
    """Predicts recalls for the next 5 years using Linear Regression and returns a BytesIO image."""
    df = get_dataframe()
    # Convert 'ReportReceivedDate' to datetime and extract the year
    df['ReportReceivedDate'] = pd.to_datetime(df['ReportReceivedDate'], errors='coerce')
    df['Year'] = df['ReportReceivedDate'].dt.year

    # Count the number of recalls per year
    trend_counts = df['Year'].value_counts().sort_index()

    # Prepare data for Linear Regression
    X = np.array(df['Year'].dropna()).reshape(-1, 1)
    y = np.array(trend_counts[df['Year'].dropna()]).reshape(-1, 1)

    if len(X) > 1 and len(y) > 1:
        model = LinearRegression()
        model.fit(X, y)

        # Predict future recalls
        future_years = np.array(range(df['Year'].max() + 1, df['Year'].max() + forecast_years + 1)).reshape(-1, 1)
        future_recalls = model.predict(future_years)

        # Create a BytesIO buffer
        img_buffer = io.BytesIO()

        # Plot the figure
        plt.figure(figsize=(10, 5))
        plt.scatter(X, y, color='blue', label='Actual Data')
        plt.plot(future_years, future_recalls, color='red', linestyle='dashed', label='Predicted Recalls')
        plt.title("Predicted Recalls for Next 5 Years")
        plt.xlabel("Year")
        plt.ylabel("Number of Recalls")
        plt.legend()

        # Save the figure to the buffer
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        plt.close()  # Close the plot to free memory

        # Move to the beginning of the buffer
        img_buffer.seek(0)

        return img_buffer  # Return the image as BytesIO
    else:
        return None  # Return None if insufficient data


if __name__ == "__main__":
    generate_component_chart()