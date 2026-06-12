import streamlit as st
import pandas as pd
import pickle
import sklearn
import sqlite3

# --- DATABASE SETUP ---
# Database file aur table create karne ka function
def create_table():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    # SQL query: Table banane ke liye
    c.execute('CREATE TABLE IF NOT EXISTS patient_records(Age INTEGER, Glucose INTEGER, BloodPressure INTEGER, BMI REAL, Pregnancies INTEGER, SkinThickness INTEGER, Insulin INTEGER, DPF REAL, Result TEXT)')
    conn.commit()
    conn.close()

# Database mein naya data insert karne ka function
def add_data(age, glucose, bp, bmi, pregnancies, skin, insulin, dpf, result):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    # SQL query: Data table mein dalne ke liye
    c.execute('INSERT INTO patient_records VALUES (?,?,?,?,?,?,?,?,?)', (age, glucose, bp, bmi, pregnancies, skin, insulin, dpf, result))
    conn.commit()
    conn.close()

# App shuru hote hi database setup ho jayega
create_table()

# 1. Page Configuration
st.set_page_config(page_title="MediConnect AI", page_icon="🏥", layout="wide")

# 2. Main Heading
st.title("🩺 MediConnect: Diabetes Risk Dashboard")
st.markdown("Niche diye gaye sliders se patient ka data enter karein.")
st.markdown("---")

# 3. Model Load karna
try:
    model = pickle.load(open('diabetes_model.pkl', 'rb'))
    model_loaded = True
except Exception as e:
    st.error(f"⚠️ Model load nahi ho paya. Error: {e}")
    model_loaded = False

# --- SECTION 1: INPUT AREA ---
st.subheader("📋 Step 1: Patient Details Enter Karein")

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    age = st.slider("Patient Age (Umar)", 1, 100, 25)
    glucose = st.slider("Glucose Level (Sugar)", 0, 250, 100)
    blood_pressure = st.slider("Blood Pressure", 0, 150, 80)
    bmi = st.slider("BMI (Body Mass Index)", 10.0, 60.0, 25.0)

with row1_col2:
    pregnancies = st.number_input("Number of Pregnancies", 0, 20, 0)
    skin_thickness = st.number_input("Skin Thickness (mm)", 0, 100, 20)
    insulin = st.number_input("Insulin Level (mu U/ml)", 0, 900, 30)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)

st.markdown("---")

# --- SECTION 2: HEALTH SNAPSHOT ---
st.subheader("📊 Step 2: Patient Health Snapshot")

m1, m2, m3, m4 = st.columns(4)
m1.metric(label="🩸 Glucose", value=f"{glucose} mg/dL")
m2.metric(label="⚖️ BMI", value=f"{bmi}")
m3.metric(label="🎂 Age", value=f"{age} Yrs")
m4.metric(label="🩺 BP", value=f"{blood_pressure}")

st.markdown("---")

# --- SECTION 3: PREDICTION & DATA SAVING ---
if st.button("AI Prediction Check Karein 🚀", use_container_width=True):
    if model_loaded:
        input_data = pd.DataFrame({
            'Pregnancies': [pregnancies], 'Glucose': [glucose], 'BloodPressure': [blood_pressure],
            'SkinThickness': [skin_thickness], 'Insulin': [insulin], 'BMI': [bmi],
            'DiabetesPedigreeFunction': [dpf], 'Age': [age]
        })
        
        prediction = model.predict(input_data)
        
        # Result set karna aur Data Save karna
        if prediction[0] == 1:
            result_status = "High Risk"
            st.error("🚨 **High Risk Detected:** Is patient ko Diabetes hone ke chances zyada hain.")
            st.warning("""
            **💡 Personalized Preventive Suggestions:**
            * Turant doctor se consult karein.
            * Sugar aur High-Carb diet se bachein.
            * Rozana workout/walking shuru karein.
            """)
        else:
            result_status = "Healthy"
            st.success("✅ **Healthy:** Patient bilkul theek hai. Diabetes ka koi bada risk nahi hai.")
            st.info("""
            **💡 Personalized Preventive Suggestions:**
            * Balanced diet aur healthy lifestyle maintain rakhein.
            * Har 6 mahine mein regular sugar test karwayein.
            """)
            
        # Database mein Patient ki detail SAVE kar rahe hain
        add_data(age, glucose, blood_pressure, bmi, pregnancies, skin_thickness, insulin, dpf, result_status)
        st.toast("💾 Patient Data successfully Database mein save ho gaya hai!", icon='✅')

    else:
        st.warning("Model load nahi hua hai, kripya file check karein.")

st.markdown("---")

# --- SECTION 4: VIEW DATABASE ---
st.subheader("📁 Digital Register (Patient Database)")
st.markdown("Yahan aap purane sabhi patients ka saved data dekh sakti hain:")

if st.checkbox("Database Table Dekhein"):
    conn = sqlite3.connect('patients.db')
    # SQL query se saara data utha rahe hain
    df_db = pd.read_sql_query("SELECT * FROM patient_records", conn)
    st.dataframe(df_db, use_container_width=True)
    conn.close()
