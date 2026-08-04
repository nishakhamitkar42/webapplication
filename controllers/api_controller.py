import re
from flask import Blueprint, request, jsonify
from models.contact import Contact

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

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
