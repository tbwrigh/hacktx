from component import component

import streamlit as st

class Model(component):
    def __init__(self, df):
        super().__init__(df)
    
    def display(self):
        st.write("### Model")
        # st.write("#### Select a column to plot")
        # # select column
        # col = st.selectbox("Select a column", self.df.columns)
        
        st.write("---")
        