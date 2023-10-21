from . import component

import streamlit as st

class Statistic(component.component):
    def __init__(self, df):
        super().__init__(df)
        self.stat_type = None
        self.run = None
        self.output = None

    def display(self):
        st.write("### Statistic")
        #selct statistic
        self.stat_type = st.selectbox("Select a statistic", ["Mean", "Median", "Standard Deviation", "IQR", "Percentile"])
        
        st.write("### Column")
        # select column
        col = st.selectbox("Select a column", self.df.columns, key=self.get_count())
        
        self.run = st.button("Run", key=self.get_count(), on_click=self.run_stat)

        if self.output:
            self.output.display()
        
        st.write("---")

    def run_stat(self):
        self.output = StatisticOutput(self.df, self.stat_type)

class StatisticOutput(component.component):
    def __init__(self, df, type):
        super().__init__(df)
        self.stat_type = type

    def display(self):
        st.write("### Statistic Output")