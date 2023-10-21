import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.markdown("# Builder Tool")
#st.sidebar.markdown("# Builder Tool")

try :
    st.write(st.session_state["selected_file"])
except:
    switch_page("Home")

