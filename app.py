from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/contact', methods=['POST'])
def contact():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        contact = Contact(name=name, email=email, message=message)
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Thank you! Your message has been sent.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Sorry, there was an error sending your message.'})


# Admin setup
admin = Admin(app, name='Portfolio Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Contact, db.session))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Add sample project if none exist
        if Project.query.count() == 0:
            sample_project = Project(
                title="Data Analysis Dashboard",
                description="Python-based data analysis project using Pandas and visualization libraries.",
                technologies="Python,Pandas,Matplotlib"
            )
            db.session.add(sample_project)
            db.session.commit()
    
    app.run(debug=True)
