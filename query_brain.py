import google.generativeai as genai
import os
import pandas as pd
from dotenv import load_dotenv
from fetch import fetch_recall_data

load_dotenv()  # Load environment variables from .env file

def get_dataframe():
    data = fetch_recall_data()
    df = pd.json_normalize(data['results'])
    
    # Ensure all boolean values are converted to strings to prevent concatenation errors
    for col in df.columns:
        if df[col].dtype == "bool":
            df[col] = df[col].astype(str)
    
    # Convert NaN values to a placeholder
    df = df.fillna("N/A")
    
    return df

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")
genai.configure(api_key=api_key)

def query_brain(query, model_name="gemini-1.5-flash-001"):
    """
    Answers questions related to vehicle recall data using the Gemini API.

    Args:
        query: The user's question.
        model_name: The name of the Gemini model to use.

    Returns:
        A string containing the answer.
    """
    data = get_dataframe()

    try:
        model = genai.GenerativeModel(model_name)
        
        # Convert the dataframe to a string-friendly format
        data_string = "\n".join(data.astype(str).apply(lambda row: " | ".join(row), axis=1))
        
        context = f"""
        You are an AI assistant specialized in vehicle recall data. You will be given a dataset
        containing vehicle recalls, including affected models, issues, solutions, and remedies.
        Your task is to answer user questions accurately based on this data.
        
        Here is the recall data:
        {data_string}
        """
        
        prompt = f"""
        {context}
        
        User Question: {query}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error processing query: {e}")
        return "Sorry, I couldn't process your request."

if __name__ == "__main__":
    print("Welcome to the Vehicle Recall Chatbot! Type 'exit' to quit.")
    
    while True:
        user_input = input("Ask a question about vehicle recalls: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        answer = query_brain(user_input)
        print("\nResponse:", answer, "\n")
