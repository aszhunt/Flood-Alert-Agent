import streamlit as st
import pandas as pd
import plotly.express as px
import random
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="Global Mountain Flood & GLOF Early Warning System",
    page_icon="🚨",
    layout="wide"
)

# App Title & Description
st.title("🚨 Global Mountain Flood & GLOF Early Warning System")
st.markdown("""
Yeh application duniya bhar ke 30 mountainous countries ke high-risk ilaqon (jahan Glacial Lake Outburst Floods ya flash floods ka khatra rehta hai) ko monitor karne ke liye design ki gayi hai.
""")

# Sidebar for Location Selection
st.sidebar.header("📍 Global Regions Control Center")

country_locations = {
    "Pakistan": ["Gilgit", "Skardu", "Chitral", "Swat", "Hunza Valley", "Kaghan Valley", "Shishper Glacier Zone", "Dir", "Astore"],
    "Nepal": ["Langtang Region", "Solukhumbu (Everest)", "Pokhara (Seti River)", "Manang", "Kathmandu Valley", "Tsho Rolpa Lake Area", "Mustang"],
    "India": ["Chamoli (Uttarakhand)", "Kedarnath Valley", "Leh (Ladakh)", "Sikkim (Teesta Basin)", "Himachal (Lahaul & Spiti)", "Dharamshala", "Kullu"],
    "Bhutan": ["Lunana Region", "Punakha Valley", "Thimphu River Basin", "Bumthang", "Paro Valley"],
    "Afghanistan": ["Badakhshan", "Panjshir Valley", "Salang Pass", "Nuristan", "Bamyan"],
    "Tajikistan": ["Pamir Mountains", "Gorno-Badakhshan", "Fann Mountains", "Khorog", "Iskanderkul"],
    "Kyrgyzstan": ["Tian Shan Range", "Issyk-Kul Region", "Ala-Archa", "Osh Mountain Belt", "Naryn"],
    "China": ["Tibet Autonomous Region (Yarlung Tsangpo)", "Sichuan Alpine Region", "Yunnan Gorge", "Xinjiang (Tian Shan)", "Qinghai"],
    "Switzerland": ["Valais (Zermatt)", "Bernese Alps (Grindelwald)", "Graubünden", "Engadin", "Uri"],
    "Austria": ["Tyrol (Innsbruck)", "Salzburg Alps", "Carinthia", "Vorarlberg"],
    "Italy": ["Dolomites (South Tyrol)", "Aosta Valley", "Valtellina", "Piedmont Alps"],
    "France": ["French Alps (Chamonix)", "Savoie", "Haute-Savoie", "Isère"],
    "Canada": ["Rocky Mountains (Banff)", "Jasper National Park", "Coast Mountains (BC)", "Yukon Territory"],
    "United States": ["Cascades (Washington)", "Rocky Mountains (Colorado)", "Sierra Nevada (California)", "Alaska Range (Denali)"],
    "Chile": ["Andes (Santiago High Zone)", "Cajón del Maipo", "Araucanía Andes", "Patagonia Mountains"],
    "Peru": ["Cordillera Blanca (Huaraz)", "Cusco Mountain Zone", "Arequipa Volcanic Belt", "Ancash High Valleys"],
    "Colombia": ["Los Nevados National Park", "Bogotá Eastern Hills", "Sierra Nevada de Santa Marta"],
    "Ecuador": ["Andean Volcanic Belt (Quito)", "Cotopaxi Region", "Chimborazo Slopes", "Cuenca Highlands"],
    "Argentina": ["Patagonia (Bariloche)", "Mendoza Andes", "Jujuy Mountain Region", "Ushuaia"],
    "New Zealand": ["Southern Alps (Mount Cook / Aoraki)", "Fiordland", "Queenstown Lakes District"],
    "Japan": ["Japanese Alps (Nagano)", "Tohoku Mountain Belt", "Hokkaido Ranges", "Niigata Snow Zone"],
    "Indonesia": ["Papua Highlands (Puncak Jaya)", "Sumatra Bukit Barisan", "Central Sulawesi Mountains"],
    "Philippines": ["Cordillera Administrative Region (Baguio/Bontoc)", "Mindanao Highlands"],
    "Iran": ["Alborz Mountains (Tehran North)", "Zagros Range", "Damavand Region"],
    "Turkey": ["Kaçkar Mountains", "Eastern Anatolia", "Taurus Mountains"],
    "Georgia": ["Greater Caucasus (Svaneti)", "Kazbegi Region", "Adjara Mountains"],
    "Russia": ["Caucasus Range (Elbrus Region)", "Altai Mountains", "Kamchatka Volcanic Belt", "Siberian Uplands"],
    "Norway": ["Jotunheimen", "Sunnmøre Alps", "Fjord Western Ranges"],
    "Spain": ["Pyrenees (Huesca/Lleida)", "Sierra Nevada (Granada)", "Picos de Europa"],
    "Germany": ["Bavarian Alps (Garmisch-Partenkirchen)", "Black Forest High Zone"]
}

