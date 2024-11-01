from agency_swarm.tools import BaseTool
from pydantic import Field
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

class ExtractKeywords(BaseTool):
    """
    A tool to extract keywords from news articles using NLTK.
    """
    text: str = Field(..., description="The text to extract keywords from.")
    num_keywords: int = Field(10, description="The number of top keywords to extract.")

    def run(self):
        """
        Extract keywords from the given text using NLTK.
        """
        try:
            # Tokenize and remove stopwords
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(self.text.lower())
            filtered_tokens = [w for w in word_tokens if w.isalnum() and w not in stop_words]

            # Count word frequencies
            word_freq = Counter(filtered_tokens)

            # Get top keywords
            top_keywords = word_freq.most_common(self.num_keywords)

            return ", ".join([word for word, _ in top_keywords])
        except Exception as e:
            return f"Error extracting keywords: {str(e)}"

if __name__ == "__main__":
    sample_text = "Artificial Intelligence and Machine Learning are transforming various industries. Deep Learning models are becoming more sophisticated, enabling breakthroughs in Natural Language Processing and Computer Vision."
    tool = ExtractKeywords(text=sample_text, num_keywords=5)
    print(tool.run())
