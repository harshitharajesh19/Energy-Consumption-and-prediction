import pandas as pd
import streamlit as st
import joblib
import plotly.graph_objects as go
import numpy as np

class EnergyConsumptionApp:
    def __init__(self):
        st.set_page_config(
            page_title="Energy Consumption Analysis",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.apply_custom_styles()
        self.load_resources()
        self.render_header()
        self.render_sidebar()

    def apply_custom_styles(self):
        with st.sidebar:
            self.theme_mode = st.radio("Select Theme", ["Light", "Dark"])
            self.font_size = st.slider("Font Size", 12, 24, 16)

        # Background color based on theme
        self.bg_color = "#FFFFFF" if self.theme_mode == "Light" else "#1E1E1E"
        self.text_color = "#000000" if self.theme_mode == "Light" else "#FFFFFF"

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {self.bg_color};
                color: {self.text_color};
                font-size: {self.font_size}px;
                font-family: 'Arial', sans-serif;
            }}
            .header {{
                text-align: center;
                background: linear-gradient(to right, #003366, #336699);
                padding: 20px;
                border-radius: 24px; /* Curved corners */
                margin: 20px 0;
                font-size: {self.font_size + 10}px;
                font-weight: bold;
                color: #FFFFFF;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }}
            .prediction {{
                text-align: center;
                padding: 10px;
                border-radius: 8px;
                font-size: {self.font_size}px;
                color: {self.text_color};
                font-weight: bold;
            }}
            .stButton>button {{
                background: linear-gradient(to right, #0059B3, #0099FF);
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 12px; /* Curved corners */
                padding: 12px 24px;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                transition: 0.3s ease-in-out;
            }}
            .stButton>button:hover {{
                background: linear-gradient(to right, #004080, #0073E6);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    def render_header(self):
        st.markdown('<div class="header">⚡ Energy Consumption Analysis ⚡</div>', unsafe_allow_html=True)

    def load_resources(self):
        try:
            self.linear_model = joblib.load("linear_model.pkl")
            self.ridge_model = joblib.load("ridge_model.pkl")
            self.feature_names = joblib.load("feature_names.pkl")
            st.sidebar.success("✅ Models loaded successfully!")
        except Exception as e:
            st.sidebar.error(f" Error loading models: {e}")

    def render_sidebar(self):
        st.sidebar.markdown("### **User Input Panel**")
        
        voltage = st.sidebar.slider("Voltage (V)", 220.0, 255.0, 240.0)
        global_intensity = st.sidebar.slider("Global Intensity (A)", 0.0, 20.0, 4.63)
        sub_metering_1 = st.sidebar.slider("Sub Metering 1 (Wh)", 0.0, 50.0, 1.12)
        sub_metering_2 = st.sidebar.slider("Sub Metering 2 (Wh)", 0.0, 50.0, 1.30)
        sub_metering_3 = st.sidebar.slider("Sub Metering 3 (Wh)", 0.0, 50.0, 6.46)
        
        date = st.sidebar.date_input("Select Date")
        time = st.sidebar.time_input("Select Time")

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
        })

        if self.feature_names is not None and len(self.feature_names) > 0:
            input_data = input_data[self.feature_names]

        if st.sidebar.button(" Run Prediction"):
            self.run_predictions(input_data, voltage, global_intensity, sub_metering_1, sub_metering_2, sub_metering_3)

    def draw_gauge(self, value, label):
        # Create the circular gauge using Plotly
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': label, 'font': {'size': 20, 'color': "white"}},
            gauge={
                'axis': {'range': [None, 10]},  # Adjust the range of the gauge as needed
                'bar': {'color': 'lightblue'},
                'bgcolor': 'white',
                'steps': [
                    {'range': [0, 3], 'color': 'red'},
                    {'range': [3, 7], 'color': 'yellow'},
                    {'range': [7, 10], 'color': 'green'}
                ],
                'borderwidth': 0,  # Removes black border
            }
        ))

        fig.update_layout(
            height=350,
            margin={'l': 20, 'r': 20, 't': 30, 'b': 20},
            paper_bgcolor=self.bg_color,
            font={'color': self.text_color},
            plot_bgcolor=self.bg_color,
            xaxis={'showgrid': False, 'zeroline': False},
            yaxis={'showgrid': False, 'zeroline': False}
        )

        return fig

    def run_predictions(self, input_data, voltage, global_intensity, sub_metering_1, sub_metering_2, sub_metering_3):
        try:
            linear_pred = self.linear_model.predict(input_data)[0]
            ridge_pred = self.ridge_model.predict(input_data)[0]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"<div class='prediction' style='color:{self.text_color}; font-size:20px;'> Linear Regression</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='prediction'>Prediction: <strong>{linear_pred:.2f} kW</strong></div>", unsafe_allow_html=True)
                # Linear Regression Circular Gauge
                fig = self.draw_gauge(linear_pred, "Linear Regression")
                st.plotly_chart(fig)

            with col2:
                st.markdown(f"<div class='prediction' style='color:{self.text_color}; font-size:20px;'> Ridge Regression</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='prediction'>Prediction: <strong>{ridge_pred:.2f} kW</strong></div>", unsafe_allow_html=True)
                # Ridge Regression Circular Gauge
                fig = self.draw_gauge(ridge_pred, "Ridge Regression")
                st.plotly_chart(fig)

        except ValueError as e:
            st.error(f" Prediction Error: {e}")

def main():
    app = EnergyConsumptionApp()

if __name__ == "__main__":
    main()
