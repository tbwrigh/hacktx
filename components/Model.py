from . import component

import streamlit as st

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

class Model(component.component):
    def __init__(self, df):
        super().__init__(df)

        print("Model init")
        tmp = vars(self)

        print(self.uuid)

        if "run" not in tmp:
            self.run = None
        if "output" not in tmp:
            self.output = None

    
    def display(self):
        st.write("### Model")


        st.selectbox(
            "Select a model", ["Linear Regression", "Logistic Regression", "KNN", "Decision Tree", "Random Forest"], 
            key="model_type_"+self.uuid, 
        )
        
        with st.form(key="form_"+self.uuid, clear_on_submit=False):
            
            
            st.selectbox("Select Response Variable", self.df.columns, key="response_input_"+self.uuid)

            st.multiselect("Select Predictor Variables", self.df.columns, key="predictor_input_"+self.uuid)

            self.run = st.form_submit_button("Run")

            if self.run:
                self.run_model()
        
        if self.output:
            self.output.display()
        
        st.write("---")

    def run_model(self):
        self.output = ModelOutput(self.df, st.session_state["model_type_"+self.uuid], st.session_state["response_input_"+self.uuid], st.session_state["predictor_input_"+self.uuid])

class ModelOutput(component.component):
    def __init__(self, df, model_type, resp, preds):
        super().__init__(df)
        self.model_type = model_type
        self.resp = resp
        self.preds = preds

    def display(self):
        st.write("### Model Output")

        if self.model_type == "Linear Regression":
            self.linear_regression()
        elif self.model_type == "Logistic Regression":
            self.logistic_regression()
        elif self.model_type == "KNN":
            self.knn()
        elif self.model_type == "Decision Tree":
            self.decision_tree()
        elif self.model_type == "Random Forest":
            self.random_forest()
    
    def linear_regression(self):
        st.write("Linear Regression")
    
    def logistic_regression(self):
        st.write("Logistic Regression")
    
    def knn(self):
        st.write("KNN")
    
    def decision_tree(self):
        st.write("Decision Tree")
    
    def random_forest(self):
        st.write("Random Forest")
    
