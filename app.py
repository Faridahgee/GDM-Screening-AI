# app.py - FINAL CORRECTED VERSION
import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="GDM Early Screening AI", layout="wide")
st.title("🤖 AI GDM Risk Screening")
st.markdown("*First-Trimester Clinical Decision Support*")

# ============================================
# STEP 1: LOAD MODEL
# ============================================
# Your files are in the CURRENT folder (C:\Users\user\Desktop\Project)
# We look for them directly, NOT in a "models" subfolder.
MODEL_PATH = "calibrated_ensemble.pkl"

if not os.path.exists(MODEL_PATH):
    st.error(f"❌ CRITICAL ERROR: Model file not found in the current folder.")
    st.info(f"Please ensure '{MODEL_PATH}' is in: {os.getcwd()}")
    st.stop()

try:
    # Load the model
    model = joblib.load(MODEL_PATH)
    
    # Verify file size to confirm it's healthy
    size_mb = os.path.getsize(MODEL_PATH) / 1e6
    st.success(f"✅ Model loaded successfully! (Size: {size_mb:.1f} MB)")
    
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# ============================================
# STEP 2: SIDEBAR INPUTS
# ============================================
st.sidebar.header("Patient Inputs (≤13 weeks)")

age = st.sidebar.slider("Age (years)", 18, 45, 30, 1)
bmi = st.sidebar.slider("Pre-pregnancy BMI", 16.0, 45.0, 26.0, 0.5)
glucose = st.sidebar.slider("Fasting Glucose (mg/dL)", 60, 150, 85, 1)
sbp = st.sidebar.slider("Systolic BP (mmHg)", 80, 160, 115, 1)
dbp = st.sidebar.slider("Diastolic BP (mmHg)", 50, 100, 75, 1)
parity = st.sidebar.slider("Parity", 0, 6, 1, 1)
prior_gdm = st.sidebar.checkbox("Prior GDM history")
family_hx = st.sidebar.checkbox("Family history of T2DM")
ethnicity = st.sidebar.selectbox("Ethnicity", ["White", "Black", "Hispanic", "Asian"])

# ============================================
# STEP 3: PREDICTION
# ============================================
if st.sidebar.button("Calculate Risk"):
    try:
        # Define feature columns
        FEATURE_COLS = [
            'age', 'bmi', 'fasting_glucose', 'systolic_bp', 'diastolic_bp', 
            'parity', 'prior_gdm', 'prior_macrosomia', 'family_history_t2dm', 'ethnicity'
        ]
        
        # Build input DataFrame
        input_data = {
            'age': [float(age)], 'bmi': [float(bmi)], 'fasting_glucose': [float(glucose)],
            'systolic_bp': [float(sbp)], 'diastolic_bp': [float(dbp)], 'parity': [int(parity)],
            'prior_gdm': [int(prior_gdm)], 'prior_macrosomia': [0], 
            'family_history_t2dm': [int(family_hx)], 'ethnicity': [str(ethnicity)]
        }
        df = pd.DataFrame(input_data)[FEATURE_COLS]
        
        # Get probability
        prob = float(model.predict_proba(df)[0, 1])
        
        # ️ UPDATED THRESHOLD (from 0.5 to 0.309)
        optimal_threshold = 0.269
        pred = int(prob >= optimal_threshold)
        
        # Display results
        col1, col2 = st.columns(2)
        with col1:
            st.metric("GDM Risk Probability", f"{prob:.1%}")
            
            if prob < 0.20:
                st.success("🟢 Low Risk")
                st.info("Recommendation: Routine OGTT at 24-28w")
            elif prob < 0.40:
                st.warning("🟡 Moderate Risk")
                st.info("Recommendation: Lifestyle counseling + early monitoring")
            else:
                st.error("🔴 High Risk")
                st.info("Recommendation: Refer to MFM specialist + early OGTT")
        
        with col2:
            st.subheader("⚠️ Clinical Disclaimer")
            st.caption("Support tool only. Final diagnosis requires OGTT & physician evaluation.")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.caption("Prototype for academic evaluation • SaMD Class II Decision Support • Наггайи Фарида 6.4.02")