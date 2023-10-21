from abc import ABC, abstractmethod

class component(ABC):
    @abstractmethod
    def __init__(self, df):
        self.df = df

    @abstractmethod
    def display(self):
        pass