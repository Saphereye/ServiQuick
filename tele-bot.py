import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
sender_email = "f20211511@hyderabad.bits-pilani.ac.in"
sender_password = "201301@noida"
receiver_email = "nowiram108@gekme.com"
subject = "Test Email Subject"
message_text = "This is a test email sent from Python."

# Create a MIME object for the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the message text to the email
message.attach(MIMEText(message_text, "plain"))

# Connect to the SMTP server (for Gmail, use "smtp.gmail.com")
smtp_server = "smtp.gmail.com"
smtp_port = 587

try:
    # Create an SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    
    # Start TLS encryption
    server.starttls()
    
    # Login to your email account
    server.login(sender_email, sender_password)
    
    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())
    
    print("Email sent successfully!")
    
except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Quit the SMTP server
    server.quit()
