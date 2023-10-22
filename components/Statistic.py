from . import component

import streamlit as st
import pandas as pd
import numpy as np

class Statistic(component.component):
    def __init__(self, df):
        super().__init__(df)
        print("Statistic init")
        tmp = vars(self)
        
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
        if self.delete:
            return

        print("Statistic display")
        st.write("### Statistic")
        #selct statistic

        st.button("Delete", key="del_button_"+self.uuid, on_click=self._delete)

        stat_type = st.selectbox(
                "Select a statistic", ["Mean", "Median", "Proportion", "Quartiles 1 and 3", "Standard Deviation"],
                key="type_"+self.uuid,
                )

        if self.stat_type != None:
            print("here" + self.stat_type)

        with st.form(key="form_"+self.uuid, clear_on_submit=False):
            
            # select column
            if stat_type == "Mean" or stat_type == "Median" or stat_type == "Quartiles 1 and 3" or stat_type == "Standard Deviation":
                st.selectbox("Select a column", st.session_state["quantitative_variables"], key="col1_"+self.uuid)
            elif stat_type == "Proportion":
                st.selectbox("Select a column", st.session_state["categorical_variables"], key="col1_"+self.uuid)
        
            self.run = st.form_submit_button("Run")

            if self.run:
                self.run_stat()

        if self.output:
            self.output.display()

        st.write("---")

    def run_stat(self):
        print(self.stat_type)
        self.output = StatisticOutput(self.df, st.session_state["type_"+self.uuid], st.session_state["col1_"+self.uuid])
    
    def _delete(self):
        self.delete = True

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
        
        elif self.stat_type == "Proportion":
            value_counts = self.df[self.col].value_counts()

            frequency = value_counts.to_dict()

            num_rows = len(self.df)

            for key, value in frequency.items():
                proportion = value/num_rows
                st.write(f"Proportion of {key} = {proportion}")