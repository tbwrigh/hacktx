from abc import ABC, abstractmethod

class component(ABC):
    count = 0
    @abstractmethod
    def __init__(self, df):
        self.df = df
        self.count = component.count
        component.count += 1


    @abstractmethod
    def display(self):
        pass