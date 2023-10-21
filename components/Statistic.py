from . import component

import streamlit as st
import pandas as pd
import numpy as np

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
        if "delete" not in tmp:
            self.delete = None

    def display(self):
        print("Statistic display")
        st.write("### Statistic")
        #selct statistic

        if self.stat_type != None:
            print("here" + self.stat_type)

        with st.form(key="form_"+self.uuid, clear_on_submit=False):
            st.selectbox(
                    "Select a statistic", ["Mean", "Median", "Percentile", "Proportion", "Quartiles 1 and 3", "Standard Deviation"],
                    key="type_"+self.uuid,
                )
        
        # select column
            st.selectbox("Select a column", self.df.columns, key="col1_"+self.uuid)
        
            self.run = st.form_submit_button("Run")
            self.delete = st.form_submit_button("Delete")

            if self.run:
                self.run_stat()

            if self.delete:
                st.form_submit_button(label="Delete", key="delete_"+self.uuid)

        if self.output:
            self.output.display()

        if self.delete:
            self.output = None

        st.write("---")

    def run_stat(self):
        print(self.stat_type)
        self.output = StatisticOutput(self.df, st.session_state["type_"+self.uuid], st.session_state["col1_"+self.uuid])

class StatisticOutput(component.component):
    def __init__(self, df, type, col):
        super().__init__(df)
        self.stat_type = type
        self.col = col

    def display(self):
        st.write("### Statistic Output")

        if self.stat_type == "Mean":
            df2 = self.df[self.col].mean()
            st.write(f"Mean: {df2}")
        
        elif self.stat_type == "Median":
            df2 = self.df[self.col].median()
            st.write(f"Median: {df2}")
        
        elif self.stat_type == "Quartiles 1 and 3":
            Q3 = np.quantile(self.df[self.col], 0.75)
            Q1 = np.quantile(self.df[self.col], 0.25)
            st.write(f"Q1: {Q1}")
            st.write(f"Q3: {Q3}")
        
        elif self.stat_type == "Standard Deviation":
            df2 = self.df[self.col].std()
            st.write(f"Standard Deviation: {df2}")