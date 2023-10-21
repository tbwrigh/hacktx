import streamlit as st
import os

st.write("# Welcome to Auto ML")

st.write("## Upload your data")

upload = False
existing = False

uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
if uploaded_file:
    upload = True


st.write("## Or Select a dataset from the list")

# get files in datasets folder
files = os.listdir("datasets/")
files = [file for file in files if os.path.isfile(os.path.join("datasets/", file))]
files = ["None"] + files
print(files)

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
        st.write("## Upload")
        st.write("You uploaded a file")

        bytes_data = uploaded_file.read()
        # write to datasets folder
        with open(os.path.join("datasets/", uploaded_file.name), "wb") as f:
            f.write(bytes_data)
        
        
    elif existing:
        st.write("## Existing")
        st.write("You selected a file")
    else:
        st.write("## Error")
        st.write("You must select a file or upload a file")

st.markdown("# Home Page")
#st.sidebar.markdown("# Home Page")