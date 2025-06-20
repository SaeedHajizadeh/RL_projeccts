from typing import Optional, Mapping

from numpy.random import binomial

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



# # Type Variables
# # The distribution class, which was an abstract interface, defines the same sample method. This method
# # however is general and does not return a "particular" type. For instance, if the class that implements
# # the abstract Distribution interface, like Die, produces an integer, then the output of the sample in the
# # interface class would be int. If the concrete class is a Normal distribution, that sample would produce a
# # float. So we could either leave the annotation out for the abstract method defined on the sample method in
# # the interface class but it will be confusing. For this purpose, we are going to need Type Variables
# # In other words, we need to tell Python that the output of the Distribution, which is an abstract class, is
# # "generic"
#
# from typing import Generic, TypeVar, Sequence
# from abc import ABC, abstractmethod
# # Define a type variable A
# A = TypeVar("A")
#
# # Distribution is "generic in A"
# class Distribution(ABC , Generic[A]):
#     # sampling must now produce an output of type A
#
#     @abstractmethod
#     def sample(self) -> A:
#         pass
#
# # so far we have said that Distribution uses type A
# class Die(Distribution[int]):
#     ...
# # This says that Die is an instance of Distribution[int]
#
# # To see how to use this in another example, let's say we want to write a function that
# # samples a given  number of times from a distribution, with int or float output, and
# # computes the sample mean to approximate the mean, say. We can annotate this concrete
# # class using Distribution[float]

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



# # This pattern of implementing general-purpose functions on our abstractions becomes a lot more
# # useful as the functions themselves become more complicated.
#
# # Suppose now we want to be able to call a (first-class) function f() n times, one way is
# for _ in range(n):
#     f()
#
# # Instead, we can write another function that takes the function f and an integer n as arguments and repeats f() n times
# def repeat(action: Callable , n: int):
#     for _ in range(n):
#         action()
#
# repeat(f , 10)
#
# # action has the type Callable which, in Python, covers everything (like a function) that can be called with a f() syntax
# # we can also specify the arguments and return type of the Callable, e.g. Callable[[int , str] , bool]


# # Lambdas: consider the following simple function (here Coin is a class pre-defined to model a Bernouli distribution)
# def payoff(coin: Coin) -> float:
#     return 1.0 if coin == "heads" else 0.0
# # and then used as
# expected_value(coin_flip , payoff)
#
# # Sometimes defining a name for such a simple function could be distracting so instead we can use Lambdas
# # Lambdas are function literals
# expected_value(coin_flip , lambda coin: 1.0 if coin == "heads" else 0.0)


# # How to define your custom iterator object in Python? Use a generator object
# # Iterator: any method that implements the __next__() method --> a bit awkward
# # Solution: create an iterator by creating a generator using the yield keyword
# # yield acts as a return in a function except whenever a yield is "called"
# # the difference, however, is that instead of stopping the function altogether
# # when it outputs a value, it "yields" the value to the caller and pauses the function
# # until the yielded element is consumed by the caller
# # As an example, not that the solution to y = sqrt(z) is the solution to the iteration
# # x_{n + 1} = (x_n + z/x_n) / 2 . One way to implement this is
# def sqrt(x: float, epsilon: float) -> float:
#     x1, x2 = x, x / 2
#     while abs(x2 - x1) > epsilon:
#         x1, x2 = x2, (x1 + x/x1) / 2
#     return x2
#
#
# # Using Iterator
# from collections.abc import Iterator
# import itertools
# def sqrt(x: float) -> Iterator[float]:
#     x1 = x / 2
#     while True:
#         x1 = (x1 + x/x1) / 2
#         yield x1
# list(itertools.islice(sqrt(139), 10))
# # Every time this function is called, its input gets one step closer to its square root
# # In other words, this function's output is an iterator that contains infinitely many iterations
#
# # The above function is a first-class function. What we now need to write the sqrt function is a
# # converge function that takes an iterator and returns the same version of that iterator and stops
# # when a condition is met. We are going to use itertools.pairwise
#
# def converge(values: Iterator[float], threshold: float) -> Iterator[float]:
#     for a, b in itertools.pairwise(values):
#         yield a
#         if abs(a - b) < threshold:
#             break
#
# # It is now easy to use this function
#
# results = converge(sqrt(139) , 0.0001)
# list(results)[-1]
#
# # Suppose now that we want to call this function to stop if a certain precision threshold is met, but we
# # also want to cap the iterations at 10000 in case something goes wrong.
# results = converge(sqrt(139) , 0.0001)
# capped_results = itertools.islice(results , 10000)
#
# # This way we can write, test, and debugg each of "converge", "sqrt", and "islice" separately
# # For instance, we have a bunch of algorithms and want to cap all of their iteration limits to
# # 1000 instead of 10000. We only need to modify the islice process




