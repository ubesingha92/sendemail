import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# Gmail SMTP configuration
SMTP_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
SMTP_PORT = 587  # Port for sending email via Gmail
EMAIL_ADDRESS = 'your_email@gmail.com'  # Replace with your Gmail email address
EMAIL_PASSWORD = 'your_app_password'  # Replace with your Gmail password or app-specific password

# Read the CSV file (modify path as needed)
csv_file = 'email_data.csv'  # Replace with the path to your CSV file
data = pd.read_csv(csv_file)  # Read CSV with default comma delimiter

# Function to send emails
def send_email(name, recipient_email, pdf_filename):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = f"Important Document for {name}"  # Set a custom subject

    # Customize the email body
    body = f"""
    Dear {name},

    Please find the attached PDF file named '{pdf_filename}'.

    If you have any questions or need further information, feel free to reach out.

    Best regards,
    [Your Name / Your Organization]
    """
    msg.attach(MIMEText(body, 'plain'))  # Set 'plain' for a text email or 'html' for HTML email

    # Attach the PDF file
    try:
        with open(pdf_filename, 'rb') as file:
            attach = MIMEApplication(file.read(), _subtype='pdf')
            attach.add_header('Content-Disposition', f'attachment; filename="{pdf_filename}"')
            msg.attach(attach)
    except FileNotFoundError:
        print(f"File {pdf_filename} not found. Skipping this email.")
        return

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login to Gmail account
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())  # Send email
            print(f"Email sent successfully to {recipient_email}")
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# Loop through each row in the CSV file and send emails
for index, row in data.iterrows():
    send_email(row['name'], row['email'], row['file_name'])
