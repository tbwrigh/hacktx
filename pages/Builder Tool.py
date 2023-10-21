import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os

import pandas as pd

st.markdown("# Builder Tool")
#st.sidebar.markdown("# Builder Tool")

try :
    st.write("## " + st.session_state["selected_file"])
except:
    switch_page("Home")

# read file
df = pd.read_csv(os.path.join("datasets/", st.session_state["selected_file"]))

st.write("### Preview of data")
st.write(df.head())

st.write("---")

# selcetor for type

st.write("### Add Section")

section_add_select = st.selectbox("Select a section type", ["Text", "Code", "Graph", "Table", "Image"])

add_button = st.button("Add Section")

if add_button:
    if section_add_select == "Text":
        #st.write("Text")
        with st.expander("Text"):
            st.write("Extra")
        st.write("---")
    elif section_add_select == "Code":
        st.write("Code")
        st.write("---")
    elif section_add_select == "Graph":
        st.write("Graph")
        st.write("---")
    elif section_add_select == "Table":
        st.write("Table")
        st.write("---")
    elif section_add_select == "Image":
        st.write("Image")        
        st.write("---")
