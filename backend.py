from flask import Flask, request, jsonify, render_template

from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (for learning)

# Create the SQLite DB if not exists
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
@app.route('/')
def home():
    return render_template('design.html')

@app.route('/api/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    notes = [{'id': row[0], 'content': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Note added successfully'})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Note deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
