# import component from same dir
from . import component

import streamlit as st

class Graph(component.component):
    def __init__(self, df):
        super().__init__(df)

    def display(self):
        st.write("### Graph")
        # select graph type
        graph_type = st.selectbox("Select a graph type", ["Line", "Bar", "Pie"], key=self.count)


        # st.write("#### Select a column to plot")
        # # select column
        # col = st.selectbox("Select a column", self.df.columns)
        
        st.write("---")