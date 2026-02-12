import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# دالة لبناء القاعدة تلقائياً على ريندر إذا كانت مفقودة
def init_db_on_render():
    conn = sqlite3.connect('shield_pro.db')
    cursor = conn.cursor()
    # بناء الجداول (المرضى والبروتوكولات)
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
        id_number TEXT PRIMARY KEY, name TEXT, age INTEGER, blood_type TEXT, 
        insurance TEXT, chronic_diseases TEXT, allergies TEXT, 
        current_medications TEXT, last_visits TEXT, emergency_contact TEXT,
        location TEXT, dispatch_msg TEXT, protocol_id TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS protocols (
        id TEXT PRIMARY KEY, title TEXT, diagnosis_criteria TEXT, full_protocol TEXT)''')
    
    # إضافة "الكيسات" المعقدة التي طلبتها (سلطان وجون سميث)
    cases = [
        ('1022334455', 'Sultan Al-Otaibi', 68, 'A+', 'Tawuniya - Diamond', 
         'Type 2 Diabetes, Hypertension, CKD', 'Sulfa Drugs', 'Metformin, Lisinopril', 
         '2025-12-10: CHF Exacerbation', '+966 50 111 2233', 'King Fahd Road', 
         '68Y male, crushing chest pain, diaphoretic.', 'C-1'),
        ('2334455667', 'John Smith', 52, 'O-', 'Bupa - Gold', 'A-Fib', 'Penicillin', 
         'Warfarin', '2025-11-20: Palpitations', '+966 55 444 5566', 'Jeddah', 
         '52Y male, sudden right-sided weakness.', 'M-1')
    ]
    cursor.executemany("INSERT OR REPLACE INTO patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", cases)

    # إضافة بروتوكولات CPGs كاملة
    protocols = [
        ('C-1', 'Acute Coronary Syndrome (ACS)', 'Chest pressure, radiation to jaw, diaphoresis.', 
         '12-lead ECG < 10 mins. Aspirin 324mg (Chewed). NTG 0.4mg SL if SBP > 90..'),
        ('M-1', 'Suspected Stroke', 'FAST Positive, slurred speech.', 
         'Check BG. Determine Last Known Well. Elevated head 30 deg. Transport to Stroke Center.')
    ]
    cursor.executemany("INSERT OR REPLACE INTO protocols VALUES (?,?,?,?)", protocols)
    
    conn.commit()
    conn.close()

# تشغيل البناء عند بداية تشغيل السيرفر
init_db_on_render()

@app.route('/')
def index():
    return render_template('identify.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    p_id = request.form.get('patient_id')
    conn = sqlite3.connect('shield_pro.db')
    cursor = conn.cursor()
    # الربط بين الجدولين
    query = """
    SELECT p.*, pr.title, pr.diagnosis_criteria, pr.full_protocol 
    FROM patients p 
    JOIN protocols pr ON p.protocol_id = pr.id 
    WHERE p.id_number = ?
    """
    cursor.execute(query, (p_id,))
    res = cursor.fetchone()
    conn.close()
    
    if res:
        return render_template('dashboard.html', d=res)
    return render_template('identify.html', error="ID not found")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)