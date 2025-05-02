from flask import Flask, jsonify, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import psycopg2
import psycopg2.extras
import io
import base64
from matplotlib.figure import Figure
import numpy as np
from configparser import ConfigParser

app = Flask(__name__)

# Φόρτωση των ρυθμίσεων από το config.ini
def config(filename='database.ini', section='postgresql'):
    # Δημιουργία parser
    parser = ConfigParser()
    # Ανάγνωση αρχείου ρυθμίσεων
    parser.read(filename)
    
    # Παίρνουμε τις ρυθμίσεις για το section που ζητήθηκε
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Η ενότητα {section} δεν βρέθηκε στο αρχείο {filename}')
    
    return db

# Σύνδεση με τη βάση δεδομένων PostgreSQL
def connect_to_db():
    """ Σύνδεση με τη βάση δεδομένων PostgreSQL """
    conn = None
    try:
        # Φόρτωση παραμέτρων σύνδεσης
        params = config()
        
        # Σύνδεση με τη βάση
        print('Σύνδεση με τη βάση δεδομένων PostgreSQL...')
        conn = psycopg2.connect(**params)
        
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Σφάλμα κατά τη σύνδεση με τη βάση: {error}")
        # Αν αποτύχει η σύνδεση, επιστρέφουμε None
        return None

