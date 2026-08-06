import os
import re
from flask import Blueprint, request, jsonify
from models.contact import Contact

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

# System prompt that grounds the chatbot in the portfolio content
CHAT_SYSTEM_PROMPT = (
    "You are 'Nisha Assistant', a friendly and professional virtual assistant for the "
    "portfolio website of Nisha, a Sales Executive specializing in Logistics and Supply Chain. "
    "You help visitors learn about Nisha's background, skills, projects, certifications, "
    "achievements, and how to contact her.\n\n"
    "Guidelines:\n"
    "- Be concise and helpful. Keep answers to a few short sentences unless the visitor asks for detail.\n"
    "- When asked about Nisha's role, describe her as a Logistics and Supply Chain Sales Executive.\n"
    "- If you do not know an answer, politely say so and suggest using the Contact page for details.\n"
    "- For business inquiries, encourage visitors to use the contact form at /contact.\n"
    "- Never invent credentials, achievements, or contact details that are not part of the website content."
)

@api_blueprint.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
        
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()
    
    # Validation
    if not name or not email or not subject or not message:
        return jsonify({"status": "error", "message": "All fields are required"}), 400
        
    if not EMAIL_REGEX.match(email):
        return jsonify({"status": "error", "message": "Invalid email address format"}), 400
        
    try:
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
        return jsonify({
            "status": "success",
            "message": "Your message has been sent successfully! We will get back to you soon.",
            "contact_id": contact.id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500

@api_blueprint.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot messages by calling the Groq API."""
    data = request.get_json()

    if not data or not data.get('message', '').strip():
        return jsonify({"status": "error", "message": "Please enter a message."}), 400

    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        return jsonify({
            "status": "error",
            "message": "GROQ_API_KEY is not configured on the server."
        }), 500

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model=os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile'),
            messages=[
                {"role": "system", "content": CHAT_SYSTEM_PROMPT},
                {"role": "user", "content": data['message'].strip()}
            ],
            temperature=0.7,
            max_tokens=512
        )
        reply = completion.choices[0].message.content.strip()
        return jsonify({"status": "success", "reply": reply}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Chat error: {str(e)}"}), 500

@api_blueprint.route('/contacts', methods=['GET'])
def get_contacts():
    """Retrieve all contact form submissions (primarily for testing/verification)."""
    try:
        contacts = Contact.get_all()
        return jsonify({
            "status": "success",
            "contacts": [{
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "subject": c.subject,
                "message": c.message,
                "created_at": c.created_at
            } for c in contacts]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
