from . import component

import streamlit as st
import pandas as pd

class Statistic(component.component):
    def __init__(self, df):
        super().__init__(df)
        print("Statistic init")
        tmp = vars(self)
        # self.stat_type = None
        # self.run = None
        # self.output = None
        print(self.uuid)

        if "stat_type" not in tmp:
            self.stat_type = None
        if "run" not in tmp:
            self.run = None
        if "output" not in tmp:
            self.output = None
        if "col1" not in tmp:
            self.col1 = None

    def display(self):
        print("Statistic display")
        st.write("### Statistic")
        #selct statistic

        if self.stat_type != None:
            print("here" + self.stat_type)

        with st.form(key="form_"+self.uuid, clear_on_submit=False):
            choice = st.selectbox(
                    "Select a statistic", ["Mean", "Median", "Standard Deviation", "IQR", "Percentile"],
                    key="type_"+self.uuid,
                )
        
        #st.write("### Column")
        # select column
            column = st.selectbox("Select a column", self.df.columns, key="col1_"+self.uuid)
        
            self.run = st.form_submit_button("Run")

            if self.run:
                self.run_stat()

        if self.output:
            self.output.display()
        
        if choice == "Mean":
            df2 = self.df[column].mean()
            st.write(df2)

        st.write("---")

    def run_stat(self):
        print(self.stat_type)
        self.output = StatisticOutput(self.df, st.session_state["type_"+self.uuid], st.session_state["col1_"+self.uuid])

class StatisticOutput(component.component):
    def __init__(self, df, type):
        super().__init__(df)
        self.stat_type = type

    def display(self):
        st.write("### Statistic Output")