import pandas as pd
import streamlit as st
import joblib

class EnergyConsumptionApp:
    def __init__(self):
        # Page configuration
        st.set_page_config(
            page_title="Energy Consumption Analysis",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.setup_styles()
        self.render_header()
        self.render_sidebar()
        self.load_resources()

    def setup_styles(self):
        # Sidebar options for customization
        with st.sidebar:
            theme_mode = st.radio("Select Theme", ["Light", "Dark"])
            font_size = st.slider("Select Font Size", 12, 24, 16)
            header_gradient_start = st.color_picker("Header Gradient Start", "#6A11CB")
            header_gradient_end = st.color_picker("Header Gradient End", "#2575FC")
            card_gradient_start = st.color_picker("Card Gradient Start", "#6A11CB")
            card_gradient_end = st.color_picker("Card Gradient End", "#2575FC")
            
        # Apply theme styles
        bg_color = "#FFFFFF" if theme_mode == "Light" else "#333333"
        text_color = "#000000" if theme_mode == "Light" else "#FFFFFF"

        # Inject CSS styles
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {bg_color};
                color: {text_color};
                font-size: {font_size}px;
                font-family: 'Arial', sans-serif;
            }}
            .stApp h3{{
                color:{text_color};
            }}
            .header {{
                text-align: center;
                background: linear-gradient(to right, {header_gradient_start}, {header_gradient_end});
                padding: 20px;
                border-radius: 12px;
                margin: 20px 0;
                font-size: {font_size + 10}px;
                font-weight: bold;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                color: #FFFFFF;
            }}
            .card {{
                background: linear-gradient(to right, {card_gradient_start}, {card_gradient_end});
                padding: 10px;
                border-radius: 12px;
                margin: 20px 0;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                color: white;
                text-align: center;
            }}
            .stButton>button {{
                background: linear-gradient(to right, #3B82F6, #06B6D4);
                color: white;
                font-size: 14px;
                font
                font-weight: 600;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: 0.3s;
            }}
            .stButton>button:hover {{
                background: linear-gradient(to right, #2563EB, #0EA5E9);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    def render_header(self):
        st.markdown('<div class="header">Energy Consumption Analysis</div>', unsafe_allow_html=True)

    def render_sidebar(self):
        with st.sidebar:
            st.markdown("## Settings")
            st.checkbox("Enable Notifications")
            st.checkbox("Show Advanced Options")
    def load_resources(self):
        # Load models and features
        try:
            self.linear_model = joblib.load("linear_model.pkl")
            self.ridge_model = joblib.load("ridge_model.pkl")
            self.feature_names = joblib.load("feature_names.pkl")
        except Exception as e:
            st.sidebar.error(f"⚠️ Error loading resources: {e}")

    def run(self):
        voltage = st.sidebar.slider("Voltage (V)", 220.0, 255.0, 240.0)
        global_intensity = st.sidebar.slider("Global Intensity (A)", 0.0, 20.0, 4.63)
        sub_metering_1 = st.sidebar.slider("Sub Metering 1 (Wh)", 0.0, 50.0, 1.12)
        sub_metering_2 = st.sidebar.slider("Sub Metering 2 (Wh)", 0.0, 50.0, 1.30)
        sub_metering_3 = st.sidebar.slider("Sub Metering 3 (Wh)", 0.0, 50.0, 6.46)
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Select Date")
        with col2:
            time=st.time_input("Select Time")
        st.markdown(
                """
                <style>
                div[data-testid="stDateInput"]{
                    padding: 5px;
                    margin-top: 20px;
                    border-radius: 12px;
                    background-color: #E3F2FD;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                }

                div[data-testid="stTimeInput"]{
                    padding: 5px;
                    margin-top: 20px;
                    border-radius: 12px;
                    background-color: #E8F5E9;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                }
                </style>
                """,
                unsafe_allow_html=True
            )

        # Features and predictions
        date_time = pd.Timestamp.combine(date, time)
        year, month, day, hour, minute = date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute
        weekday = date_time.weekday()
        is_holiday, light = 0, 1

        input_data = pd.DataFrame({
            "Global_reactive_power": [0.0],
            "Voltage": [voltage],
            "Global_intensity": [global_intensity],
            "Sub_metering_1": [sub_metering_1],
            "Sub_metering_2": [sub_metering_2],
            "Sub_metering_3": [sub_metering_3],
            "Year": [year],
            "Month": [month],
            "Day": [day],
            "Hour": [hour],
            "Minute": [minute],
            "Is_holiday": [is_holiday],
            "Light": [light],
            "Weekday": [weekday]
        })[self.feature_names]

        try:
            linear_pred = self.linear_model.predict(input_data)[0]
            ridge_pred = self.ridge_model.predict(input_data)[0]
            st.markdown('<div class="card">Your prediction results will appear here.</div>', unsafe_allow_html=True)
            if st.button("Run Prediction"):
                st.markdown(f"<div class='stApp'><h3>Prediction Executed Successfully</h3></div>",unsafe_allow_html=True)
                st.markdown(
                    f"<div class='stApp'><h3>Linear Regression</h3><p>{linear_pred:.2f} kW</p></div>"
                    f"<div class='stApp'><h3>Ridge Regression</h3><p>{ridge_pred:.2f} kW</p></div>",
                    unsafe_allow_html=True
                )
        except ValueError as e:
            st.error(f"⚠️ Prediction Error: {e}")
        st.markdown(
            "<div class='stApp'>"
            "<strong>Note:</strong>Results are based on predictive models. For accuracy, seek expert consultation."
            "</div>",
            unsafe_allow_html=True
        )
# Run app
def main():
    app = EnergyConsumptionApp()
    app.run()

if __name__ == "__main__":
    main()

