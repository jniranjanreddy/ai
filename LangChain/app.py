from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoTokenizer
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Initialize the question-answering pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Initialize tokenizer for token counting
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased-distilled-squad")

# Knowledge base with information the chatbot can answer questions about
knowledge_base = """
my name is Niranjan
Language Models are a type of AI model that can generate text based on a given prompt.
They are trained on large amounts of text data and learn patterns in language.
Popular language models include GPT, BERT, and T5.

Artificial Intelligence (AI) is a field of computer science that aims to create machines 
that can perform tasks that typically require human intelligence. This includes learning, 
reasoning, problem-solving, perception, and language understanding.

Machine Learning is a subset of AI that focuses on algorithms that can learn and improve 
from experience without being explicitly programmed. Common types include supervised learning, 
unsupervised learning, and reinforcement learning.

Python is a popular programming language for AI and machine learning due to its simplicity 
and extensive libraries like TensorFlow, PyTorch, scikit-learn, and transformers.

Deep Learning is a subset of machine learning that uses neural networks with multiple layers 
to model and understand complex patterns in data. It's particularly effective for tasks like 
image recognition, natural language processing, and speech recognition.
"""

def count_tokens(text):
    """
    Count the number of tokens in a given text
    """
    return len(tokenizer.encode(text))

def answer_question(question, context):
    """
    Use the QA pipeline to answer a question based on the given context
    """
    try:
        result = qa_pipeline(question=question, context=context)
        return result['answer'], result['score']
    except Exception as e:
        return f"Sorry, I couldn't process that question: {str(e)}", 0.0

@app.route('/')
def index():
    """
    Render the main chat interface
    """
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages via AJAX
    """
    try:
        data = request.get_json()
        user_question = data.get('message', '').strip()
        
        if not user_question:
            return jsonify({
                'response': '🤖 Please ask me a question!',
                'confidence': 0,
                'tokens': {'input': 0, 'output': 0, 'total': 0}
            })
        
        # Get answer from the chatbot
        answer, confidence = answer_question(user_question, knowledge_base)
        
        # Count tokens for input and output
        input_tokens = count_tokens(user_question)
        output_tokens = count_tokens(answer)
        total_tokens = input_tokens + output_tokens
        
        return jsonify({
            'response': answer,
            'confidence': round(confidence, 2) if confidence > 0 else 0,
            'tokens': {
                'input': input_tokens,
                'output': output_tokens,
                'total': total_tokens
            }
        })
    
    except Exception as e:
        return jsonify({
            'response': f'Sorry, there was an error processing your request: {str(e)}',
            'confidence': 0,
            'tokens': {'input': 0, 'output': 0, 'total': 0}
        }), 500

if __name__ == '__main__':
    print("🚀 Starting AI Chatbot Web Server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

