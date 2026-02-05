import streamlit as st

# إعداد القائمة الجانبية
st.sidebar.title("🛠️ منصة المهندس الكهربائي")
choice = st.sidebar.selectbox("اختر القسم الرئيسي:", 
                             ["حاسبة القواطع", "ركن الطاقة المتجددة والـ UPS"])

# --- القسم الأول: القواطع ---
if choice == "حاسبة القواطع":
    st.title("🛡️ تصميم القواطع الكهربائية")
    p = st.number_input("القدرة الكلية (Watt)", value=1000)
    v = st.selectbox("الجهد (Volt)", [220, 380, 400])
    phase = st.radio("الطور", ["1-Phase", "3-Phase"])
    
    # الحساب
    if phase == "1-Phase":
        i = p / (v * 0.8)
    else:
        i = p / (1.732 * v * 0.8)
    
    st.success(f"التيار: {i:.2f} A | القاطع المقترح: {i*1.25:.1f} A")

# --- القسم الثاني: الطاقة المتجددة والـ UPS ---
else:
    tab1, tab2 = st.tabs(["☀️ حسابات الشمسية", "🔋 حسابات الـ UPS"])
    
    with tab1:
        st.header("تصميم الألواح")
        load = st.number_input("الاستهلاك اليومي (kWh)", value=10.0)
        sun = st.slider("ساعات الذروة", 3.0, 8.0, 5.0)
        p_watt = st.selectbox("قدرة اللوح", [400, 450, 550])
        res = round((load * 1.2 * 1000) / (sun * p_watt))
        st.info(f"عدد الألواح المطلوبة: {res}")

    with tab2:
        st.header("تصميم نظام الـ UPS")
        ups_load = st.number_input("إجمالي حمل الأجهزة (Watt)", value=500)
        backup_time = st.number_input("ساعات التشغيل المطلوبة", value=4)
        battery_voltage = st.selectbox("جهد نظام البطاريات (V)", [12, 24, 48])
        
        # معادلة الـ UPS (Capacity Ah = (Load * Time) / (Voltage * Efficiency))
        # نعتبر الكفاءة 85% كمعيار هندسي
        capacity_ah = (ups_load * backup_time) / (battery_voltage * 0.85)
        
        st.subheader("النتيجة الهندسية:")
        st.write(f"تحتاج سعة بطاريات إجمالية لا تقل عن: **{capacity_ah:.1f} Ah**")
        st.warning(f"مثال: يمكنك استخدام بطاريتين سعة كل منهما {capacity_ah/2:.1f} Ah إذا كان النظام 24 فولت.")

