from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Load a pre-trained NLP model (e.g., Hugging Face)
nlp_model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Data model for API requests
class Query(BaseModel):
    user_id: str
    channel: str  # e.g., "chat", "email", "voice"
    query: str

# Sample knowledge base for FAQs
knowledge_base = {
    "return policy": "Our return policy lasts 30 days from the purchase date. Please contact support for assistance.",
    "shipping": "We offer free shipping on orders over $50. Delivery typically takes 5-7 business days."
}

# Escalation rules (simple keyword matching)
escalation_keywords = ["refund", "cancel order", "technical issue"]

# Function to process queries
def process_query(query: str) -> str:
    for keyword, response in knowledge_base.items():
        if keyword in query.lower():
            return response
    return "I'm sorry, I couldn't find an answer to your question. Let me connect you to a human agent."

# Endpoint for handling customer queries
@app.post("/handle-query")
async def handle_query(query: Query):
    # NLP sentiment analysis (to check if customer is upset)
    sentiment = nlp_model(query.query)[0]
    
    # Check for escalation
    if any(keyword in query.query.lower() for keyword in escalation_keywords) or sentiment["label"] == "NEGATIVE":
        return {"response": "Your issue is being escalated to a human agent.", "escalate": True}
    
    # Process query using knowledge base
    response = process_query(query.query)
    return {"response": response, "escalate": False}

# Endpoint for testing
@app.get("/")
async def root():
    return {"message": "Customer Support Chatbot is running!"}

