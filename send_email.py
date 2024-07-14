import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_email_with_attachment(subject, body, to_email, attachment_path):
    # Set up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    # Login credentials for sending the email
    EMAIL_ADDRESS = st.secrets["credentials"]["USERNAME"]
    EMAIL_PASSWORD = st.secrets["credentials"]["PASSWORD"]


    # Login to the server
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = 'Bighnaraj Mohapatra'
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # Open the file to be sent
    attachment = open(attachment_path, "rb")
    
    # Instance of MIMEBase and named as p
    part = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    part.set_payload((attachment).read())
    
    # Encode into base64
    encoders.encode_base64(part)
    
    part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
    
    # Attach the instance 'part' to instance 'msg'
    msg.attach(part)
    
    # Send the message via the server
    server.send_message(msg)
    server.quit()
