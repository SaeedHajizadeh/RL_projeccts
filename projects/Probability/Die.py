from Distribution import Distribution
import random
from dataclasses import dataclass

# define an n-sided Die, for example
class Die(Distribution):
    def __init__(self , sides):
        self.sides = sides

    # the following constructor used to "represent" any instant of the class Die
    def __repr__(self):
        return f"{self.sides}"

    # is used to check if two objects of this class have the same "side" property
    def __eq__(self, other):
        if isinstance(other , Die):
            return self.sides == other.sides
        return False

    def sample(self):
        return random.randint(1 , self.sides)

fifteen_sided = Die(15)
six_sided = Die(6)


# roll a 15- and a 6- sided dice and add the results
def roll_dice():
    return fifteen_sided.sample() + six_sided.sample()

########################################################################
# # This is a tedious and mistake-prone method to deal with this issue
# # For example:  Comment this section out to see the example
# class Student:
#     def __init__(self, name, age, grade):
#         self.name = name
#         self.age = age
#         self.grade = grade
#
#     def __eq__(self, other):
#         return (self.name == other.name and
#                 self.age == other.age)
#         # MISTAKE: Forgot to include self.grade!
#
#     def __repr__(self):
#         return f"Student('{self.name}', {self.age}, '{self.grade}')"
#
#
# # Now watch the weird behavior:
# student1 = Student("Alice", 20, "A")
# student2 = Student("Alice", 20, "F")  # Same name/age, different grade
#
# print(student1 == student2)  # True - BUT THEY'RE NOT THE SAME!
# print(student1)  # Student('Alice', 20, 'A')
# print(student2)  # Student('Alice', 20, 'F')

# # Instead, use dataclasses to do the above much simpler
# # In the dataclass below, all __eq__ and __repr__ and __init__
# # are implicit and the code is equivalent to the nugget above
#
#
# # Python decorators are modifiers that can be applied to class, function and method definitions. A decorator
# # is written above the definition that it applies to, starting with a @ symbol.
#
# @dataclass
# class Die(Distribution):
#     sides: int
#
#     def sample(self):
#         return random.randint(1 , self.sides)

#########################################################################


# If we create a Die object with, say, n sides, then if, by any chance, we need
# to change its number of sides, it is strongly recommend to simply create a new
# object with a different size in lieu of changing the sides of the previously
# defined object. To ensure integrity in coding, dataclasses provides a framework
# to ask Python to prevent us from rewriting the sides of an already defined object
# or in general, changing the characteristics of any already defined object


# @dataclass(frozen=True)
# class Die(Distribution):
#     ...

# # with frozen = True, the following raises an error
# d = Die(6)
# d.sides = 10

# # Suppose now we want to change the value of this "immutable" object:
# import dataclasses
# d6 = Die(6)
# d20 = dataclasses.replace(d6 , sides = 20)

# # Aside from helping us prevent bugs and errors, frozen = True, which makes the object immutable
# # as stated, has another benefit. Only immutable objects can be used as "keys" in dictionaries
# # Hence, an object sides_nf from a non-frozen dataclass, cannot bet set as a key in a dictionary:
# sides_nf = Die(6)
# {sides_nf : "6"}   # raises an error if Die is nonfrozen
# # whereas an object sides_f from a frozen dataclass could
# sides_f = Die(6)
# {sides_f: "6"}     # runs well if Die is frozen


# # Sometimes we need to add annotations to, not only variables, as required by @dataclasses, but also
# # to the output of a function
# @dataclass(frozen=True)
# class Die(Distribution):
#     sides: int                # variable annotation
#
#     def sample(self) -> int:  # function annotation
#         return random.randint(1 , self.sides)



# Type Variables
# The distribution class, which was an abstract interface, defines the same sample method. This method
# however is general and does not return a "particular" type. For instance, if the class that implements
# the abstract Distribution interface, like Die, produces an integer, then the output of the sample in the
# interface class would be int. If the concrete class is a Normal distribution, that sample would produce a
# float. So we could either leave the annotation out for the abstract method defined on the sample method in
# the interface class but it will be confusing. For this purpose, we are going to need Type Variables
# In other words, we need to tell Python that the output of the Distribution, which is an abstract class, is
# "generic"

from typing import Generic, TypeVar, Sequence
from abc import ABC, abstractmethod
# Define a type variable A
A = TypeVar("A")

# Distribution is "generic in A"
class Distribution(ABC , Generic[A]):
    # sampling must now produce an output of type A

    @abstractmethod
    def sample(self) -> A:
        pass

# so far we have said that Distribution uses type A
class Die(Distribution[int]):
    ...
# This says that Die is an instance of Distribution[int]

# To see how to use this in another example, let's say we want to write a function that
# samples a given  number of times from a distribution, with int or float output, and
# computes the sample mean to approximate the mean, say. We can annotate this concrete
# class using Distribution[float]

# import statistics
#
# def expected_value(d: Distribution[float] , n: int = 100) -> float:
#     return statistics.mean(d.sample() for _ in range(n))
#
# print(expected_value(Die(6)))
# print(expected_value(RandomName())) # RandomName() is of type Distribution[str] --> raises a type Error

# # Why this much abstraction?;
# # How does the abstraction help us understand the code?
# # What kind of mistakes does it prevent—and what kind of mistakes does it encourage?
# # What kind of added functionality does it give us?
#
# # One such application of this level of abstraction is to avoid coding up "frequently used"
# # functionalities from scratch every single time. Example: sampling from a distribution n times
# # and putting them in a list
# import random
# from abc import ABC, abstractmethod
# from typing import TypeVar, Generic, Sequence
# T = TypeVar("T")
#
# class Distribution(ABC , Generic[T]):
#     @abstractmethod
#     def sample(self) -> T:
#         pass
#
#     def sample_n(self, n: int) -> Sequence[T]:
#         return [self.sample() for _ in range(n)]
#
# class Die(Distribution[int]):  # T = int for dice
#     def sample(self) -> int:
#         return random.randint(1, 6)
#
# die = Die()
# rolls = die.sample_n(10)  # Returns Sequence[int]
#
# # Notice that T could be more generic. It could also be float, str, or another, say, object
# # which could, for instance, be actions taken in a reinforcement learning algorithm

if __name__ == "__main__":
    print(f'Rolling a {six_sided.__repr__()}-sided and a '
          f'{fifteen_sided.__repr__()}-side die and adding them: {roll_dice()}')

    print(f"{six_sided.__eq__(Die(6))}")
    print(f"{six_sided == Die(6)}")
    print(f"{six_sided == None}")



