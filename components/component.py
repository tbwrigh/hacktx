from abc import ABC, abstractmethod

class component(ABC):
    count = 0
    @abstractmethod
    def __init__(self, df):
        self.df = df
        self.count = str(self.get_count())

    @abstractmethod
    def display(self):
        pass

    def get_count(self):
        component.count += 1
        return component.count