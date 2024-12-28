from flask import Flask, render_template, request
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import nltk

# Initialize Flask app
app = Flask(__name__)

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def fetch_instagram_trends(keyword):
    """
    Fetch hashtag popularity data for a given keyword using Instagram (mock or scraping).
    """
    # Simulate API or scraping response (since Instagram's public API doesn't allow hashtag data directly)
    hashtag_data = {
        "low_competition": [f"#{keyword}Tips", f"#{keyword}Guide"],
        "moderate_competition": [f"#{keyword}", f"#{keyword}Life"],
        "high_competition": [f"#Go{keyword.capitalize()}", f"#{keyword}Now"],
    }
    return hashtag_data

def generate_hashtags(text):
    """
    Generate unique hashtags and fetch trends for input text.
    """
    # Tokenize the input text
    words = word_tokenize(text.lower())

    # Remove stopwords and non-alphanumeric characters
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word not in stop_words and word.isalnum()]

    # Generate hashtags and analyze trends
    all_hashtags = {}
    for keyword in keywords:
        trends = fetch_instagram_trends(keyword)
        all_hashtags[keyword] = trends

    return all_hashtags

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handle the main page for hashtag generation and analysis.
    """
    if request.method == "POST":
        # Get user input from the form
        user_input = request.form["description"]
        hashtags = generate_hashtags(user_input)
        return render_template("index.html", hashtags=hashtags, description=user_input)

    # Default behavior for GET requests
    return render_template("index.html", hashtags=None)

if __name__ == "__main__":
    app.run(debug=True)
