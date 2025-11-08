import json
import subprocess
import pandas as pd
import streamlit as st
import io

st.set_page_config(
    page_title="E-commerce Price Tracker",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Add a background color */
    body {
        background-color: #f0f2f6;
    }

    /* Custom font for headers */
    h1, h2 {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #333;
    }

    /* Center the input box */
    .stTextInput {
        text-align: center;
        padding: 10px;
    }

    /* Style the button */
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        padding: 10px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        cursor: pointer;
        width: 200px;
        margin-top: 10px;
    }

    .stButton button:hover {
        background-color: #ff3333;
    }

    /* Center content */
    .block-container {
        max-width: 600px;
        padding-top: 50px;
    }

    /* Add footer */
    footer {
        font-size: 12px;
        text-align: center;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

def run_uipath_automation(product_name):
    input_data = json.dumps({"product_name": product_name})

    package_path = r"C:\Users\HP\pricetracker-rpa-ecommerce\BlankProcess.1.0.7.nupkg"
    result = subprocess.run(
        [r"C:\Users\HP\AppData\Local\Programs\UiPath\Studio\UiRobot.exe", "execute", "-f", package_path, f"--input={input_data}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if result.returncode == 0:
        return True  
    else:
        return False, result.stderr.decode()

st.title("🛒 E-commerce Price Tracker")
st.subheader("Easily track product prices from various online stores")

st.markdown("""
    <div style="background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    """, unsafe_allow_html=True)

product_name = st.text_input("Enter the Product Name", "")

if st.button("Track Prices"):
    if product_name:
        st.info("Tracking prices, please wait...")
        success = run_uipath_automation(product_name) 
        if success:
            st.success(f"Tracking initiated for {product_name}")
            excel_file_path = r"C:\Users\HP\OneDrive\Pictures\Documents\priceMonitor.xlsx"
            try:
                df = pd.read_excel(excel_file_path)
                st.table(df)  
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                excel_buffer.seek(0) 

                st.download_button(
                    label="Download Excel File",
                    data=excel_buffer.getvalue(),
                    file_name='product_prices.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            except Exception as e:
                st.error(f"Failed to load data from Excel: {str(e)}")
        else:
            st.error("Failed to initiate tracking.")
    else:
        st.error("Please enter a product name.")

st.markdown("</div>", unsafe_allow_html=True)