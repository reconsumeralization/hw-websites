from flask import Flask, request, render_template
from flask_mail import Mail, Message
from wtforms import Form, StringField, TextAreaField, validators

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# WTForms configuration
class ContactForm(Form):
    name = StringField('Name', [validators.InputRequired(), validators.Length(min=2, max=50)])
    email = StringField('Email', [validators.InputRequired(), validators.Email()])
    message = TextAreaField('Message', [validators.InputRequired(), validators.Length(min=10, max=500)])

@app.route('/submit', methods=['POST'])
def submit_form():
    form = ContactForm(request.form)
    if form.validate():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        site = request.form.get('site')

        # Compose email
        msg = Message('New Contact Form Submission',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=['recipient_email@example.com'])  # Replace with your recipient email
        msg.body = f"""
        You have received a new message from {name} ({email}) via {site}.

        Message:
        {message}
        """

        try:
            mail.send(msg)
            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
            return render_template('error.html'), 500

        return render_template('success.html', site=site, name=name)
    else:
        # Handle form validation errors
        return render_template('error.html', errors=form.errors), 400

if __name__ == '__main__':
    app.run(debug=True)
