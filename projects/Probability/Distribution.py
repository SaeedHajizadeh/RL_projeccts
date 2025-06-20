# Here we are going to practice abstract base classes in a tutorial
# ABC is the base class for abstract classes
# abstractmethod is a decorator for creating abstract methods
# abc is Abstract Base Class module
from abc import ABC, abstractmethod

# below creates an "abstract" class that inherits from ABC
class Distribution(ABC):

    # line below makes the method following it an abstract method
    # Any subclass of Distribution MUST implement this method
    @abstractmethod
    def sample(self):
        pass


# Abstract classes are a "template"
# One cannot create an instant of this class
# Now let us define a class for a "concrete" class that implements an interface
# in another file Die.py