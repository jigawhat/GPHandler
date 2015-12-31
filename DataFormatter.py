from abc import ABCMeta, abstractmethod

class DataFormatter:

    __metaclass__ = ABCMeta

    @abstractmethod
    def format_X_y(self):
        raise NotImplementedError("Implementation of format_X_y required here")

    # Format input X dataframe
    @abstractmethod
    def format_X(self):
        raise NotImplementedError("Implementation of format_X required here")

    # Correct and format output prices
    @abstractmethod
    def format_y_sigma(self):
        raise NotImplementedError("Implementation of format_y_sigma required here")


