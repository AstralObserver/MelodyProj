from flask import Flask, Blueprint, render_template, request, redirect, url_for
from __init__ import create_app  # Import the create_app function from __init__.py

app = create_app()  # Create and configure the app

@app.route('/')
def index():
    return about()

@app.route('/about')
def about(error=None):
    return render_template('about.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)