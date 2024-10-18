from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact_us.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy modification tracking
db = SQLAlchemy(app)

# Define SQLAlchemy model for contact entries
class ContactEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ContactEntry {self.name}, {self.email}>'

# Initialize the database (run this once when the app starts)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Render the contact form page
    return render_template('contact_us.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us_page():
    if request.method == 'POST':
        # Extract the data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Validate form data
        if not name or not email or not message:
            return "Error: All fields are required.", 400  # Return an error if any field is missing

        # Add new contact entry to the database
        new_entry = ContactEntry(name=name, email=email, message=message)
        db.session.add(new_entry)
        db.session.commit()
        
        return "Thank you for your message!"
    
    return render_template('contact_us.html')

@app.route('/entries')
def entries():
    # Retrieve all contact entries from the database
    entries = ContactEntry.query.all()
    return render_template('entries.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True, port=5012)
