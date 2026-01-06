SENDER = "your-sender@example.com"    # Sender of the email; fills "From" field
RECIPIENTS = ("you@example.com")   # Recipient(s) of the email; fills "To" field
KEY = "your_password"    # Fills password argument of smtplib.login; needed to login to SMTP server
SUBJECT = "System Monitor"    # Fills the subject line of the email
WAIT = 3600    # Number of seconds to wait before main loop runs again