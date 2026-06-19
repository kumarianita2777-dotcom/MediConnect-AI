import streamlit as st
import pandas as pd
import pickle
import sklearn
import sqlite3

# --- DATABASE SETUP ---
def create_table():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS patient_records(Age INTEGER, Glucose INTEGER, BloodPressure INTEGER, BMI REAL, Pregnancies INTEGER, SkinThickness INTEGER, Insulin INTEGER, DPF REAL, Result TEXT)')
    conn.commit()
    conn.close()

def add_data(age, glucose, bp, bmi, pregnancies, skin, insulin, dpf, result):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('INSERT INTO patient_records VALUES (?,?,?,?,?,?,?,?,?)', (age, glucose, bp, bmi, pregnancies, skin, insulin, dpf, result))
    conn.commit()
    conn.close()

create_table()

# 1. Page Configuration
st.set_page_config(page_title="MediConnect AI", page_icon="🏥", layout="wide")

# 2. Main Heading
st.title("%s MediConnect: Diabetes Risk Dashboard" % "🩺")

# Disclaimer and Note
st.warning("⚠️ **Disclaimer:** This project is only for educational and learning purposes. It should not be used as a substitute for professional medical advice.")
st.info("ℹ️ **Note:** Please ensure all medical parameters are entered accurately for the best results.")
st.markdown("---")

# 3. Model Load karna
try:
    model = pickle.load(open('diabetes_model.pkl', 'rb'))
    model_loaded = True
except Exception as e:
    st.error(f"⚠️ Model is not loaded yet! (failed). Error: {e}")
    model_loaded = False

# --- SECTION 1: INPUT AREA ---
st.subheader("📋 Step 1: Enter Patient Details")

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
if st.button("Check AI Prediction 🚀", use_container_width=True):
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
            st.error("🚨 **High Risk Detected:** This patient has a high probability of having Diabetes.")
            st.warning("""
            **💡 Personalized Preventive Suggestions:**
            * Consult a doctor immediately for further medical advice.
            * Avoid sugar and high-carb diets.
            * Start regular physical exercise or daily walking.
            """)
        else:
            result_status = "Healthy"
            st.success("✅ **Healthy:** The patient is perfectly fine. No significant risk of Diabetes detected.")
            st.info("""
            **💡 Personalized Preventive Suggestions:**
            * Maintain a balanced diet and a healthy lifestyle.
            * Get regular blood sugar checkups every 6 months.
            """)
            
        add_data(age, glucose, blood_pressure, bmi, pregnancies, skin_thickness, insulin, dpf, result_status)
        st.toast("💾 Patient Data successfully saved on database!", icon='✅')

    else:
        st.warning("Model is not loaded, please check the file.")

st.markdown("---")

# --- SECTION 4: VIEW DATABASE ---
st.subheader("📁 Digital Register (Patient Database)")
st.markdown("Here you can view the saved data of all previous patients:")
if st.checkbox("View Database table"):
    conn = sqlite3.connect('patients.db')
    df_db = pd.read_sql_query("SELECT * FROM patient_records", conn)
    st.dataframe(df_db, use_container_width=True)
    conn.close()

# --- SECTION 5: FOOTER DISCLAIMER ---
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This project is only for educational and learning purposes. It should not be used as a substitute for professional medical advice.")
