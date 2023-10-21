from abc import ABC, abstractmethod

import uuid

class component(ABC):
    @abstractmethod
    def __init__(self, df):
        self.df = df
        self.count = str(uuid.uuid4())
    @abstractmethod
    def display(self):
        pass

