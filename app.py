import streamlit as st
import pandas as pd
import pickle
import sklearn

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

# --- SECTION 1: INPUT AREA (Upar wala hissa) ---
st.subheader("📋 Step 1: Patient Details Enter Karein")

# Inputs ko 2 rows mein arrange kar rahe hain taaki screen zyada lambi na ho
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

# --- SECTION 2: HEALTH SNAPSHOT (Niche wala hissa) ---
st.subheader("📊 Step 2: Patient Health Snapshot")

# Metrics ko 4 columns mein ek row mein dikha rahe hain (Horizontal Row)
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="🩸 Glucose", value=f"{glucose} mg/dL")
m2.metric(label="⚖️ BMI", value=f"{bmi}")
m3.metric(label="🎂 Age", value=f"{age} Yrs")
m4.metric(label="🩺 BP", value=f"{blood_pressure}")

st.markdown("---")

# --- SECTION 3: PREDICTION RESULT (Sabse niche) ---
if st.button("AI Prediction Check Karein 🚀", use_container_width=True):
    if model_loaded:
        # Data prepare karna
        input_data = pd.DataFrame({
            'Pregnancies': [pregnancies], 'Glucose': [glucose], 'BloodPressure': [blood_pressure],
            'SkinThickness': [skin_thickness], 'Insulin': [insulin], 'BMI': [bmi],
            'DiabetesPedigreeFunction': [dpf], 'Age': [age]
        })
        
        prediction = model.predict(input_data)
        
        # Result Show karna
        if prediction[0] == 1:
            st.error("🚨 **High Risk Detected:** Is patient ko Diabetes hone ke chances zyada hain.")
            st.warning("""
            **💡 Personalized Preventive Suggestions:**
            * Turant doctor se consult karein.
            * Sugar aur High-Carb diet se bachein.
            * Rozana workout/walking shuru karein.
            """)
        else:
            st.success("✅ **Healthy:** Patient bilkul theek hai. Diabetes ka koi bada risk nahi hai.")
            st.info("""
            **💡 Personalized Preventive Suggestions:**
            * Balanced diet aur healthy lifestyle maintain rakhein.
            * Har 6 mahine mein regular sugar test karwayein.
            """)
    else:
        st.warning("Model load nahi hua hai, kripya file check karein.")