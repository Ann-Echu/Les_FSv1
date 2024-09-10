import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

def send_email(subject, message, sender_email, sender_name, receiver_email):
    try:
        # Set up the email parameters
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        
        # Attach the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login to your email account
        server.login(sender_email, 'YOUR_EMAIL_PASSWORD')
        
        # Send the email
        server.send_message(msg)
        server.quit()
        
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Contact Us")

    with st.form(key='contact_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            # Validate email
            try:
                validate_email(email)
                # Send the email
                response = send_email(subject, message, email, name, 'RECEIVER_EMAIL')
                st.success(response)
            except EmailNotValidError as e:
                st.error(str(e))
