# import component from same dir
from . import component

import streamlit as st

class Graph(component.component):

    def __init__(self, df):
        super().__init__(df)
        print("Graph init")
        tmp = vars(self)

        print(self.uuid)

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

        with st.form(key="form_"+self.uuid, clear_on_submit=False):
            st.selectbox(
                    "Select a graph type", ["Line", "Bar"], 
                    key="type_"+self.uuid, 
                )
            
            st.selectbox("Select a column", self.df.columns, key="col1_"+self.uuid)
            st.selectbox("Select a column (Only Used for Line)", self.df.columns, key="col2_"+self.uuid)

            self.run = st.form_submit_button("Run")

            # st.write(st.session_state)

            if self.run:
                self.run_graph()

        if self.output:
            self.output.display()
        
        st.write("---")
    
    def run_graph(self):
        print(self.graph_type)
        self.output = GraphOutput(self.df, st.session_state["type_"+self.uuid], st.session_state["col1_"+self.uuid], st.session_state["col2_"+self.uuid])


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
    
    def line_graph(self):
        st.line_chart(data=self.df, x=self.col1, y=self.col2)

    def bar_graph(self):
        counts_df = self.df[self.col1].value_counts().reset_index()
        st.bar_chart(data=counts_df, x=self.col1, y="count")
