import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIG & CUSTOM MEDICAL CSS ---
st.set_page_config(page_title="NCRH CD-DSS", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004b87; color: white; }
    h1, h2, h3 { color: #004b87; font-family: 'Helvetica', sans-serif; }
    .patient-card { padding: 20px; border-radius: 10px; background-color: white; border-left: 5px solid #004b87; margin-bottom: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY & LOGIN STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = ""
    st.session_state['username'] = ""

# --- SIDEBAR LOGIC ---
st.sidebar.markdown("## 🏥 NCRH PORTAL")

if not st.session_state['logged_in']:
    role_input = st.sidebar.selectbox("User Role", ["Select Role", "Doctor", "Nurse", "Admin"], key="login_role")
    user_input = st.sidebar.text_input("Staff ID", key="login_user")
    pass_input = st.sidebar.text_input("Security Key", type="password", key="login_pass")
    
    if st.sidebar.button("Login"):
        if role_input != "Select Role" and user_input and pass_input:
            st.session_state['logged_in'] = True
            st.session_state['role'] = role_input
            st.session_state['username'] = user_input
            st.rerun()
        else:
            st.sidebar.error("Please enter all credentials")
else:
    st.sidebar.success(f"Authenticated: {st.session_state['role']}")
    st.sidebar.write(f"Logged in as: {st.session_state['username']}")
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- 3. MAIN APP LOGIC ---
if st.session_state['logged_in']:
    current_role = st.session_state['role']
    current_user = st.session_state['username']

    # Professional Header Banner
    st.markdown(f"""
        <div style="background-color:#004b87;padding:15px;border-radius:10px;margin-bottom:25px;">
            <h2 style="color:white;text-align:center;margin:0;">Nairobi Central Referral Hospital | CD-DSS</h2>
            <p style="color:white;text-align:center;margin:0;">User: {current_role} {current_user} | Clinical Session Active</p>
        </div>
    """, unsafe_allow_html=True)

    # --- SECTION 1: PATIENT REGISTRATION ---
    st.markdown('<div class="patient-card"><h3>📋 1. Patient Registration & Vitals</h3></div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        p_name = st.text_input("Patient Full Name", placeholder="Enter official name...", key="main_pname")
    with col_b:
        p_id = st.text_input("Hospital ID (MRN)", placeholder="NCRH-XXXX", key="main_pid")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        age = st.number_input("Age", 0, 120, value=25, key="main_age")
    with m2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="main_gender")
    with m3:
        temp = st.text_input("Temp (°C)", "36.5", key="main_temp")
    with m4:
        bp = st.text_input("BP (mmHg)", "120/80", key="main_bp")

    allergies = st.text_input("Known Drug Allergies", placeholder="e.g. Penicillin", key="main_allergies")

    st.divider()

    # --- SECTION 2: CLINICAL PRESENTATION ---
    st.markdown('<div class="patient-card"><h3>🩺 2. Clinical Presentation</h3></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        symptoms = st.multiselect("Select Presenting Symptoms", 
                                   ["Fever", "Cough", "Chest Pain", "Headache", "Excessive Thirst", "Blurred Vision"],
                                   key="main_symptoms")
    with c2:
        lab_results = st.selectbox("Laboratory/Radiology Findings", 
                                    ["Pending", "Normal", "Abnormal X-ray", "Positive Malaria Test", "High Blood Sugar (HbA1c)"],
                                    key="main_lab")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 3: INFERENCE ENGINE ---
    if st.button("🚀 EXECUTE DIAGNOSTIC ANALYSIS"):
        if not p_name or not p_id:
            st.error("Missing Data: Please enter Patient Name and ID.")
        else:
            st.markdown(f"### 📊 Diagnostic Dashboard for {p_name}")
            suggestions = []

            # Logic Engine
            if "Fever" in symptoms and "Cough" in symptoms and "Chest Pain" in symptoms and lab_results == "Abnormal X-ray":
                suggestions.append({"Diagnosis": "Pneumonia", "Prob": "85%", "Protocol": "WHO Respiratory Guidelines"})
            
            if "Fever" in symptoms and "Headache" in symptoms and lab_results == "Positive Malaria Test":
                suggestions.append({"Diagnosis": "Malaria", "Prob": "95%", "Protocol": "National Malaria Standards"})
                
            if "Excessive Thirst" in symptoms and lab_results == "High Blood Sugar (HbA1c)":
                suggestions.append({"Diagnosis": "Diabetes Mellitus", "Prob": "90%", "Protocol": "Chronic Care Manual"})

            # Results Display
            if suggestions:
                for s in suggestions:
                    st.info(f"**Possible Diagnosis: {s['Diagnosis']} ({s['Prob']} Probability)**")
                    st.caption(f"Evidence-Based Protocol: {s['Protocol']}")
                
                if allergies:
                    st.error(f"⚠️ **CONTRAINDICATION ALERT:** Patient allergic to {allergies}. Verify treatment plan.")
            else:
                st.warning("Insufficient clinical data for automated suggestion. Refer to Senior Consultant.")

else:
    st.info("Welcome to the NCRH CD-DSS. Please use the portal on the left to authenticate.")