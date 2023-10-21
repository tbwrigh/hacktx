# import component from same dir
from . import component

import streamlit as st

class Graph(component.component):
    def __init__(self, df):
        super().__init__(df)
        self.graph_type = None
        self.run = None

    def display(self):
        st.write("### Graph")
        # select graph type
        self.graph_type = st.selectbox("Select a graph type", ["Line", "Bar", "Pie"], key=self.get_count())

        self.run = st.button("Run", key=self.get_count())


        # st.write("#### Select a column to plot")
        # # select column
        # col = st.selectbox("Select a column", self.df.columns)
        
        st.write("---")