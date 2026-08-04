# pyrefly: ignore [missing-import]
from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return render_template('home.html', active_page='home')

@main_blueprint.route('/about')
def about():
    return render_template('about.html', active_page='about')

@main_blueprint.route('/projects')
def projects():
    return render_template('projects.html', active_page='projects')

@main_blueprint.route('/certification')
def certification():
    return render_template('certification.html', active_page='certification')

@main_blueprint.route('/skills')
def skills():
    return render_template('skills.html', active_page='skills')

@main_blueprint.route('/achievements')
def achievements():
    return render_template('achievements.html', active_page='achievements')

@main_blueprint.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')
