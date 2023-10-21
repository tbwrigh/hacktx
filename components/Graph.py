# import component from same dir
from . import component

import streamlit as st

class Graph(component.component):
    def __init__(self, df):
        super().__init__(df)
        print("Graph init")
        tmp = vars(self)

        if "graph_type" not in tmp:
            self.graph_type = None
        if "run" not in tmp:
            self.run = None
        if "output" not in tmp:
            self.output = None
        if "col1" not in tmp:
            self.col1 = None
        if "col2" not in tmp:
            self.col2 = None


    def display(self):
        print("Graph display")
        st.write("### Graph")
        # select graph type

        if self.graph_type != None:
            print("here" + self.graph_type)

        with st.form(key="form_"+self.count, clear_on_submit=False):
            st.selectbox(
                    "Select a graph type", ["Line", "Bar", "Pie"], 
                    key="type_"+self.count, 
                )
            
            st.selectbox("Select a column", self.df.columns, key="col1_"+self.count)
            st.selectbox("Select a column (Only Used for Line)", self.df.columns, key="col2_"+self.count)

            self.run = st.form_submit_button("Run")

            st.write(st.session_state)

            if self.run:
                self.run_graph()

        if self.output:
            self.output.display()
        
        st.write("---")
    
    def run_graph(self):
        print(self.graph_type)
        self.output = GraphOutput(self.df, st.session_state["type_"+self.count], st.session_state["col1_"+self.count], st.session_state["col2_"+self.count])


class GraphOutput(component.component):
    def __init__(self, df, type):
        super().__init__(df)
        self.graph_type = type

    def display(self):
        st.write("### Graph Output")