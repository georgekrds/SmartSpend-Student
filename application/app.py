from flask import Flask, request, render_template, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO

app = Flask(__name__)

DATA_PATH = 'static/database.json'

@app.route('/')
def index():
    return render_template('index.html')  # Φροντίστε να υπάρχει το index.html με φόρμα επιλογών

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    selected_city = data.get('city')
    selected_categories = data.get('categories', [])

    # Ανάγνωση δεδομένων από JSON
    try:
        df = pd.read_json(DATA_PATH)
    except Exception as e:
        return jsonify({'error': f'Could not load data: {e}'}), 500

    # Φιλτράρισμα για την επιλεγμένη πόλη
    city_data = df[df['LOCATION'].str.lower() == selected_city.lower()]
    if city_data.empty:
        return jsonify({'error': 'City not found'}), 404

    # Συλλογή επιλεγμένων δεδομένων και υπολογισμός κόστους
    total = 0
    values = {}
    for category in selected_categories:
        value = city_data[category.upper()].values[0]
        if pd.notna(value):
            values[category] = round(float(value), 2)
            total += float(value)

    # Δημιουργία γραφήματος
    fig, ax = plt.subplots()
    ax.bar(values.keys(), values.values(), color='skyblue')
    ax.set_title(f'Μηνιαίο Κόστος για {selected_city}')
    ax.set_ylabel('Ευρώ')
    plt.xticks(rotation=45)

    # Αποθήκευση σε προσωρινό buffer
    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
