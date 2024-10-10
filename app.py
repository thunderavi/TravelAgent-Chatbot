import os
from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# Initialize the Groq client with your API key
client = Groq(api_key="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")

# Global state to keep track of the conversation
user_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-chat', methods=['GET'])
def start_chat():
    initial_message = "How can I help you today?"  # Initial message from the assistant
    return jsonify({'reply': initial_message})

@app.route('/get-itinerary', methods=['POST'])
def get_response():
    user_message = request.json.get('message')
    print(f"User Message: {user_message}")  # Debug: log user message

    # Initialize the response
    bot_response = ""

    # Check if we already have a destination
    if 'destination' not in user_data:
        user_data['destination'] = user_message
        bot_response = "For how many days are you planning the trip?"  # Prompt for days
    elif 'days' not in user_data:
        try:
            user_data['days'] = int(user_message)
            destination = user_data['destination']
            days = user_data['days']

            # Generate itinerary using Groq AI based on destination and days
            bot_response = call_groq_api(destination, days)

            # After getting the itinerary, inform the user they can ask anything
            bot_response += "\n\nFeel free to ask me anything else about your trip!"
        except ValueError:
            bot_response = "Please enter a valid number of days."  # Error message for invalid days
    else:
        # Process any further questions from the user
        follow_up_response = call_groq_api_follow_up(user_message)
        bot_response = follow_up_response

    # Return the response
    return jsonify({'reply': bot_response})

def call_groq_api(destination, days):
    # Use the Groq API to generate a concise itinerary with bullet points
    try:
        prompt = (
            f"Please provide a structured travel itinerary for {destination} for {days} days. "
            f"Format the response as follows:\n"
            f"**Day 1:**\n- Activity 1\n- Activity 2\n"
            f"**Day 2:**\n- Activity 1\n- Activity 2\n"
            f"Ensure the response is clear, detailed, and formatted with bullet points."
        )
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        # Get the AI's response
        bot_response = chat_completion.choices[0].message.content
    except Exception as e:
        print("Error while calling Groq AI:", e)
        bot_response = "Sorry, there was an error getting a response from the AI."

    return bot_response

def call_groq_api_follow_up(user_message):
    # Use the Groq API to answer follow-up questions
    try:
        prompt = (
            f"The user is planning a trip. They have asked: '{user_message}'. "
            f"Provide relevant information or advice regarding their trip."
        )
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        follow_up_response = chat_completion.choices[0].message.content
    except Exception as e:
        print("Error while calling Groq AI for follow-up:", e)
        follow_up_response = "Sorry, I couldn't fetch that information at this time."

    return follow_up_response

if __name__ == '__main__':
    app.run(debug=True)
