from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "contacts.db")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact Manager</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f8; padding: 35px; }
        .container { max-width: 950px; margin: auto; background: white; padding: 25px; border-radius: 6px; }
        h1 { text-align: center; color: #263b53; }
        form { display: flex; gap: 8px; margin-bottom: 20px; }
        input { padding: 10px; border: 1px solid #ccc; border-radius: 4px; min-width: 0; flex: 1; }
        button { padding: 9px 14px; border: 0; border-radius: 4px; cursor: pointer; }
        .primary { background: #2878b5; color: white; }
        .edit { background: #e7a33e; color: #222; }
        .delete { background: #c74646; color: white; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 11px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background: #e9eff5; }
        .actions { display: flex; gap: 6px; }
        @media (max-width: 700px) {
            body { padding: 10px; }
            form { flex-direction: column; }
            table { font-size: 12px; }
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Contact Manager</h1>
    <p style="text-align:center;">Version 2 — Edit and Delete Contacts</p>

    <h3>Add New Contact</h3>
    <form method="POST" action="/add">
        <input name="name" placeholder="Name" required>
        <input name="phone" placeholder="Phone Number" required>
        <input name="email" type="email" placeholder="Email Address" required>
        <button class="primary">Add Contact</button>
    </form>

    <h3>Contact List</h3>
    <table>
        <tr>
            <th>ID</th><th>Name</th><th>Phone</th><th>Email</th><th>Actions</th>
        </tr>
        {% for c in contacts %}
        <tr>
            <td>{{ c.id }}</td>
            <td>{{ c.name }}</td>
            <td>{{ c.phone }}</td>
            <td>{{ c.email }}</td>
            <td>
                <div class="actions">
                    <form method="GET" action="/edit/{{ c.id }}">
                        <button class="edit">Edit</button>
                    </form>
                    <form method="POST" action="/delete/{{ c.id }}"
                          onsubmit="return confirm('Delete this contact?')">
                        <button class="delete">Delete</button>
                    </form>
                </div>
            </td>
        </tr>
        {% else %}
        <tr><td colspan="5">No contacts added yet.</td></tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""

EDIT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Edit Contact</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f8; padding: 35px; }
        .container { max-width: 500px; margin: auto; background: white; padding: 25px; }
        input { box-sizing: border-box; width: 100%; padding: 10px; margin: 8px 0; }
        button { padding: 10px 16px; background: #2878b5; color: white; border: 0; cursor: pointer; }
    </style>
</head>
<body>
<div class="container">
    <h2>Edit Contact</h2>
    <form method="POST">
        <input name="name" value="{{ c.name }}" required>
        <input name="phone" value="{{ c.phone }}" required>
        <input name="email" type="email" value="{{ c.email }}" required>
        <button type="submit">Save Changes</button>
    </form>
    <p><a href="/">Back to Contact List</a></p>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    with get_db() as conn:
        contacts = conn.execute("SELECT * FROM contacts ORDER BY id").fetchall()
    return render_template_string(HTML, contacts=contacts)

@app.route("/add", methods=["POST"])
def add_contact():
    with get_db() as conn:
        conn.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (request.form["name"].strip(),
             request.form["phone"].strip(),
             request.form["email"].strip())
        )
    return redirect("/")

@app.route("/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    with get_db() as conn:
        contact = conn.execute(
            "SELECT * FROM contacts WHERE id = ?", (contact_id,)
        ).fetchone()

        if contact is None:
            return "Contact not found", 404

        if request.method == "POST":
            conn.execute(
                "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
                (request.form["name"].strip(),
                 request.form["phone"].strip(),
                 request.form["email"].strip(),
                 contact_id)
            )
            return redirect("/")

    return render_template_string(EDIT_HTML, c=contact)

@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    with get_db() as conn:
        conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    return redirect("/")

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