# Εναλλακτική σύνδεση με hardcoded παραμέτρους (για δοκιμές)
def connect_to_db_direct():
    """ Εναλλακτική σύνδεση με απευθείας παραμέτρους """
    try:
        # Αντικατέστησε με τα δικά σου στοιχεία σύνδεσης
        conn = psycopg2.connect(
            host="localhost",
            database="smartspend",
            user="postgres",
            password="your_password"
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Σφάλμα κατά τη σύνδεση με τη βάση: {error}")
        return None

# Ανάκτηση δεδομένων από τη βάση
def get_city_data():
    """ Ανάκτηση πληροφοριών για τις πόλεις """
    conn = connect_to_db()
    if conn is None:
        return pd.DataFrame()
    
    try:
        # Δημιούργησε ένα cursor
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Εκτέλεσε το query
        cur.execute("SELECT * FROM cities")
        
        # Ανάκτηση αποτελεσμάτων
        rows = cur.fetchall()
        
        # Μετατροπή σε DataFrame
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        
        # Κλείσιμο cursor και σύνδεσης
        cur.close()
        
        return df
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Σφάλμα κατά την ανάκτηση δεδομένων πόλεων: {error}")
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()

def get_expense_data():
    """ Ανάκτηση δεδομένων εξόδων """
    conn = connect_to_db()
    if conn is None:
        return pd.DataFrame()
    
    try:
        # Δημιούργησε ένα cursor
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Εκτέλεσε το query για τα έξοδα
        cur.execute("""
            SELECT e.expense_id, e.city_id, c.city_name, e.category, 
                   e.subcategory, e.amount, e.date_recorded 
            FROM expenses e
            JOIN cities c ON e.city_id = c.city_id
        """)
        
        # Ανάκτηση αποτελεσμάτων
        rows = cur.fetchall()
        
        # Μετατροπή σε DataFrame
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        
        # Κλείσιμο cursor και σύνδεσης
        cur.close()
        
        return df
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Σφάλμα κατά την ανάκτηση δεδομένων εξόδων: {error}")
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()

# Ανάλυση δεδομένων
def analyze_expenses():
    """ Ανάλυση δεδομένων εξόδων και επιστροφή των αποτελεσμάτων """
    expenses_df = get_expense_data()
    
    if expenses_df.empty:
        return {
            "error": "Δεν βρέθηκαν δεδομένα εξόδων"
        }
    
    # Μετατροπή τύπων δεδομένων αν χρειάζεται
    expenses_df['amount'] = pd.to_numeric(expenses_df['amount'], errors='coerce')
    expenses_df['date_recorded'] = pd.to_datetime(expenses_df['date_recorded'], errors='coerce')
    
    # Δημιουργία λεξικού για την αποθήκευση των αποτελεσμάτων
    results = {}
    
    # 1. Υπολογισμός μέσου όρου εξόδων ανά κατηγορία και πόλη
    avg_by_category_city = expenses_df.groupby(['city_name', 'category'])['amount'].mean().reset_index()
    results['avg_by_category_city'] = avg_by_category_city.to_dict(orient='records')
    
    # 2. Υπολογισμός ελάχιστων και μέγιστων εξόδων ανά κατηγορία
    min_expenses = expenses_df.groupby(['category'])['amount'].min().reset_index()
    max_expenses = expenses_df.groupby(['category'])['amount'].max().reset_index()
    results['min_expenses'] = min_expenses.to_dict(orient='records')
    results['max_expenses'] = max_expenses.to_dict(orient='records')
    
    # 3. Συνολικά έξοδα ανά πόλη
    total_by_city = expenses_df.groupby('city_name')['amount'].sum().reset_index()
    results['total_by_city'] = total_by_city.sort_values('amount', ascending=False).to_dict(orient='records')
    
    # 4. Μέσο μηνιαίο κόστος ανά πόλη
    # Χωρίζουμε τα δεδομένα ανά μήνα, αν τα δεδομένα μας έχουν ημερομηνίες
    if 'date_recorded' in expenses_df.columns:
        expenses_df['month'] = expenses_df['date_recorded'].dt.to_period('M')
        monthly_by_city = expenses_df.groupby(['city_name', 'month'])['amount'].sum().reset_index()
        avg_monthly_by_city = monthly_by_city.groupby('city_name')['amount'].mean().reset_index()
        results['avg_monthly_by_city'] = avg_monthly_by_city.sort_values('amount', ascending=False).to_dict(orient='records')
    
    # 5. Κατανομή εξόδων στις κατηγορίες
    category_distribution = expenses_df.groupby('category')['amount'].sum().reset_index()
    results['category_distribution'] = category_distribution.to_dict(orient='records')
    
    # 6. Σύγκριση πόλεων για συγκεκριμένες κατηγορίες
    city_category_comparison = {}
    for category in expenses_df['category'].unique():
        category_data = expenses_df[expenses_df['category'] == category]
        city_avg = category_data.groupby('city_name')['amount'].mean().reset_index()
        city_category_comparison[category] = city_avg.sort_values('amount', ascending=False).to_dict(orient='records')
    
    results['city_category_comparison'] = city_category_comparison
    
    return results

# Δημιουργία γραφημάτων
def create_monthly_cost_chart():
    """ Δημιουργία γραφήματος για το μέσο μηνιαίο κόστος ανά πόλη """
    expenses_df = get_expense_data()
    
    if expenses_df.empty:
        return None
    
    # Μετατροπή τύπων δεδομένων
    expenses_df['amount'] = pd.to_numeric(expenses_df['amount'], errors='coerce')
    expenses_df['date_recorded'] = pd.to_datetime(expenses_df['date_recorded'], errors='coerce')
    
    # Δημιουργία μηνιαίων δεδομένων
    expenses_df['month'] = expenses_df['date_recorded'].dt.to_period('M')
    monthly_by_city = expenses_df.groupby(['city_name', 'month'])['amount'].sum().reset_index()
    avg_monthly_by_city = monthly_by_city.groupby('city_name')['amount'].mean().reset_index()
    avg_monthly_by_city = avg_monthly_by_city.sort_values('amount', ascending=False)
    
    # Περιορισμός στις πρώτες 10 πόλεις για καλύτερη οπτικοποίηση
    if len(avg_monthly_by_city) > 10:
        avg_monthly_by_city = avg_monthly_by_city.head(10)
    
    # Δημιουργία του γραφήματος
    plt.figure(figsize=(12, 6))
    sns.barplot(x='city_name', y='amount', data=avg_monthly_by_city)
    plt.title('Μέσο Μηνιαίο Κόστος ανά Πόλη')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Πόλη')
    plt.ylabel('Μέσο Κόστος (€)')
    plt.tight_layout()
    
    # Αποθήκευση του γραφήματος σε buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Κωδικοποίηση του γραφήματος σε base64 για εμφάνιση στο HTML
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{image_base64}'

def create_category_distribution_chart():
    """ Δημιουργία γραφήματος για την κατανομή των εξόδων ανά κατηγορία """
    expenses_df = get_expense_data()
    
    if expenses_df.empty:
        return None
    
    # Μετατροπή τύπων δεδομένων
    expenses_df['amount'] = pd.to_numeric(expenses_df['amount'], errors='coerce')
    
    # Κατανομή εξόδων στις κατηγορίες
    category_distribution = expenses_df.groupby('category')['amount'].sum()
    
    # Δημιουργία του γραφήματος πίτας
    plt.figure(figsize=(10, 8))
    plt.pie(category_distribution, labels=category_distribution.index, 
            autopct='%1.1f%%', startangle=90)
    plt.title('Κατανομή Εξόδων ανά Κατηγορία')
    plt.axis('equal')
    plt.tight_layout()
    
    # Αποθήκευση του γραφήματος σε buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Κωδικοποίηση του γραφήματος σε base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{image_base64}'

def create_category_city_heatmap():
    """ Δημιουργία heatmap για το κόστος ανά κατηγορία και πόλη """
    expenses_df = get_expense_data()
    
    if expenses_df.empty:
        return None
    
    # Μετατροπή τύπων δεδομένων
    expenses_df['amount'] = pd.to_numeric(expenses_df['amount'], errors='coerce')
    
    # Υπολογισμός μέσου όρου εξόδων ανά κατηγορία και πόλη
    avg_by_category_city = expenses_df.groupby(['city_name', 'category'])['amount'].mean().reset_index()
    
    # Μετατροπή σε pivot table για heatmap
    heatmap_data = avg_by_category_city.pivot(index='city_name', columns='category', values='amount')
    
    # Δημιουργία του heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title('Μέσο Κόστος ανά Κατηγορία και Πόλη')
    plt.tight_layout()
    
    # Αποθήκευση του γραφήματος σε buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Κωδικοποίηση του γραφήματος σε base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{image_base64}'

# Flask routes
@app.route('/')
def index():
    """Αρχική σελίδα της εφαρμογής"""
    # Ανάλυση δεδομένων
    analysis_results = analyze_expenses()
    
    # Δημιουργία γραφημάτων
    monthly_cost_chart = create_monthly_cost_chart()
    category_distribution_chart = create_category_distribution_chart()
    category_city_heatmap = create_category_city_heatmap()
    
    # Απόδοση του template με τα δεδομένα
    return render_template('index.html',
                           analysis_results=analysis_results,
                           monthly_cost_chart=monthly_cost_chart,
                           category_distribution_chart=category_distribution_chart,
                           category_city_heatmap=category_city_heatmap)

@app.route('/api/expenses')
def get_expenses_api():
    """API endpoint για τα δεδομένα εξόδων"""
    analysis_results = analyze_expenses()
    return jsonify(analysis_results)

@app.route('/api/cities')
def get_cities_api():
    """API endpoint για τα δεδομένα πόλεων"""
    cities_df = get_city_data()
    if cities_df.empty:
        return jsonify({"error": "Δεν βρέθηκαν δεδομένα πόλεων"})
    return jsonify(cities_df.to_dict(orient='records'))

@app.route('/api/compare/<city1>/<city2>')
def compare_cities(city1, city2):
    """API endpoint για τη σύγκριση δύο πόλεων"""
    expenses_df = get_expense_data()
    
    if expenses_df.empty:
        return jsonify({"error": "Δεν βρέθηκαν δεδομένα εξόδων"})
    
    # Μετατροπή τύπων δεδομένων
    expenses_df['amount'] = pd.to_numeric(expenses_df['amount'], errors='coerce')
    
    # Φιλτράρισμα δεδομένων για τις δύο πόλεις
    city1_data = expenses_df[expenses_df['city_name'] == city1]
    city2_data = expenses_df[expenses_df['city_name'] == city2]
    
    if city1_data.empty or city2_data.empty:
        return jsonify({"error": "Μία ή και οι δύο πόλεις δεν βρέθηκαν"})
    
    # Σύγκριση μέσου όρου εξόδων ανά κατηγορία
    city1_avg = city1_data.groupby('category')['amount'].mean().reset_index()
    city2_avg = city2_data.groupby('category')['amount'].mean().reset_index()
    
    # Συνολικός μέσος όρος εξόδων
    city1_total_avg = city1_data['amount'].mean()
    city2_total_avg = city2_data['amount'].mean()
    
    # Συνδυασμός αποτελεσμάτων
    comparison = {
        "city1": {
            "name": city1,
            "average_total": city1_total_avg,
            "average_by_category": city1_avg.to_dict(orient='records')
        },
        "city2": {
            "name": city2,
            "average_total": city2_total_avg,
            "average_by_category": city2_avg.to_dict(orient='records')
        },
        "difference_percent": ((city1_total_avg - city2_total_avg) / city2_total_avg) * 100 if city2_total_avg > 0 else 0
    }
    
    return jsonify(comparison)

@app.route('/city/<city_name>')
def city_detail(city_name):
    """Σελίδα με λεπτομέρειες για συγκεκριμένη πόλη"""
    expenses_df = get_expense_data()
    
    if expenses_df.empty:
        return render_template('city_detail.html', 
                              city_name=city_name, 
                              error="Δεν βρέθηκαν δεδομένα εξόδων")
    
    # Μετατροπή τύπων δεδομένων
    expenses_df['amount'] = pd.to_numeric(expenses_df['amount'], errors='coerce')
    
    # Φιλτράρισμα δεδομένων για τη συγκεκριμένη πόλη
    city_data = expenses_df[expenses_df['city_name'] == city_name]
    
    if city_data.empty:
        return render_template('city_detail.html', 
                              city_name=city_name, 
                              error="Η πόλη δεν βρέθηκε στα δεδομένα")
    
    # Υπολογισμός στατιστικών
    avg_by_category = city_data.groupby('category')['amount'].mean().reset_index()
    total_avg = city_data['amount'].mean()
    
    # Δημιουργία γραφήματος για την κατανομή εξόδων της πόλης
    plt.figure(figsize=(10, 8))
    category_data = city_data.groupby('category')['amount'].sum()
    plt.pie(category_data, labels=category_data.index, 
            autopct='%1.1f%%', startangle=90)
    plt.title(f'Κατανομή Εξόδων στην πόλη {city_name}')
    plt.axis('equal')
    plt.tight_layout()
    
    # Αποθήκευση του γραφήματος σε buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Κωδικοποίηση του γραφήματος σε base64
    city_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return render_template('city_detail.html', 
                          city_name=city_name,
                          avg_by_category=avg_by_category.to_dict(orient='records'),
                          total_avg=total_avg,
                          city_chart=f'data:image/png;base64,{city_chart}')

# Εκτέλεση της εφαρμογής 
if __name__ == '__main__':
    # Δημιουργία φακέλου templates αν δεν υπάρχει
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Εκτέλεση της εφαρμογής Flask σε debug mode
    app.run(debug=True)
