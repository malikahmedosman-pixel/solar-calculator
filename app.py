import streamlit as st

# إعداد القائمة الجانبية للتنقل
st.sidebar.title("القائمة الهندسية")
choice = st.sidebar.radio("اختر الحاسبة:", ["حاسبة القواطع الكهربائية", "حاسبة الطاقة الشمسية"])

# --- القسم الأول: حاسبة القواطع ---
if choice == "حاسبة القواطع الكهربائية":
    st.title("🛡️ مصمم القواطع الكهربائية (CB)")
    
    col1, col2 = st.columns(2)
    with col1:
        power = st.number_input("القدرة (وات W)", value=1000)
        voltage = st.selectbox("الجهد (فولت V)", [220, 380, 400, 415])
    with col2:
        pf = st.slider("معامل القدرة (PF)", 0.5, 1.0, 0.8)
        phase = st.radio("نوع الطور", ["أحادي الطور (1ph)", "ثلاثي الطور (3ph)"])

    # الحسابات الهندسية
    if phase == "أحادي الطور (1ph)":
        current = power / (voltage * pf)
    else:
        current = power / (1.732 * voltage * pf)
    
    cb_size = current * 1.25 # إضافة معامل أمان 25%

    if st.button("حساب سعة القاطع"):
        st.subheader(f"التيار الفعلي: {current:.2f} أمبير")
        st.success(f"سعة القاطع المقترحة (أدنى حد): {cb_size:.2f} أمبير")
        st.warning("ملاحظة: اختر أقرب سعة تجارية أعلى من هذه القيمة (مثلاً: 16A, 20A, 32A...).")

# --- القسم الثاني: حاسبة الطاقة الشمسية ---
else:
    st.title("⚡ حاسبة الطاقة الشمسية")
    daily_load = st.number_input("الاستهلاك اليومي (KWh)", value=10.0)
    sun_hours = st.slider("ساعات الذروة الشمسية", 3.0, 8.0, 5.0)
    panel_watt = st.selectbox("قدرة اللوح (Watt)", [350, 400, 450, 550])
    
    num_panels = round(((daily_load * 1.2) / sun_hours) * 1000 / panel_watt)
    
    if st.button("احسب عدد الألواح"):
        st.success(f"تحتاج تقريباً إلى: {num_panels} لوح شمسي")