if __name__ == "__main__":
    print(f'Rolling a {six_sided.__repr__()}-sided and a '
          f'{fifteen_sided.__repr__()}-side die and adding them: {roll_dice()}')

    print(f"{six_sided.__eq__(Die(6))}")
    print(f"{six_sided == Die(6)}")
    print(f"{six_sided == None}")



import numpy as np
from dataclasses import dataclass
import itertools
from numpy.random import binomial

@dataclass
class Process1:

    @dataclass
    class State:
        price: int

    level_param: int
    alpha1: float = 0.25

    def up_prob(self , state: State):
        return 1 / (1 + np.exp(-self.alpha1 * (self.level_param - state.price)))

    def next_state(self , state: State) -> State:
        up_move: int = binomial(1 , self.up_prob(state) , 1)[0]
        return Process1.State(price = state.price + up_move * 2 - 1)

def simulation(process , start_state):
    state = start_state
    while True:
        yield state
        state = process.next_state(state)

def process1_price_traces(
        start_price: int,
        level_param: int,
        alpha1: float,
        time_steps: int,
        num_traces: int
) -> np.ndarray:
    process = Process1(level_param = level_param , alpha1 = alpha1)
    start_state = process.State(price = start_price)
    return np.vstack([np.fromiter((s.price for s in itertools.islice(simulation(process , start_state) , time_steps + 1)) , float) for _ in range(num_traces)])


# Plotting these
import matplotlib.pyplot as plt
import numpy as np

# Fix for non-interactive environments
plt.ioff()  # Turn off interactive mode

# Generate your price traces (using your existing function)
price_traces = process1_price_traces(
    start_price=100,
    level_param=100,
    alpha1=0.25,
    time_steps=50,
    num_traces=10
)

# Create time axis
time_steps = price_traces.shape[1] - 1  # -1 because we include t=0
time_axis = np.arange(time_steps + 1)

# Basic plot - all traces
plt.figure(figsize=(12, 8))
for i in range(price_traces.shape[0]):
    plt.plot(time_axis, price_traces[i, :], alpha=0.7, linewidth=1)

plt.title('Stock Price Simulation - Multiple Paths')
plt.xlabel('Time Steps')
plt.ylabel('Price')
plt.grid(True, alpha=0.3)
plt.savefig('price_traces_basic.png', dpi=150, bbox_inches='tight')
plt.close()  # Close to free memory

# Alternative: Plot with different styling
plt.figure(figsize=(12, 8))

# Plot all traces in light gray
for i in range(price_traces.shape[0]):
    plt.plot(time_axis, price_traces[i, :], color='lightgray', alpha=0.6, linewidth=0.8)

# Highlight the mean path
mean_path = np.mean(price_traces, axis=0)
plt.plot(time_axis, mean_path, color='red', linewidth=2, label='Average Path')

# Add level parameter line (mean-reversion level)
plt.axhline(y=100, color='blue', linestyle='--', linewidth=1, label='Mean-Reversion Level')

