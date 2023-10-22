from . import component

import streamlit as st

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import confusion_matrix

from sklearn.exceptions import ConvergenceWarning

from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

import numpy as np

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
        if "delete" not in tmp:
            self.delete = None

    
    def display(self):
        if self.delete:
            return
        
        st.write("### Model")

        st.button("Delete", key="del_button_"+self.uuid, on_click=self._delete)

        st.selectbox(
            "Select a model", ["Linear Regression", "Logistic Regression", "KNN", "Decision Tree", "Random Forest"], 
            key="model_type_"+self.uuid, 
        )

        with st.form(key="form_"+self.uuid, clear_on_submit=False):
            
            
            st.selectbox("Select Response Variable", self.df.columns, key="response_input_"+self.uuid)

            st.multiselect("Select Predictor Variables", self.df.columns, key="predictor_input_"+self.uuid)

            st.slider("Percent Data Withheld For Testing", key="test_size_input_"+self.uuid, min_value=0.05, max_value=0.5, value=0.2, step=0.05)

            if st.session_state["model_type_"+self.uuid] == "Logistic Regression":
                st.selectbox("Select Model", ["Ridge", "Lasso"], key="penalty_input_"+self.uuid)
            elif st.session_state["model_type_"+self.uuid] == "KNN":
                st.number_input("Number of Neighbors", key="n_neighbors_input_"+self.uuid, min_value=1, max_value=100, value=5)
            elif st.session_state["model_type_"+self.uuid] == "Random Forest":
                st.number_input("Number of Trees", key="n_estimators_input_"+self.uuid, min_value=1, max_value=100, value=10)
                st.number_input("Max Depth", key="max_depth_input_"+self.uuid, min_value=1, max_value=100, value=10)

            self.run = st.form_submit_button("Run")

            if self.run:
                self.run_model()
        
        if self.output:
            self.output.display()
        
        st.write("---")

    def run_model(self):
        self.output = ModelOutput(self.df, st.session_state["model_type_"+self.uuid], st.session_state["response_input_"+self.uuid], st.session_state["predictor_input_"+self.uuid], self.uuid)

    def _delete(self):
        self.delete = True

