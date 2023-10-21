import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os

import pandas as pd

from components import Graph, Statistic, Model, NN

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

section_add_select = st.selectbox("Select a section type", ["Graph", "Statistic", "Model", "Neural Network"])

add_button = st.button("Add Section")

st.write("---")

if "components" not in st.session_state:
    st.session_state["components"] = []

if add_button:
    if section_add_select == "Graph":
        st.session_state["components"].append(Graph.Graph(df))
    elif section_add_select == "Statistic":
        st.session_state["components"].append(Statistic.Statistic(df))
    elif section_add_select == "Model":
        st.session_state["components"].append(Model.Model(df))
    elif section_add_select == "Neural Network":
        st.session_state["components"].append(NN.NeuralNetwork(df))

for component in st.session_state["components"]:
    component.display()

