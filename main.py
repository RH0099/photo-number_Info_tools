from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.secret_key = "supersecretkey"

# যদি আপলোড ফোল্ডার না থাকে, তাহলে তৈরি করো
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# হোম পেজ (Drawer Interface)
@app.route('/')
def index():
    return render_template('index.html')

# 📷 ফটো আপলোড ও প্রসেসিং ফিচার
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files['photo']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # এখানে আমরা AI বা OSINT API ব্যবহার করতে পারি (ডেমো স্ক্র্যাপিং)
            info = scrape_info(file_path)

            return render_template('upload.html', filename=filename, info=info)

    return render_template('upload.html')

# 📞 নাম্বার দিয়ে অনলাইন তথ্য বের করা
@app.route('/number_search', methods=['GET', 'POST'])
def number_search():
    info = None
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        if phone_number:
            info = scrape_number(phone_number)
    
    return render_template('number_search.html', info=info)

# 🌍 ছবি থেকে ডেটা স্ক্র্যাপিং (ডেমো)
def scrape_info(image_path):
    return {
        "Name": "John Doe",
        "Facebook": "https://facebook.com/johndoe",
        "LinkedIn": "https://linkedin.com/in/johndoe",
        "Twitter": "https://twitter.com/johndoe"
    }

# 📞 ফোন নম্বর স্ক্যানিং (ডেমো)
def scrape_number(phone):
    return {
        "WhatsApp": f"https://api.whatsapp.com/send?phone={phone}",
        "Facebook": f"https://www.facebook.com/search/top?q={phone}",
        "Telegram": f"https://t.me/{phone}"
    }

if __name__ == '__main__':
    app.run(debug=True)