class ModelOutput(component.component):
    def __init__(self, df, model_type, resp, preds, parent_uuid):
        super().__init__(df)
        self.model_type = model_type
        self.resp = resp
        self.preds = preds
        self.model = None
        self.prediction = None
        self.parent_uuid = parent_uuid
        self.cat_maps = {}

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

        self.predict_window()

        if self.prediction:
            st.write("Prediction: " + str(self.prediction[0]))
    
    def linear_regression(self):
        X = self.df[self.preds]
        y = self.df[self.resp]

        if "test_size_input_"+self.parent_uuid not in st.session_state:
            st.session_state["test_size_input_"+self.parent_uuid] = 0.2
        split_percent = st.session_state["test_size_input_"+self.parent_uuid]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_percent)

        self.model = LinearRegression()

        self.model.fit(X_train, y_train)

        st.write("Linear Regression")

        st.write("Fitted Model: ")

        st.latex('\hat{y} = ' + str(round(self.model.intercept_, 4)) + " + " + " + ".join([str(round(self.model.coef_[i],4)) + "x_" + str(i) for i in range(len(self.model.coef_))]))

        st.write("Mean Squared Error: " + str(np.mean((y_test - self.model.predict(X_test)) ** 2)))

        st.write("Root Mean Squared Error: " + str(np.sqrt(np.mean((y_test - self.model.predict(X_test)) ** 2))))

        st.write("R Squared: " + str(self.model.score(X_test, y_test)))

        st.write("Adjusted R Squared: " + str(1 - (1 - self.model.score(X_test, y_test)) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)))

    
    def logistic_regression(self):
        st.write("Logistic Regression")

        X = self.df[self.preds]
        y = self.df[self.resp]

        if "test_size_input_"+self.parent_uuid not in st.session_state:
            st.session_state["test_size_input_"+self.parent_uuid] = 0.2
        split_percent = st.session_state["test_size_input_"+self.parent_uuid]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_percent)

        penalty_map = {"Ridge": "l2", "Lasso": "l1"}

        try:
            self.model = LogisticRegression(penalty=penalty_map[st.session_state["penalty_input_"+self.parent_uuid]], solver="saga")
            self.model.fit(X_train, y_train)
        except ConvergenceWarning:
            st.write("Error: Coefficients did not converge")
            return

        st.write("Fitted Model: ")

        st.latex('\hat{y} = ' + str(round(self.model.intercept_[0], 4)) + " + " + " + ".join([str(round(self.model.coef_[0][i],4)) + "x_" + str(i) for i in range(len(self.model.coef_[0]))]))

        st.write("Mean Squared Error: " + str(np.mean((y_test - self.model.predict(X_test)) ** 2)))

        st.write("Root Mean Squared Error: " + str(np.sqrt(np.mean((y_test - self.model.predict(X_test)) ** 2))))

        st.write("R Squared: " + str(self.model.score(X_test, y_test)))

        st.write("Adjusted R Squared: " + str(1 - (1 - self.model.score(X_test, y_test)) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)))
    
    def knn(self):
        st.write("KNN")

        X = self.df[self.preds]

        # map predictor variables to numbers
        for pred in self.preds:
            if X[pred].dtype == "object":
                category_map = dict(enumerate(X[pred].astype("category").cat.categories))
                X[pred] = X[pred].astype("category").cat.codes
                self.cat_maps[pred] = category_map
        
        y = self.df[self.resp]

        if "test_size_input_"+self.parent_uuid not in st.session_state:
            st.session_state["test_size_input_"+self.parent_uuid] = 0.2
        split_percent = st.session_state["test_size_input_"+self.parent_uuid]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_percent)

        self.model = KNeighborsClassifier(n_neighbors=st.session_state["n_neighbors_input_"+self.parent_uuid])

        self.model.fit(X_train, y_train)

        st.write("Score: " + str(self.model.score(X_test, y_test)))

        cm = confusion_matrix(y_test, self.model.predict(X_test))
        classes = [str(i) for i in range(len(cm))]
        
        fig, ax = plt.subplots()
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)

        # Add labels to the plot
        ax.set(xticks=np.arange(cm.shape[1]),
            yticks=np.arange(cm.shape[0]),
            xticklabels=classes, yticklabels=classes,
            title='Confusion Matrix',
            ylabel='True label',
            xlabel='Predicted label')

            # Rotate the tick labels and set their alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                    rotation_mode="anchor")

        st.pyplot(fig)
    
    def decision_tree(self):
        st.write("Decision Tree")

        self.model = DecisionTreeClassifier()

        X = self.df[self.preds]

        # map predictor variables to numbers
        for pred in self.preds:
            if X[pred].dtype == "object":
                category_map = dict(enumerate(X[pred].astype("category").cat.categories))
                X[pred] = X[pred].astype("category").cat.codes
                self.cat_maps[pred] = category_map

        y = self.df[self.resp]

        if "test_size_input_"+self.parent_uuid not in st.session_state:
            st.session_state["test_size_input_"+self.parent_uuid] = 0.2
        split_percent = st.session_state["test_size_input_"+self.parent_uuid]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_percent)

        self.model.fit(X_train, y_train)

        st.write("Score: " + str(self.model.score(X_test, y_test)))

        cm = confusion_matrix(y_test, self.model.predict(X_test))
        classes = [str(i) for i in range(len(cm))]
        
        fig, ax = plt.subplots()
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)

        # Add labels to the plot
        ax.set(xticks=np.arange(cm.shape[1]),
            yticks=np.arange(cm.shape[0]),
            xticklabels=classes, yticklabels=classes,
            title='Confusion Matrix',
            ylabel='True label',
            xlabel='Predicted label')

            # Rotate the tick labels and set their alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                    rotation_mode="anchor")

        st.pyplot(fig)
    
    def random_forest(self):
        st.write("Random Forest")

        self.model = RandomForestClassifier(n_estimators=st.session_state["n_estimators_input_"+self.parent_uuid], max_depth=st.session_state["max_depth_input_"+self.parent_uuid])

        X = self.df[self.preds]

        # map predictor variables to numbers
        for pred in self.preds:
            if X[pred].dtype == "object":
                category_map = dict(enumerate(X[pred].astype("category").cat.categories))
                X[pred] = X[pred].astype("category").cat.codes
                self.cat_maps[pred] = category_map

        y = self.df[self.resp]

        if "test_size_input_"+self.parent_uuid not in st.session_state:
            st.session_state["test_size_input_"+self.parent_uuid] = 0.2
        split_percent = st.session_state["test_size_input_"+self.parent_uuid]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_percent)

        self.model.fit(X_train, y_train)

        st.write("Score: " + str(self.model.score(X_test, y_test)))

        cm = confusion_matrix(y_test, self.model.predict(X_test))
        classes = [str(i) for i in range(len(cm))]
        
        fig, ax = plt.subplots()
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)

        # Add labels to the plot
        ax.set(xticks=np.arange(cm.shape[1]),
            yticks=np.arange(cm.shape[0]),
            xticklabels=classes, yticklabels=classes,
            title='Confusion Matrix',
            ylabel='True label',
            xlabel='Predicted label')

            # Rotate the tick labels and set their alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                    rotation_mode="anchor")

        st.pyplot(fig)

    
    def predict_window(self):
        with st.form(key="predict_form_"+self.uuid, clear_on_submit=False):
            st.write("### Predict")
            for pred in self.preds:
                if pred in self.cat_maps:
                    st.selectbox("Input " + pred, self.cat_maps[pred].values(), key="predict_input_"+pred+"_"+self.uuid)
                else:
                    st.number_input("Input " + pred, key="predict_input_"+pred+"_"+self.uuid)
            
            predict_button = st.form_submit_button("Predict")

            if predict_button:
                self.predict()
    
    def predict(self):
        row = []
        for pred in self.preds:
            val = st.session_state["predict_input_"+pred+"_"+self.uuid]
            if pred in self.cat_maps:
                reversed_map = {v: k for k, v in self.cat_maps[pred].items()}
                row.append(reversed_map[val])
            else:
                row.append(val)
        self.prediction = self.model.predict([row])

    
