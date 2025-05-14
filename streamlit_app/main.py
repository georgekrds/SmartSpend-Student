import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Προσαρμογή ρυθμίσεων σελίδας
st.set_page_config(
    page_title="SmartSpend Student",
    page_icon="https://raw.githubusercontent.com/georgekrds/SmartSpend-Student/main/streamlit_app/logo.png",
    layout="centered"
)

# Τίτλος
st.markdown("""
    <div style='display: flex; align-items: center; justify-content: center; gap: 10px; padding: 1rem;'>
        <img src='https://raw.githubusercontent.com/georgekrds/SmartSpend-Student/main/streamlit_app/favicon.png' width='100'>
        <h1 style='margin: 0;'>SmartSpend Student</h1>
    </div>
    <h4 style='text-align: center; color: gray;'>Προσωπικός Σύμβουλος Μηνιαίου Προϋπολογισμού Φοιτητή</h4>
    <hr style='border: 1px solid #ccc;'>
""", unsafe_allow_html=True)

# Φόρτωση δεδομένων JSON
file_path = Path("costs.json")
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

cities = [item["LOCATION"] for item in data]
selected_city = st.selectbox("📍 Επιλογή πόλης", cities)

budget = st.number_input("💰 Μηνιαίος προϋπολογισμός (€)", min_value=0, value=300, step=20)

# Επιλογή κατηγοριών εξόδων
st.markdown("### 🛍️ Επιλογή εξόδων για υπολογισμό:")
default_categories = ["FOOD", "TRANSPORTATION", "ENTERTAINMENT", "SUPERMARKET", "BILLS", "STUDENT_RESTAURANT"]
category_labels = {
    "FOOD": "🍽️ Φαγητό έξω",
    "TRANSPORTATION": "🚌 Μεταφορές",
    "ENTERTAINMENT": "🎭 Διασκέδαση",
    "SUPERMARKET": "🛒 Σούπερ Μάρκετ",
    "BILLS": "💡 Λογαριασμοί",
    "STUDENT_RESTAURANT": "🧑‍🎓 Φοιτητική Λέσχη"
}

selected_categories = []
city_data = next((item for item in data if item["LOCATION"] == selected_city), None)
for cat in default_categories:
    if cat == "FOOD":
        label = f"{category_labels[cat]} ({city_data[cat]}€/μέρα)"
    else:
        label = f"{category_labels[cat]} ({city_data[cat]}€)"
    if st.checkbox(label, value=True):
        selected_categories.append(cat)

# Επιπλέον επιλογή για Φαγητό
days_out = 0
if "FOOD" in selected_categories:
    st.markdown("##### 🍴 Πόσες μέρες την εβδομάδα τρως έξω;")
    days_out = st.slider("", min_value=0, max_value=7, value=2)

# Ανάκτηση δεδομένων για την επιλεγμένη πόλη
city_data = next((item for item in data if item["LOCATION"] == selected_city), None)

# Υπολογισμός κόστους
cost_items = {}
for cat in selected_categories:
    cost = city_data[cat]
    if cat == "FOOD":
        daily_cost = cost
        cost = (daily_cost * days_out * 4)
    cost_items[cat] = cost

total_cost = sum(cost_items.values())

# Κανονικοποίηση κόστους αν ξεπερνά τον προϋπολογισμό
adjusted_cost_items = {}
if budget < total_cost:
    ratio = budget / total_cost
    for k, v in cost_items.items():
        adjusted_cost_items[k] = round(v * ratio, 2)
else:
    adjusted_cost_items = cost_items

# Μπάρα προϋπολογισμού
st.markdown("### 🧾 Επαρκεί ο προϋπολογισμός σου;")
percentage = budget / total_cost if total_cost > 0 else 0
bar_percentage = min(percentage, 1.0) * 100
st.progress(bar_percentage / 100, text=f"{budget}€ / {round(total_cost, 2)}€")

if percentage >= 1:
    st.success("✅ Ο προϋπολογισμός σου επαρκεί!")
else:
    st.warning("⚠️ Ο προϋπολογισμός σου είναι χαμηλότερος από το μέσο κόστος.")

# Διάγραμμα
remaining = budget - sum(adjusted_cost_items.values())
categories = [category_labels[c] for c in adjusted_cost_items.keys()]
costs = list(adjusted_cost_items.values())

if remaining > 0:
    categories.append("💶 Υπολειπόμενο")
    costs.append(round(remaining, 2))

df_chart = pd.DataFrame({
    "Κατηγορία": categories,
    "Κόστος (€)": costs
})


fig = px.pie(df_chart, values="Κόστος (€)", names="Κατηγορία", title="Κατανομή κόστους ανά κατηγορία")
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)

# Συμβουλές
st.markdown("### 💡 Συμβουλές εξοικονόμησης:")
tips = []
if "FOOD" in selected_categories:
    tips.append("🍱 Σκέψου να μειώσεις τις μέρες που τρως έξω ή να μαγειρεύεις στο σπίτι.")
if "STUDENT_RESTAURANT" in selected_categories:
    tips.append("🧑‍🎓 Αξιοποίησε την μηνιαία συνδρομή στη φοιτητική λέσχη.")
if "TRANSPORTATION" in selected_categories:
    tips.append("🚍 Αγόρασε μηνιαία κάρτα απεριορίστων διαδρομών για έκπτωση.")
if "SUPERMARKET" in selected_categories:
    tips.append("🛒 Κάνε λίστα για τα ψώνια και εκμεταλλεύσου τις προσφορές.")
if "ENTERTAINMENT" in selected_categories:
    tips.append("🎬 Προτίμησε φοιτητικές εκπτώσεις ή δωρεάν εκδηλώσεις.")
if "BILLS" in selected_categories:
    tips.append("💡 Μείωσε κατανάλωση ρεύματος και νερού με έξυπνες πρακτικές.")

for tip in tips:
    st.markdown(f"- {tip}")

# Υποσέλιδο
st.markdown("""
---
<div style='text-align: center;'>
    <img src='https://raw.githubusercontent.com/georgekrds/SmartSpend-Student/main/streamlit_app/logo.png' width='80'>
    <p style='margin-top: 10px;'>
        <strong>Εργασία Python 2ου Εξαμήνου</strong><br>
        <a href='https://ionio.gr' target='_blank'>Ιόνιο Πανεπιστήμιο</a><br><br>
        <strong>Sigma Budget Masters</strong><br>
        Βαν Σλότεν Σταυρούλα (inf2024025)<br>
        Καρύδης Γεώργιος - Εδουάρδος (inf2024072)<br>
        Λειβαδιώτης Νικόλαος (inf2024101)<br>
        Τζώρτζης Κωνσταντίνος (inf2024168)<br><br>
        <a href='https://github.com/georgekrds/SmartSpend-Student/tree/main' target='_blank'>🔗 GitHub Project Link</a>
    </p>
</div>
""", unsafe_allow_html=True)
