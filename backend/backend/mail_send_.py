
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask,request

def send_email(receiver_email, subject, message_body, reply=False,reply_to_email=None):
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'goodturn@gmail.com'  
    message['To'] = receiver_email
    message['Subject'] = subject
    sender_email = mail_config.sender_email
    # Add Reply-To header if specified
    if reply_to_email:
        message.add_header('Reply-To', reply_to_email)

    # Attach the message body
    message.attach(MIMEText(message_body, 'html'))

    # Create SMTP session for sending the mail
    try:
        smtp_server = 'smtp.gmail.com'
        port = 587  # For SSL - 465, For TLS - 587
        app_password = mail_config.app_password
        
        # Establish a secure session with Gmail's outgoing SMTP server using TLS
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()

        # Login to the sender's email account
        server.login(sender_email, app_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
    finally:
        # Terminate the SMTP session
        server.quit()








# Import the Flask class from the flask module

import mail_config
# Create an instance of the Flask class
app = Flask(__name__)

# Define a route and the function to be executed when the route is accessed
@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/mail', methods=['POST'])
def mailSend():
  #Form data

  name = request.form['name']
  client_mail_id = request.form['email']
  country = request.form['country']
  cname = request.form['cname']
  affiliation = request.form['affiliation']
  role = request.form['role']
  message = request.form['message']

  # Now you can use these variables as needed


  #welcome message to client
   
  welcome_subject = mail_config.welcome_email_subject
  welcome_message_body=mail_config.welcome_email

  send_email(client_mail_id,welcome_subject, welcome_message_body)

  #mail send to admin
  admin_subject = mail_config.register_email
  admin_message_body = f"""
    
    Hello Admin,<br>
    <br>
    A new user has successfully registered. Here are the details:<br>
    <br>
    Name: {name} <br>
    Email: {client_mail_id} <br>
    country: {country} <br>
    Contact Name: {cname} <br>
    Affiliation: {affiliation} <br>
    Role: {role} <br>
    Message: {message} <br>
    <br>
    <br>
    Thanks <br>
    Good Turn
    """
  send_email(client_mail_id,admin_subject, admin_message_body,reply=True,reply_to_email=client_mail_id)

    
  return "success"

# Run the application if the script is executed directly
if __name__ == '__main__':
  app.run(debug=True)
