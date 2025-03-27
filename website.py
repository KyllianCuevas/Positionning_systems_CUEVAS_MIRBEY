#!/usr/bin/python3
'''
Created on 12-03-2024

@author: Kyllian Cuevas, Thomas Mirbey
@version: 1

Positioning System - Webpage tracking
'''

#------------------
# Import
#------------------

from flask import Flask, render_template_string, request, session
from collections import defaultdict

#------------------
# Variables
#------------------

app = Flask(__name__)
app.secret_key = 'some_token'

page_transitions = defaultdict(int)

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background: #00274D;
            color: white;
        }
        .container {
            max-width: 900px;
            margin: auto;
            background: #001F3F;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
            margin-top: 50px;
        }
        .top-right {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 14px;
            color: #CCCCCC;
        }
        .nav-links a {
            text-decoration: none;
            color: #1E90FF;
            margin: 0 10px;
            font-weight: bold;
        }
        .nav-links a:hover {
            text-decoration: underline;
        }
        h1, h2 {
            color: #1E90FF;
        }
    </style>
</head>
<body>
    <div class="top-right">Current Page: {{ title }}</div>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="nav-links">
            <a href="/">Home</a> | 
            <a href="/quit">Quit</a> | 
            <a href="/stats">Stats</a>
        </div>
        <ul class="nav-links" style="list-style-type: none; padding: 0;">
            <li><a href="/subject1">Smart Home Automation App - ECOM</a></li>
            <li><a href="/subject2">Hospital Network Deployment - AKAT</a></li>
        </ul>
        <div class="content mt-4">
            <p>{{ content }}</p>
        </div>
    </div>
</body>
</html>"""

#------------------
# Functions
#------------------

def track_page_transition(current_page):
    previous_page = session.get('previous_page', None)
    if previous_page:
        page_transitions[f"{previous_page} -> {current_page}"] += 1
    session['previous_page'] = current_page

@app.route('/')
def home():
    track_page_transition("Home")
    return render_template_string(template, title="Home", content="Welcome to the homepage.")

@app.route('/subject1')
def subject1():
    track_page_transition("Smart Home Automation App - ECOM")
    return render_template_string(template, title="Smart Home Automation App - ECOM", content="The ECOM Smart Home Automation App provides seamless integration of IoT devices, enabling users to remotely control lighting, security systems, and energy consumption through an intuitive mobile application. It ensures encrypted communication and AI-powered automation for an optimized living experience.")

@app.route('/subject2')
def subject2():
    track_page_transition("Hospital Network Deployment - AKAT")
    return render_template_string(template, title="Hospital Network Deployment - AKAT", content="The AKAT Hospital Network Deployment project focuses on building a secure and scalable IT infrastructure for healthcare facilities. It includes high-speed networking, real-time patient data synchronization, cybersecurity measures, and seamless integration with existing hospital management systems.")

@app.route('/quit')
def quit_page():
    track_page_transition("Quit")
    return "<h1>Goodbye!</h1><p>You have exited the application.</p>", 200

@app.route('/stats')
def stats():
    total_transitions = sum(page_transitions.values())
    table = """
    <html>
    <head>
        <title>Page Transition Stats</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-dark text-white text-center">
        <h1 class="mt-4">Page Transition Statistics</h1>
        <div class="container mt-4">
            <a href="/" class="btn btn-primary mb-3">Home</a>
            <table class="table table-dark table-bordered">
                <thead>
                    <tr>
                        <th>Transition</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
    """
    for transition, count in page_transitions.items():
        percentage = (count / total_transitions * 100) if total_transitions > 0 else 0
        table += f"<tr><td>{transition}</td><td>{count}</td><td>{percentage:.2f}%</td></tr>"
    
    table += """
                </tbody>
            </table>
            <p>Total Transitions: {}</p>
        </div>
    </body>
    </html>
    """.format(total_transitions)
    return table

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)