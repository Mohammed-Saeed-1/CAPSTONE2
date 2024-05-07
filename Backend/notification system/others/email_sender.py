# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email(subject, message, from_email, to_emails, smtp_server, smtp_port, smtp_username, smtp_password):
#     # Create a MIMEText object to represent the email message
#     msg = MIMEMultipart()
#     msg['From'] = from_email
#     msg['To'] = ', '.join(to_emails)
#     msg['Subject'] = subject

#     # Attach the message to the MIME object
#     msg.attach(MIMEText(message, 'plain'))

#     # Connect to the SMTP server
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()  # Secure the connection
#     server.login(smtp_username, smtp_password)

#     # Send the email
#     server.sendmail(from_email, to_emails, msg.as_string())

#     # Close the connection
#     server.quit()

# # Email configuration
# subject = "This is the subject part"
# message = "Hello There, how are you"
# from_email = "univmohammed@gmail.com"  # Replace with your email
# to_emails = ["mohammedaziz2060@gmail.com", "mohammedthabit4321@gmail.com"]  # List of recipient emails
# smtp_server = "smtp.example.com"  # Replace with your SMTP server address
# smtp_port = 587  # Replace with your SMTP port
# smtp_username = "your_username"  # Replace with your SMTP username
# smtp_password = "your_password"  # Replace with your SMTP password

# # Send the email
# send_email(subject, message, from_email, to_emails, smtp_server, smtp_port, smtp_username, smtp_password)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(employee_emails, message):

    company_email = 'utrade4321@gmail.com'
    password = 'rpgs phnw sqja ldkh'

    # Set up the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(company_email, password)

    # Compose the message
    msg = MIMEMultipart()
    msg['From'] = company_email
    msg['Subject'] = 'Hello'

    # Body of the email
    body = message

    # Add body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Send the email to each employee
    for employee_email in employee_emails:
        msg['To'] = employee_email
        smtp_server.sendmail(company_email, employee_email, msg.as_string())

    # Quit SMTP server
    smtp_server.quit()

employee_emails = ['univmohammed@gmail.com']
message = "Hello,\n\nThis is an automated message."
send_email(employee_emails, message)