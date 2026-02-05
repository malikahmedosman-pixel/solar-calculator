import streamlit as st

# إعداد الصفحة لتناسب الهاتف
st.set_page_config(page_title="المساعد الكهربائي الشامل", page_icon="⚡", layout="centered")

# --- قاعدة بيانات الكابلات القياسية (mm2 -> Amps) ---
# هذه قيم تقريبية للكابلات النحاسية داخل المواسير
CABLES_DB = {
    1.5: 16, 2.5: 20, 4: 27, 6: 34, 10: 48, 
    16: 66, 25: 88, 35: 110, 50: 135, 70: 175
}

# --- القائمة الجانبية ---
st.sidebar.header("🔧 القائمة الرئيسية")
mode = st.sidebar.radio("اختر القسم:", ["توزيع كهربائي (Cables & CB)", "طاقة متجددة (Solar & UPS)"])

st.title("👷‍♂️ المساعد الكهربائي الشامل")

# ================= القسم الأول: التوزيع الكهربائي =================
if mode == "توزيع كهربائي (Cables & CB)":
    st.subheader("تصميم القواطع والكابلات")
    
    col1, col2 = st.columns(2)
    with col1:
        power = st.number_input("القدرة (وات W)", value=5000, step=100)
        voltage = st.selectbox("الجهد (Volt)", [220, 380, 400, 415])
    with col2:
        pf = st.number_input("معامل القدرة (PF)", 0.5, 1.0, 0.85)
        phase = st.radio("النظام", ["1-Phase", "3-Phase"])

    # زر الحساب
    if st.button("حساب القاطع والكابل"):
        # 1. حساب التيار
        if phase == "1-Phase":
            current = power / (voltage * pf)
        else:
            current = power / (1.732 * voltage * pf)
        
        # 2. حساب القاطع (معامل أمان 1.25)
        cb_amp = current * 1.25
        
        # 3. اختيار الكابل المناسب آلياً
        selected_cable = "غير متوفر (تيار عالٍ جداً)"
        for size, amp_capacity in CABLES_DB.items():
            if amp_capacity >= cb_amp: # الكابل يجب أن يتحمل تيار القاطع
                selected_cable = f"{size} mm²"
                break
        
        # عرض النتائج
        st.success(f"⚡ تيار الحمل الفعلي: {current:.2f} أمبير")
        st.info(f"🛡️ القاطع المقترح (Circuit Breaker): {cb_amp:.1f} أمبير (أو أقرب قياس تجاري)")
        st.warning(f"🔌 مقطع الكابل النحاسي المقترح: {selected_cable}")
        st.caption("ملاحظة: حساب الكابل مبني على السعة التياريه فقط (Ampacity) دون حساب هبوط الجهد والمسافة.")

# ================= القسم الثاني: الطاقة المتجددة =================
else:
    st.subheader("أنظمة الطاقة والبطاريات")
    tab1, tab2 = st.tabs(["☀️ منظومة شمسية", "🔋 نظام UPS"])

    # --- تبويب الطاقة الشمسية ---
    with tab1:
        load_kwh = st.number_input("الاستهلاك اليومي (KWh)", value=15.0)
        sun_h = st.slider("ساعات الشمس (Peak Hours)", 3.0, 8.0, 5.5)
        panel_w = st.selectbox("قدرة اللوح الواحد (W)", [300, 450, 550, 600])
        
        if st.button("احسب الألواح"):
            # معادلة: (الاستهلاك * 1.3 فواقد) / ساعات الشمس = قدرة المصفوفة
            array_watt = (load_kwh * 1000 * 1.3) / sun_h
            panels_count = round(array_watt / panel_w)
            if panels_count < 1: panels_count = 1
            
            st.metric(label="عدد الألواح المطلوبة", value=f"{panels_count} لوح")
            st.write(f"إجمالي قدرة المصفوفة: {panels_count * panel_w / 1000} كيلو وات")

    # --- تبويب الـ UPS ---
    with tab2:
        st.write("حساب زمن النسخ الاحتياطي (Backup Time)")
        ups_load_w = st.number_input("حمل الأجهزة (Watt)", value=300)
        batt_v = st.selectbox("جهد البطارية (V)", [12, 24, 48])
        batt_ah = st.number_input("سعة البطارية (Ah)", value=100)
        batt_qty = st.number_input("عدد البطاريات", value=1, step=1)
        
        if st.button("احسب وقت التشغيل"):
            # الطاقة الكلية = جهد * سعة * عدد * كفاءة (0.8) * عمق تفريغ (0.7)
            total_energy_wh = (batt_v * batt_ah * batt_qty) * 0.8 * 0.7
            hours = total_energy_wh / ups_load_w
            
            st.success(f"🕒 الزمن المتوقع للتشغيل: {hours:.2f} ساعة")
            st.caption("تم احتساب كفاءة وعمق تفريغ للحفاظ على عمر البطاريات.")

