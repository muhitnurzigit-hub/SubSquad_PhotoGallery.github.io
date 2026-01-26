import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'fll_secret_key'
ADMIN_PASSWORD = "SubSquadCA" 
UPLOAD_FOLDER = 'static/photos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def user_view():
    photos = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', photos=photos)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
    if session.get('logged_in'):
        photos = os.listdir(UPLOAD_FOLDER)
        return render_template('admin.html', photos=photos)
    return '''<form method="post">Пароль: <input type="password" name="password"><input type="submit" value="Войти"></form>'''

@app.route('/upload', methods=['POST'])
def upload():
    if session.get('logged_in') and 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('admin'))

@app.route('/delete/<filename>')
def delete_file(filename):
    if filename in ['cover.jpg', 'background.jpg']:
        return redirect(url_for('admin'))
        
    if session.get('logged_in'):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host='0.0.0.0', port=port)