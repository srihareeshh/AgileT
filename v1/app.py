
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

contacts = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact Manager</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 40px;
        }
        .container {
            max-width: 850px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 6px;
        }
        h1 { text-align: center; color: #263b53; }
        form { display: flex; gap: 10px; margin-bottom: 25px; }
        input {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            flex: 1;
            min-width: 0;
        }
        button {
            padding: 10px 16px;
            background: #2878b5;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        table { width: 100%; border-collapse: collapse; }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }
        th { background: #e9eff5; }
        @media (max-width: 650px) {
            body { padding: 12px; }
            form { flex-direction: column; }
            table { font-size: 13px; }
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Contact Manager</h1>
    <p style="text-align:center;">Version 1 — Add Contact</p>

    <h3>Add New Contact</h3>
    <form method="POST" action="/add">
        <input name="name" placeholder="Name" required>
        <input name="phone" placeholder="Phone Number" required>
        <input name="email" type="email" placeholder="Email Address" required>
        <button type="submit">Add Contact</button>
    </form>

    <h3>Contact List</h3>
    <table>
        <tr>
            <th>ID</th><th>Name</th><th>Phone</th><th>Email</th>
        </tr>
        {% for c in contacts %}
        <tr>
            <td>{{ c.id }}</td>
            <td>{{ c.name }}</td>
            <td>{{ c.phone }}</td>
            <td>{{ c.email }}</td>
        </tr>
        {% else %}
        <tr><td colspan="4">No contacts added yet.</td></tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, contacts=contacts)

@app.route("/add", methods=["POST"])
def add_contact():
    global next_id

    name = request.form["name"].strip()
    phone = request.form["phone"].strip()
    email = request.form["email"].strip()

    contacts.append({
        "id": next_id,
        "name": name,
        "phone": phone,
        "email": email
    })
    next_id += 1

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