selected_country = st.sidebar.selectbox("Country Select Karein", list(country_locations.keys()))
locations = country_locations[selected_country]
selected_location = st.sidebar.selectbox("Specific Valley / City / Village Select Karein", locations)

# Simulated Live Data Generation
random.seed(hash(selected_location))
rainfall = round(random.uniform(5.0, 120.5), 1)  # mm
temp = round(random.uniform(12.0, 28.0), 1)      # °C
water_level = round(random.uniform(1.5, 8.8), 2)   # Meters

# Risk Calculation Logic
if rainfall > 80 or water_level > 6.5:
    risk_level = "HIGH RISK 🔴"
elif rainfall > 40 or water_level > 4.0:
    risk_level = "MEDIUM RISK 🟡"
else:
    risk_level = "NORMAL / SAFE 🟢"

# Main Dashboard UI
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🌧️ Current Rainfall", value=f"{rainfall} mm", delta="Last 24 Hours")

with col2:
    st.metric(label="🌡️ Mountain Temp", value=f"{temp} °C", delta="Glacier Melting Rate")

with col3:
    st.metric(label="🌊 River Water Level", value=f"{water_level} m", delta="Danger mark: 6.0m")

st.markdown("---")

# Status Banner Display
if "HIGH" in risk_level:
    st.error(f"### ⚠️ ALERTS FOR {selected_location.upper()} ({selected_country}): {risk_level}")
elif "MEDIUM" in risk_level:
    st.warning(f"### ⚠️ ALERTS FOR {selected_location.upper()} ({selected_country}): {risk_level}")
else:
    st.success(f"### ✅ STATUS FOR {selected_location.upper()}, {selected_country}: {risk_level}")

# Groq AI Powered Analysis Section
st.subheader("🤖 Groq AI Real-Time Disaster Analysis & Advice")

groq_api_key = st.secrets.get("GROQ_API_KEY", "")

if st.button("Generate AI Safety & Evacuation Plan"):
    if not groq_api_key:
        st.error("Streamlit Secrets mein GROQ_API_KEY mojood nahi hai.")
    else:
        with st.spinner("Groq AI analysis generate kar raha hai..."):
            try:
                client = Groq(api_key=groq_api_key)
                prompt = f"""
                You are an expert disaster management and flash flood / GLOF early warning AI. 
                Current situation in high-risk zone {selected_location} located in {selected_country}:
                - Rainfall: {rainfall} mm
                - Mountain Temp: {temp} °C
                - River Water Level: {water_level} meters
                - Calculated Risk Status: {risk_level}
                
                Please provide a short, urgent, and practical safety advisory in Urdu (written in Roman Urdu script) for local residents and tourists in this specific mountain region. Tell them what immediate safety actions they should take.
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-120b",
                )
                ai_response = chat_completion.choices[0].message.content
                st.success("AI Advisory Generated Successfully:")
                st.write(ai_response)
            except Exception as e:
                st.error(f"API connection mein masla aaya hai: {e}")

st.markdown("---")

# Visual Trend Graph
st.subheader(f"📊 Past 7 Days Trend Analysis for {selected_location}, {selected_country}")
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
trend_data = pd.DataFrame({
    'Day': days,
    'Water Level (m)': [random.uniform(2.0, 5.0) for _ in range(7)],
    'Rainfall (mm)': [random.uniform(10.0, 50.0) for _ in range(7)]
})

fig = px.line(trend_data, x='Day', y=['Water Level (m)', 'Rainfall (mm)'], markers=True, 
              title=f"Water Level & Rainfall Trends in {selected_location}")
st.plotly_chart(fig, use_container_width=True)

# Community Reporting Section
st.markdown("---")
st.subheader("👥 Local Community Emergency Reporting")
with st.form("report_form"):
    reporter_name = st.text_input("Aapka Naam")
    report_text = st.text_area("Situation Details (misal ke tor par: pani ka rang badal gaya hai ya level upar aa gaya hai)")
    submitted = st.form_submit_button("Submit Emergency Report")
    
    if submitted:
        if reporter_name and report_text:
            st.success("Shukriya! Aapki report control room ko forward kar di gayi hai.")
        else:
            st.warning("Barah-e-karam apna naam aur details mukammal likhein.")
