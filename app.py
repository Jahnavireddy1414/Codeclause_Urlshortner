from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

# Base62 characters
BASE62 = string.ascii_letters + string.digits

# Dictionary to store URL mappings
url_mapping = {}

# Function to generate a random short URL key
def generate_short_key(length=6):
    return ''.join(random.choice(BASE62) for _ in range(length))

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']  # Get the long URL from the form
        if long_url:
            short_key = generate_short_key()
            while short_key in url_mapping:  # Ensure the key is unique
                short_key = generate_short_key()
            url_mapping[short_key] = long_url
            short_url = f"http://localhost:5000/{short_key}"
            return render_template('index.html', short_url=short_url)
    return render_template('index.html', short_url=None)

# Route to retrieve the original URL using the short URL
@app.route('/<short_key>')
def redirect_to_url(short_key):
    long_url = url_mapping.get(short_key)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
