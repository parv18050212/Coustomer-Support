import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import random

class ChatBot:
    def __init__(self):
        # Initialize NLTK components
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Set similarity threshold
        self.similarity_threshold = 0.3
        
        # Initialize fallback responses
        self.fallback_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "I'm still learning. Could you try asking in a different way?",
            "I don't have enough information to answer that properly.",
            "That's an interesting question, but I'm not sure how to answer it."
        ]
        
        # Initialize with default data
        try:
            # Create initial DataFrame with required columns
            self.df = pd.DataFrame({
                'question': ['default question'],
                'answer': ['I apologize, but I am currently unable to access my knowledge base.']
            })
            # Ensure DataFrame has required columns
            if not all(col in self.df.columns for col in ['question', 'answer']):
                raise ValueError("Default DataFrame initialization failed: missing required columns")
            
            self.vectorizer = TfidfVectorizer()
            # Ensure strings for vectorizer
            self.df['question'] = self.df['question'].astype(str)
            self.df['answer'] = self.df['answer'].astype(str)
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df['question'])
        except Exception as e:
            print(f"Error in default initialization: {e}")
            # Create and validate absolute minimal DataFrame
            try:
                self.df = pd.DataFrame({'question': [''], 'answer': ['']})
                # Ensure DataFrame has expected structure
                if not isinstance(self.df, pd.DataFrame) or \
                   not all(col in self.df.columns for col in ['question', 'answer']):
                    raise ValueError("Failed to create valid fallback DataFrame")
                # Initialize vectorizer with empty data
                self.vectorizer = TfidfVectorizer()
                self.tfidf_matrix = self.vectorizer.fit_transform([''])
            except Exception as inner_e:
                print(f"Critical error in fallback initialization: {inner_e}")
                # Last resort - ensure we have a valid but minimal state
                # Create with a single row containing empty strings to establish structure
                self.df = pd.DataFrame({
                    'question': [''],
                    'answer': ['']
                })
                self.vectorizer = TfidfVectorizer(min_df=0, max_df=1.0)  # Allow all terms
                # Fit with the empty question to establish feature space
                self.tfidf_matrix = self.vectorizer.fit_transform(self.df['question'])
        
        # Try to load and process the CSV data
        try:
            # Load CSV into a temporary DataFrame
            temp_df = pd.read_csv('data/responses.csv')
            print(f"Available columns in CSV: {list(temp_df.columns)}")
            
            # Convert column names to lowercase
            temp_df.columns = temp_df.columns.str.lower()
            
            # Define possible column names for questions and answers
            question_columns = ['question', 'questions', 'prompt', 'input']
            answer_columns = ['answer', 'answers', 'response', 'responses', 'output']
            
            # Find the actual question and answer columns
            question_col = next((col for col in question_columns if col in temp_df.columns), None)
            answer_col = next((col for col in answer_columns if col in temp_df.columns), None)
            
            if not question_col or not answer_col:
                available_cols = list(temp_df.columns)
                error_msg = []
                if not question_col:
                    error_msg.append(f"No question column found. Looking for {question_columns}")
                if not answer_col:
                    error_msg.append(f"No answer column found. Looking for {answer_columns}")
                error_msg.append(f"Available columns: {available_cols}")
                raise ValueError('\n'.join(error_msg))
            
            # Create a new DataFrame with just the columns we need, handling NaN values
            new_df = pd.DataFrame({
                'question': temp_df[question_col].fillna('').astype(str),
                'answer': temp_df[answer_col].fillna('').astype(str)
            })
            # Remove any empty rows
            new_df = new_df[new_df['question'].str.strip() != '']
            new_df = new_df.reset_index(drop=True)
            
            # Verify the new DataFrame is valid
            if len(new_df) == 0:
                raise ValueError("No valid data rows found in CSV")
            
            # If we got this far, all the data is valid
            # Create and fit a new vectorizer on the full dataset
            new_vectorizer = TfidfVectorizer()
            new_tfidf_matrix = new_vectorizer.fit_transform(new_df['question'])
            
            # Only update instance variables after successful vectorizer creation
            self.df = new_df
            self.vectorizer = new_vectorizer
            self.tfidf_matrix = new_tfidf_matrix
        except Exception as e:
            print(f"Error loading CSV: {e}")
            # Keep using the default initialization values set above
    
    def preprocess_text(self, text):
        """Preprocess the input text by tokenizing, removing stopwords, and lemmatizing."""
        # Tokenize and convert to lowercase
        tokens = word_tokenize(text.lower())
        
        # Remove punctuation and stopwords
        tokens = [token for token in tokens if token not in string.punctuation]
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # Lemmatize tokens
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return " ".join(tokens)
    
    def get_response(self, user_input):
        """Generate a response to the user input by finding the most similar question in the dataset."""
        try:
            # Verify DataFrame is in valid state
            if 'question' not in self.df.columns or 'answer' not in self.df.columns:
                print("Error: Invalid DataFrame structure")
                return random.choice(self.fallback_responses)
                
            # Preprocess the user input
            if not user_input or not isinstance(user_input, str):
                return random.choice(self.fallback_responses)
                
            processed_input = self.preprocess_text(user_input)
            
            # Transform user input using the same vectorizer
            user_vector = self.vectorizer.transform([processed_input])
            
            # Check if we have any actual data
            if len(self.df) == 0:
                return random.choice(self.fallback_responses)
                
            # Calculate cosine similarity between user input and all questions
            similarities = cosine_similarity(user_vector, self.tfidf_matrix)
            
            # Find the index of the most similar question
            most_similar_idx = similarities.argmax()
            
            # Return the corresponding answer from the dataset
            # Check if the similarity is above threshold
            if similarities[0][most_similar_idx] >= self.similarity_threshold:
                return self.df['answer'].iloc[most_similar_idx]
            else:
                return random.choice(self.fallback_responses)
            
            # Find the most similar question
            best_match_idx = similarities.argmax()
            max_similarity = similarities[best_match_idx]
            
            # If similarity is too low, return a fallback response
            if max_similarity < 0.3:
                return random.choice(self.fallback_responses)
            
            # Return the corresponding response
            return self.df.iloc[best_match_idx]['response']
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return random.choice(self.fallback_responses)