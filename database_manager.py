import sqlite3

def setup_complex_system():
    conn = sqlite3.connect('shield_pro.db')
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS patients")
    cursor.execute('''
    CREATE TABLE patients (
        id_number TEXT PRIMARY KEY,
        name TEXT, age INTEGER, blood_type TEXT, insurance TEXT,
        chronic_diseases TEXT, allergies TEXT, current_medications TEXT,
        last_visits TEXT, emergency_contact TEXT,
        location TEXT, dispatch_msg TEXT, protocol_id TEXT
    )
    ''')

    cursor.execute("DROP TABLE IF EXISTS protocols")
    cursor.execute('''
    CREATE TABLE protocols (
        id TEXT PRIMARY KEY,
        title TEXT,
        diagnosis_criteria TEXT,
        full_protocol TEXT -- دمجنا الـ BLS و ACLS هنا كما طلبت
    )
    ''')

    # تعبئة كيسات معقدة (واقعية جداً)
    patients = [
        # حالة سعودي - جلطة قلبية مع تاريخ مرضي طويل
        ('1022334455', 'Sultan Al-Otaibi', 68, 'A+', 'Tawuniya - Diamond', 
         'Type 2 Diabetes, Hypertension, Chronic Kidney Disease (Stage 3), Prior CABG (2019)', 
         'Sulfa Drugs, Shellfish', 
         'Metformin 500mg, Lisinopril 20mg, Atorvastatin 40mg, Clopidogrel 75mg', 
         '1. 2025-12-10: CHF Exacerbation | 2. 2025-10-05: Hyperglycemia | 3. 2025-08-12: Routine Follow-up', 
         '+966 50 111 2233', 
         'King Fahd Road - Near Kingdom Tower', 
         '68Y male, crushing chest pain radiating to jaw, diaphoretic, HR 110, BP 160/95.', 'C-1'),

        # حالة مقيم (Resident) - سكتة دماغية
        ('2334455667', 'John Smith (Resident)', 52, 'O-', 'Bupa - Gold', 
         'Atrial Fibrillation (A-Fib), Hyperlipidemia', 
         'Penicillin', 
         'Warfarin (Coumadin), Digoxin, Fenofibrate', 
         '1. 2025-11-20: Palpitations | 2. 2025-09-15: INR Adjustment', 
         '+966 55 444 5566', 
         'Jeddah - Al Hamra District', 
         '52Y male, sudden right-sided weakness, slurred speech, onset 45 mins ago.', 'M-1')
    ]
    cursor.executemany("INSERT INTO patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", patients)

    # بروتوكولات الهلال الأحمر كاملة (Full Protocol)
    protocols = [
        ('C-1', 'Acute Coronary Syndrome (ACS)', 
         'Retrosternal chest pressure, radiation to left arm/jaw, diaphoresis, nausea, exertional dyspnea.', 
         '1. Immediate 12-lead ECG (Target < 10 mins). 2. Oxygen if SpO2 < 94%. 3. Aspirin 324mg (Chewed). 4. Nitroglycerin 0.4mg SL every 5 mins (Max 3 doses) IF SBP > 90. 5. Early STEMI Notification to PCI Center.'),
         
        ('M-1', 'Suspected Stroke / TIA', 
         'Facial drooping, arm drift, abnormal speech (FAST), blood glucose check to rule out hypoglycemia.', 
         '1. Check BG immediately. 2. Determine "Last Known Well" time. 3. Maintain SpO2 > 94%. 4. Establish IV access (Avoid fluid bolus). 5. Elevated head to 30 degrees. 6. Rapid transport to designated Stroke Center. 7. Do NOT give Aspirin.')
    ]
    cursor.executemany("INSERT INTO protocols VALUES (?,?,?,?)", protocols)

    conn.commit()
    conn.close()
    print("✅ System initialized with Complex Cases and Full Protocols!")

setup_complex_system()