import streamlit as st

st.title("⚡ حاسبة المهندس الكهربائي للطاقة الشمسية")
st.write("أدخل البيانات للحصول على عدد الألواح التقريبي")

daily_load = st.number_input("إجمالي الاستهلاك اليومي (كيلو وات ساعة)", value=10.0)
sun_hours = st.slider("ساعات الذروة الشمسية في منطقتك", 3.0, 8.0, 5.0)
panel_watt = st.selectbox("قدرة اللوح الواحد (وات)", [350, 400, 450, 550])

total_watt_needed = (daily_load * 1.2) / sun_hours 
num_panels = round((total_watt_needed * 1000) / panel_watt)

if st.button("احسب الآن"):
    st.success(f"تحتاج تقريباً إلى: {num_panels} لوح شمسي")
    st.info("تم إضافة 20% كمعامل فقد طبيعي في المنظومة.")
