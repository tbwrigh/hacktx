from . import component

import streamlit as st

class Model(component.component):
    def __init__(self, df):
        super().__init__(df)
    
    def display(self):
        st.write("### Model")
        # st.write("#### Select a column to plot")
        # # select column
        # col = st.selectbox("Select a column", self.df.columns)

        self.run = st.button("Run", key=self.get_count(), on_click=self.run_model)
        
        st.write("---")
