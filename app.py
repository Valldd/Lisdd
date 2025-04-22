from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

users = {}

tasks = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('signup.html')

@app.route('/submit_login', methods=['POST'])
def submit_login():
    email = request.form['email']
    password = request.form['password']

    if email in users and users[email] == password:
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid email or password', 'danger')
        return redirect(url_for('login'))

@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash('Passwords do not match', 'danger')
        return redirect(url_for('register'))

    if email in users:
        flash('Email already exists', 'danger')
        return redirect(url_for('register'))

    users[email] = password
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('login'))

@app.route('/lupa_password')
def lupa_password():
    return render_template('lupa_password.html')

@app.route('/submit_lupa_password', methods=['POST'])
def submit_lupa_password():
    email = request.form['email']
    flash('Password reset instructions have been sent to your email.', 'success')
    return redirect(url_for('login'))

@app.route('/add_task')
def add_task():
    return render_template('add_task.html')

@app.route('/submit_add_task', methods=['POST'])
def submit_add_task():
    task_name = request.form['task_name']
    task_description = request.form['task_description']
    task_status = request.form['task_status']
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "name": task_name, "description": task_description, "status": task_status})
    flash('Task added successfully.', 'success')
    return redirect(url_for('task_list'))

@app.route('/task_list')
def task_list():
    return render_template('task_list.html', tasks=tasks)

@app.route('/edit_task/<int:task_id>')
def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return render_template('edit_task.html', task=task)
    else:
        flash('Task not found.', 'danger')
        return redirect(url_for('task_list'))

@app.route('/submit_edit_task/<int:task_id>', methods=['POST'])
def submit_edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task['name'] = request.form['task_name']
        task['description'] = request.form['task_description']
        task['status'] = request.form['task_status']
        flash('Task updated successfully.', 'success')
    else:
        flash('Task not found.', 'danger')
    return redirect(url_for('task_list'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('task_list'))

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/submit_search', methods=['POST'])
def submit_search():
    query = request.form['query']
    results = [t for t in tasks if query.lower() in t['name'].lower() or query.lower() in t['description'].lower()]
    return render_template('search_results.html', query=query, results=results)

@app.route('/mark_task/<int:task_id>/<status>')
def mark_task(task_id, status):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task['status'] = status
        flash('Task status updated successfully.', 'success')
    else:
        flash('Task not found.', 'danger')
    return redirect(url_for('task_list'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)