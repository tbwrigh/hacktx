# import component from same dir
from . import component

import streamlit as st
import pandas as pd

class Graph(component.component):

    def __init__(self, df):
        super().__init__(df)
        print("Graph init")
        tmp = vars(self)

        print(self.uuid)

        if "run" not in tmp:
            self.run = None
        if "output" not in tmp:
            self.output = None
        if "delete" not in tmp:
            self.delete = None

    def display(self):
        if self.delete:
            return
        
        print("Graph display")
        st.write("### Graph")
        # select graph type

        st.button("Delete", key="del_button_"+self.uuid, on_click=self._delete)

        graph_type = st.selectbox(
                    "Select a graph type", ["Line", "Bar", "Scatter plot"], 
                    key="type_"+self.uuid, 
                )

        with st.form(key="form_"+self.uuid, clear_on_submit=False):
            if graph_type == "Line":
                st.selectbox("Select a column", st.session_state["quantitative_variables"], key="col1_"+self.uuid)
                st.selectbox("Select a second column", st.session_state["quantitative_variables"], key="col2_"+self.uuid)
            elif graph_type == "Bar":
                st.selectbox("Select a column", st.session_state["categorical_variables"], key="col1_"+self.uuid)
                st.session_state["col2_"+self.uuid] = None
            elif graph_type == "Scatter plot":
                st.selectbox("Select a column", st.session_state["quantitative_variables"], key="col1_"+self.uuid)
                st.selectbox("Select a second column", st.session_state["quantitative_variables"], key="col2_"+self.uuid)

            self.run = st.form_submit_button("Run")

            if self.run:
                self.run_graph()

        if self.output:
            self.output.display()
        
        st.write("---")
    
    def run_graph(self):
        self.output = GraphOutput(self.df, st.session_state["type_"+self.uuid], st.session_state["col1_"+self.uuid], st.session_state["col2_"+self.uuid])

    def _delete(self):
        self.delete = True

class GraphOutput(component.component):
    def __init__(self, df, type, col1, col2):
        super().__init__(df)
        self.graph_type = type
        self.col1 = col1
        self.col2 = col2

    def display(self):
        st.write("### Graph Output")

        if self.graph_type == "Line":
            self.line_graph()
        elif self.graph_type == "Bar":
            self.bar_graph()
        elif self.graph_type == "Scatter plot":
            self.scatter_graph()
    
    def line_graph(self):
        st.line_chart(data=self.df, x=self.col1, y=self.col2)

    def bar_graph(self):
        counts_df = self.df[self.col1].value_counts().reset_index()
        st.bar_chart(data=counts_df, x=self.col1, y="count")
    
    def scatter_graph(self):
        self.df[self.col1] = pd.to_numeric(self.df[self.col1], errors='coerce')
        self.df[self.col2] = pd.to_numeric(self.df[self.col2], errors='coerce')
        st.scatter_chart(data=self.df, x=self.col1, y=self.col2)