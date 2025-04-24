import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Function to normalize text
def normalize_text(text):
    # Lowercase the text
    text = text.lower()
    
    # Remove non-alphabetic characters (e.g., numbers, punctuation)
    # text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespaces
    text = ' '.join(text.split())
    
    # Remove stopwords
    # stop_words = set(stopwords.words('english'))
    # text = ' '.join([word for word in text.split() if word not in stop_words])
    
    # Optionally, apply stemming
    # ps = PorterStemmer()
    # text = ' '.join([ps.stem(word) for word in text.split()])
    
    return text