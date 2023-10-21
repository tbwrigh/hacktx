from abc import ABC, abstractmethod

class component(ABC):
    count = 0
    @abstractmethod
    def __init__(self, df):
        self.df = df

    @abstractmethod
    def display(self):
        pass

    def get_count(self):
        self.count += 1
        return self.count