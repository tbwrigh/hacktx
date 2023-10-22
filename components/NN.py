from . import component

import streamlit as st

from sklearn.model_selection import train_test_split

import tensorflow as tf

class NN(component.component):
    def __init__(self, df):
        super().__init__(df)
        self.layers = []

        self.output = None

        if "delete" not in self.layers:
            self.delete = None
    
    def display(self):
        if self.delete:
            return

        col1_container, col2_container = st.columns(2)
        
        col1_container.write("### Neural Network")
        # st.write("#### SelNo resultsect a column to plot")
        # # select column
        # col = st.selectbox("Select a column", self.df.columns)
        
        # num layers input

        col2_container.button("Delete", key="del_button_"+self.uuid, on_click=self._delete)

        st.number_input("Number of layers", key="num_layers_"+self.uuid, min_value=2, max_value=10, step=1)

        if st.session_state["num_layers_"+self.uuid] != len(self.layers):
            self.layers = []
            for n in range(st.session_state["num_layers_"+self.uuid]):
                self.layers.append(Layer(self.df))
        
        for layer in self.layers:
            layer.display()


        with st.form(key="form_"+self.uuid, clear_on_submit=False):

            # define inputs 
            st.multiselect("Select inputs", self.df.columns, key="inputs_"+self.uuid)

            # define output
            st.selectbox("Select output", self.df.columns, key="output_"+self.uuid)

            # test train split
            st.number_input("Test size", key="test_size_"+self.uuid, min_value=0.05, max_value=0.5, step=0.05)

            # num epochs
            st.number_input("Number of epochs", key="num_epochs_"+self.uuid, min_value=1, max_value=250, step=1)

            # categorical, regression
            st.selectbox("Select a model type", ["Categorical", "Regression"], key="model_output_type_"+self.uuid)

            self.run = st.form_submit_button("Run", on_click=self.run_NN)

        if self.output:
            self.output.display()

        st.write("---")

    def run_NN(self):

        layers = []
        for layer_i in range(len(self.layers)):
            if layer_i == 0:
                layers.append(self.layers[layer_i].getLayer(input_shape=(len(st.session_state["inputs_"+self.uuid]),)))
            else:
                layers.append(self.layers[layer_i].getLayer())
                        
        self.output = NNModel(self.df, layers, st.session_state["inputs_"+self.uuid], st.session_state["output_"+self.uuid], st.session_state["test_size_"+self.uuid], st.session_state["num_epochs_"+self.uuid], st.session_state["model_output_type_"+self.uuid])

    def _delete(self):
        self.delete = True

class Layer(component.component):
    def __init__(self, df):
        super().__init__(df)
    
    def display(self):
        st.selectbox(
                    "Select a type", ["Dense", "Dropout"],
                    key="layer_type_"+self.uuid,
                )

        if st.session_state["layer_type_"+self.uuid] == "Dense":
            st.number_input("Number of neurons", key="neurons_"+self.uuid, min_value=1, step=1)
            st.selectbox(
                "Select an activation function", ["None", "ReLU", "Sigmoid", "Softmax"],
                key="activation_"+self.uuid,
            )
        elif st.session_state["layer_type_"+self.uuid] == "Dropout":
            st.number_input("Dropout rate", key="dropout_"+self.uuid, min_value=0.0, max_value=1.0, step=0.1)
        else:
            st.write("Error: Invalid layer type")

    def getLayer(self, input_shape=None):
        if st.session_state["layer_type_"+self.uuid] == "Dense":
            if st.session_state["activation_"+self.uuid] == "None":
                if input_shape:
                    return tf.keras.layers.Dense(st.session_state["neurons_"+self.uuid], input_shape=input_shape, name="dense_"+self.uuid)
                return tf.keras.layers.Dense(st.session_state["neurons_"+self.uuid], name="dense_"+self.uuid)
            if input_shape:
                return tf.keras.layers.Dense(st.session_state["neurons_"+self.uuid], activation=st.session_state["activation_"+self.uuid].lower(), input_shape=input_shape, name="dense_"+self.uuid)
            return tf.keras.layers.Dense(st.session_state["neurons_"+self.uuid], activation=st.session_state["activation_"+self.uuid].lower(), name="dense_"+self.uuid)
        elif st.session_state["layer_type_"+self.uuid] == "Dropout":
            return tf.keras.layers.Dropout(st.session_state["dropout_"+self.uuid], name="dropout_"+self.uuid)
        else:
            st.write("Error: Invalid layer type")


class NNModel(component.component):
    def __init__(self, df, layers, inputs, output, test_size, num_epochs, type_out):    
        super().__init__(df)
        self.df = df
        self.layers = layers
        self.inputs = inputs
        self.output = output
        self.test_size = test_size
        self.num_epochs = num_epochs
        self.type_out = type_out
        self.results = None
        self.model = None
        self.model_name = None

    def display(self):
        st.write("### Neural Network Output")

        # split data
        X = self.df[self.inputs]
        y = self.df[self.output]


        if self.type_out == "Categorical":
            y = tf.keras.utils.to_categorical(y)

            total_categories = len(y[0])

            if not self.layers[-1].name.startswith("output_layer"):
                self.layers.append(tf.keras.layers.Dense(total_categories, activation="softmax", name="output_layer_categories_"+self.uuid))
        elif self.type_out == "Regression":
            if not self.layers[-1].name.startswith("output_layer"):
                self.layers.append(tf.keras.layers.Dense(1, name="output_layer_regression_"+self.uuid))

        # determine if model is sequential and already has correct layers
        if not (self.model and self.model.layers == self.layers):
            self.model = tf.keras.Sequential(self.layers)

            # select loss based on type_out
            if self.type_out == "Categorical":
                self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            elif self.type_out == "Regression":
                self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])


            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size)

            # train model
            self.model.fit(X_train, y_train, epochs=self.num_epochs)

            self.results = self.model.evaluate(X_test, y_test)
        
            name = st.session_state["selected_file"] + "_" + "_".join(self.inputs)+"_"+self.output+"_"+str(self.test_size)+"_"+str(self.num_epochs)+".h5"
            self.model.save("models/"+name)

            self.model_name = name

        # evaluate model
        if self.type_out == "Categorical" and self.results:
            st.write(f"Accuracy: {self.results[1]}")
        elif self.type_out == "Regression" and self.results:
            st.write(f"MSE: {self.results[0]}")


        if self.model_name:
            # save model
            with open("models/"+self.model_name, "rb") as f:
                bytes_data = f.read()
                st.download_button('Download Model', f, file_name=self.model_name)