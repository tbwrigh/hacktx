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

