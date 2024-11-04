import streamlit as st
from streamlit_option_menu import option_menu
from prediction_page import show_prediction_page
from explore_data_page import show_explore_data_page

selected = option_menu(
    menu_title = None,
    options=["Predict", "Explore Data"],
    icons=["currency-euro", "bar-chart-line-fill"],
    orientation = "horizontal",
)

if selected == "Predict":
    show_prediction_page()
else:
    show_explore_data_page()