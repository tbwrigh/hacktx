from streamlit_extras.switch_page_button import switch_page
from io import BytesIO
import streamlit as st
import os

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="KeiFlow",
    page_icon="logo_icon.png",  # Replace with the path to your local icon file
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none;
    }
    [data-testid="stSidebar"] {
    display: none;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.write("# Welcome to KeiFlow")

st.write("## Upload your data")

upload = False
existing = False

uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False, type="csv")
if uploaded_file:
    upload = True

st.write("## Or Select an Existing Dataset")

# get files in datasets folder
files = os.listdir("datasets/")
files = [file for file in files if os.path.isfile(os.path.join("datasets/", file))]
files = ["None"] + files

# create drop down  
selected_file = st.selectbox("Select a dataset", files)

# on select file
if selected_file != "None":
    # read file
    existing=True

# go button
start_button = st.button("Start")

if start_button:
    if upload:
        bytes_data = uploaded_file.read()
        # write to datasets folder
        with open(os.path.join("datasets/", uploaded_file.name), "wb") as f:
            f.write(bytes_data)

        st.session_state["selected_file"] = uploaded_file.name
        
        switch_page("Builder Tool")        
        
    elif existing:                

        st.session_state["selected_file"] = selected_file

        switch_page("Builder Tool")
    else:
        st.write("## Error")
        st.write("You must select a file or upload a file")

# st.markdown("# Home Page")
#st.sidebar.markdown("# Home Page")
