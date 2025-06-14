from Distribution import Distribution
import random

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

#########################################################################


if __name__ == "__main__":
    print(f'Rolling a {six_sided.__repr__()}-sided and a '
          f'{fifteen_sided.__repr__()}-side die and adding them: {roll_dice()}')

    print(f"{six_sided.__eq__(Die(6))}")
    print(f"{six_sided == Die(6)}")
    print(f"{six_sided == None}")