plt.title('Stock Price Simulation with Mean Path')
plt.xlabel('Time Steps')
plt.ylabel('Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('price_traces_mean.png', dpi=150, bbox_inches='tight')
plt.close()

# Even fancier: Plot with confidence bands
plt.figure(figsize=(12, 8))

# Calculate percentiles for confidence bands
p5 = np.percentile(price_traces, 5, axis=0)
p25 = np.percentile(price_traces, 25, axis=0)
p75 = np.percentile(price_traces, 75, axis=0)
p95 = np.percentile(price_traces, 95, axis=0)

# Fill between percentiles
plt.fill_between(time_axis, p5, p95, alpha=0.2, color='blue', label='90% Range')
plt.fill_between(time_axis, p25, p75, alpha=0.3, color='blue', label='50% Range')

# Plot mean
plt.plot(time_axis, mean_path, color='red', linewidth=2, label='Mean Path')

# Plot a few individual traces
for i in range(min(5, price_traces.shape[0])):
    plt.plot(time_axis, price_traces[i, :], alpha=0.4, linewidth=1)

plt.axhline(y=100, color='green', linestyle='--', linewidth=1, label='Mean-Reversion Level')

plt.title('Stock Price Simulation with Confidence Bands')
plt.xlabel('Time Steps')
plt.ylabel('Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('price_traces_confidence.png', dpi=150, bbox_inches='tight')
plt.close()



handy_map: Mapping[Optional[bool], int] = {True: 1, False: -1, None: 0}

# Process 2
@dataclass
class Process2:

    @dataclass
    class State:
        price: int
        is_prev_move_up: Optional[bool]

    alpha2: float = 0.75

    # We need up_move and next_state
    def up_move(self , state: State) -> int:
        is_prev_move_up: int = handy_map[state.is_prev_move_up]
        up_prob: float = 0.5 * (1 - self.alpha2 * is_prev_move_up)
        return binomial(1 , up_prob , 1)[0]

    def next_state(self , state: State) -> State:
        next_move_up = self.up_move(state)
        return Process2.State(price = state.price + 2 * next_move_up - 1 , is_prev_move_up = (next_move_up == 1))


def process2_price_traces(
        start_price: int,
        num_traces: int,
        time_steps: int,
        alpha2: float
) -> np.ndarray:
    process = Process2(alpha2 = alpha2)
    start_state = process.State(price = start_price , is_prev_move_up = None)
    return np.vstack([(np.fromiter(s.price for s in itertools.islice(simulation(process , start_state)
                                                                     , time_steps + 1 )) , float)
                      for _ in range(num_traces)])


# Let us now design proccess 3
@dataclass
class Process3:
    alpha3: float = 1.0
    @dataclass
    class State:
        num_of_up_moves: int
        num_of_down_moves: int

    def up_prob(self , state: State) -> float:
        if state.num_of_up_moves == 0 and state.num_of_up_moves == 0:
            return 0.5
        return 1/(1 + (state.num_of_up_moves/state.num_of_down_moves) ** self.alpha3)

    def next_state(self , state: State) -> State:
        up_move: int = binomial(1 , self.up_prob(state) , 1)[0]
        return Process3.State(num_of_up_moves = state.num_of_up_moves + up_move ,
                              num_of_down_moves = state.num_of_down_moves - up_move + 1
                              )

def process3_price_traces(
        num_traces: int,
        time_steps: int,
        alpha3: float,
        start_price: int
) -> np.ndarray:
    process = Process3(alpha3 = alpha3)
    start_state = process.State(0 , 0)
    return np.vstack(
        [
            np.fromiter(
                (
                    start_price + s.num_of_up_moves - s.num_of_down_moves for s in
                    itertools.islice(simulation(process, start_state), time_steps + 1
                )
            ), float) for _ in range(num_traces)
        ]
    )




# @dataclass
# class Process1:
#
#     @dataclass
#     class State:
#         price: int
#
#     level_parameter: int
#     alpha1: float = 0.25
#
#
#     def up_prob(self , state: State):
#         return 1/(1 + np.exp(-self.alpha1 * (self.level_parameter - state.price)))
#
#     def next_state(self , state: State) -> State:
#         up_move: int = binomial(1 , self.up_prob(state) , 1)[0]
#         return Process1.State(price = state.price + up_move * 2 - 1)
#
#
# def simulation(process , init_stat):
#     state = init_stat
#     while True:
#         yield state
#         state = process.next_state(state)
