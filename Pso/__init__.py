# !/usr/bin/env python3
from .pso_constants import (
    DEFAULT_OPERATIONS,
    NULL_INIT_INERTIA,
    RANDOM_INIT,
)


"""classes definitions"""


class Particle:
    """
    Represents a single particle in the particle swarm optimization algorithm.
    """

    def __init__(
        self,
        dimension,
        max_value,
        goal_function,
        w,
        c1,
        c2,
        r1,
        r2,
        operations,
        initialization,
        velocity_initialization,
        mutation,
        position=None,
        velocity=None,
    ):
        """
        Initializes a new instance of the Swarm class.

        Args:
        :param dimension: int, the number of dimensions for the particle's position and velocity vectors
        :param max_value: int, the maximum value that the elements of the position and velocity vectors can take
        :param goal_function: function, the function to be optimized by the algorithm
        :param w: float, the inertia weight factor
        :param c1: float, the cognitive weight factor
        :param c2: float, the social weight factor
        :param r1: function, the function to generate random value for the cognitive component
        :param r2: function, the function to generate random value for the social component
        :param operations: instance of the class OperationsSet
        :param initialization: function, the function to generate initial position vector for the particle
        :param velocity_initialization: function, the function to generate initial velocity vector for the particle
        :param mutation: bool, whether to enable mutation when the particle is stuck
        :param position: Position, an optional initial position for the particle
        :param velocity: Velocity, an optional initial velocity for the particle
        """
        assert position is None or len(position) == dimension
        assert velocity is None or len(velocity) == dimension
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.r1 = r1
        self.r2 = r2
        self.max_value = max_value
        self.dimension = dimension
        self.mutation = mutation
        self.goal_function = goal_function
        self.no_move_count = 0
        if position is None:
            self.position = Position(dimension, max_value, operations, initialization)
        else:
            self.position = position
        if velocity is None:
            self.velocity = Velocity(
                dimension, max_value, operations, velocity_initialization
            )
        self.cognitive_value = self.goal_function(self.position)
        self.cognitive_position = self.position

    def update_cognitive(self):
        """
        Updates the cognitive value and position of the particle if its current value is better than the cognitive one.
        """
        current_value = self.goal_function(self.position)
        if current_value > self.cognitive_value:
            self.cognitive_value = current_value
            self.cognitive_position = self.position

    def update_velocity(self, social_position):
        """
        Updates the velocity of the particle based on its current position, cognitive position, and social position.

        Args:
        :param social_position: Position, the current social position of the swarm system.
        :return None
        """
        self.velocity = self.velocity * self.w  # inertia
        self.velocity += (
            (self.cognitive_position - self.position) * self.c1 * self.r1()
        )  # cognitive component
        self.velocity += (
            (social_position - self.position) * self.c2 * self.r2()
        )  # social component

    def update_position(self):
        """
        Updates the position of the particle based on its current velocity.

        :return bool, whether the position of the particle changed or not.

        """
        last_position = self.position.vector
        self.position += self.velocity
        assert len(self.position.vector) == len(last_position)
        if last_position == self.position.vector:
            self.no_move_count += 1
        else:
            self.no_move_count = 0
        return last_position != self.position.vector


class SwarmSystem:
    """
    Represents a group of particles in the particle swarm optimization algorithm.
    Contains a list of Swarm instances, as well as the current global best position and value
    (referred to as the "social position" and "social value").
    Also contains methods for updating the position, velocity, and cognitive values of all particles
    as well as the global best position and value.
    """

    def __init__(
        self,
        dimension,
        max_value,
        goal_function,
        number_of_swarms,
        w,
        c1,
        c2,
        r1=lambda: 1,
        r2=lambda: 1,
        operations=DEFAULT_OPERATIONS,
        initialization=RANDOM_INIT,
        velocity_initialization=NULL_INIT_INERTIA,
        mutation=False,
    ):
        """
        Initializes a new instance of the SwarmSystem class.

        Args:
        :param dimension: int, the number of dimensions for the particles' position and velocity vectors
        :param max_value: int, the maximum value that the elements of the position and velocity vectors can take
        :param goal_function: function, the function to be optimized by the algorithm
        :param number_of_swarms: int, number of particles in the swarm
        :param w: float, the inertia weight factor
        :param c1: float, the cognitive weight factor
        :param c2: float, the social weight factor
        :param r1: function, the function to generate random value for the cognitive component
        :param r2: function, the function to generate random value for the social component
        :param operations: instance of the class OperationsSet
        , the set of operations for the position and velocity vectors
        :param initialization: function, the function to generate initial position vector for the particle
        :param velocity_initialization: function, the function to generate initial velocity vector for the particle
        :param mutation: bool, whether to enable mutation when the particle is stuck
        """
        self.swarms = [
            Particle(
                dimension,
                max_value,
                goal_function,
                w,
                c1,
                c2,
                r1,
                r2,
                operations,
                initialization,
                velocity_initialization,
                mutation,
            )
            for _ in range(number_of_swarms)
        ]
        self.social_value = float("-inf")
        self.social_position = None
        self.position_history = [[] for _ in range(100000)]
        self.social_history = [0 for _ in range(100000)]
        self.social_history_position = [0 for _ in range(100000)]
        self.no_moves = 0
        self.social_found_in_step = 0
        self.more_than_10_per_cent_moving_step = 0
        self.more_than_10_per_cent_moving_steps = []
        self.more_than_10_per_cent_moving_value = 0
        self.update_social(0)

    def update_social(self, step):
        """
        Updates the global best position and value (social position and social value) of the swarm system
        if a particle's cognitive value is better than the current global best value.

        Args:
        :param step: int, the current step of the algorithm.

        :return improved: bool, whether the global best value was updated or not.

        """
        improved = False
        for swarm in self.swarms:
            if (
                swarm.cognitive_value > self.social_value
            ):  # TODO maybe or equal is better
                self.social_value = swarm.cognitive_value
                self.social_position = swarm.cognitive_position
                self.social_found_in_step = step
                improved = True
        self.social_history[step] = self.social_value
        self.social_history_position[step] = sorted(list(self.social_position.vector))
        return improved

    def update_cognitive(self):
        """
        Updates the cognitive value and position of each particle if its current value is better than the cognitive one.

        :return: None
        """
        for swarm in self.swarms:
            if swarm.no_move_count == 0:
                swarm.update_cognitive()

    def update_velocity(self, wake=True):
        """
        Updates the velocity of each particle based on its current position, cognitive position, and social position.

        Args:
        :param wake: bool, whether to update all particles' velocity or ignore the particles that haven't moved for a while.

        Returns:
        None

        """
        for swarm in self.swarms:
            if wake or swarm.no_move_count < 10:
                swarm.update_velocity(self.social_position)

    def update_position(self, step, wake=True):
        """
        Updates the position of each particle based on its current velocity.

        Args:
        :param wake: bool, whether to update all particles' position or ignore the particles that haven't moved for a while.

        :returns number of moves: int, the number of particles that have moved.

        """

        number_of_moves = 0
        for swarm in self.swarms:
            if wake or swarm.no_move_count < 10:
                number_of_moves += int(swarm.update_position())
                self.position_history[step].append(sorted(list(swarm.position.vector)))
        return number_of_moves

    def run_step(self, step, wake=True):
        """
        Executes one step of the PSO algorithm, which includes updating velocity, position, cognitive values, and social values.

        Args:
        :param step: int, the current step of the algorithm
        :param wake: bool, whether to update all particles' velocity, position,
        and cognitive values or only the particles that haven't moved for a while

        :return improved : bool, whether the social value was updated or not.

        """
        self.update_velocity(wake)
        moved = self.update_position(step, wake)
        self.update_cognitive()
        improved = self.update_social(step)
        if moved > len(self.swarms) // 10:
            self.more_than_10_per_cent_moving_step = step
            self.more_than_10_per_cent_moving_value = self.social_value
        else:
            self.more_than_10_per_cent_moving_steps.append(step)

        if not moved:
            self.no_moves += 1
        else:
            self.no_moves = 0
        return improved

    def run(self, steps, convergence_condition=lambda self, step: False):
        """
        Runs the PSO algorithm for a certain number of steps or until a certain convergence condition is met.

        Args:
        :param steps: int, the number of steps to run the algorithm for.
        :param convergence_condition: function, a function that takes in the current SwarmSystem object and
         the current step as arguments and returns a bool indicating whether to stop the algorithm or not.

        :return  convergence_step: int, the number of steps the algorithm ran for or -1 if the algorithm did not converge.

        """
        improved = True
        for i in range(steps):
            if convergence_condition(self, i):
                return i - 1
            improved = self.run_step(i, improved)
        return -1


class Velocity:
    """
    A class that represents the velocity of a particle in a d-dimensional space.
    For CNP a velocity represents a function that change nodes in the position(to be deleted) by nodes that aren't (nodes that are in the residual graph)

    Attributes:
        dimension (int): The number of dimensions of the velocity vector. For CNP it's the number of nodes to be deleted
        operations (OperationsSet): An object containing functions for performing operations on the velocity vector.
        max_value (int): The maximum value of the velocity vector elements. For CNP it's the number of swarms
        initialization (function): A function that generates a new velocity vector with random values.
        vector (list or dict): The velocity vector. We use a dict for CNP
    """

    def __init__(self, dimension, max_value, operations, initialization, vector=None):
        """
        Initializes the velocity with a vector attribute. If the vector attribute is not provided, it is initialized
        using the initialization function.

        Args:
            dimension (int): The number of dimensions of the velocity vector. For CNP it's the number of nodes to be deleted
            max_value (int): The maximum value of the velocity vector elements. For CNP it's the number of swarms
            operations (OperationsSet): An object containing functions for performing operations on the velocity vector.
            initialization (function): A function that generates a new velocity vector with random values.
            vector (list or dict, optional): The velocity vector.
        """
        self.dimension = dimension
        self.operations = operations
        self.max_value = max_value
        self.initialization = initialization
        if vector is None:
            self.vector = initialization(dimension, max_value)
        else:
            self.vector = vector

    def __mul__(self, scalar_number):
        """
        The multiplication operator for a Velocity object and a scalar number. It returns a new object of the "Velocity" class.
        It uses the multiplication_by_scalar from the operations attribute to calculate the new velocity vector.

        Args:
            scalar_number (float or int): The scalar number to multiply the velocity vector by.

        Returns:
            Velocity: A new velocity object.
        """
        return Velocity(
            self.dimension,
            self.max_value,
            self.operations,
            self.initialization,
            self.operations.multiplication_by_scalar(self, scalar_number),
        )

    def __add__(self, other):
        """
        The addition operator for two Velocity objects. It returns a new object of the "Velocity" class.
        It uses the addition_velocity from the operations attribute to calculate the new velocity vector.

        Args:
            other (Velocity): The other velocity to be added.

        Returns:
            Velocity: A new velocity object.
        """
        return Velocity(
            self.dimension,
            self.max_value,
            self.operations,
            self.initialization,
            self.operations.addition_velocity(self, other),
        )


class Position:
    """
    A class that represents the position of a particle in a d-dimensional space.

    Attributes:
        dimension (int): The number of dimensions of the position vector. For CNP it's the number of nodes to be deleted
        max_value (int): The maximum value of the position vector elements. For CNP it's the number of swarms
        operations (OperationsSet): An object containing functions for performing operations on the position vector.
        initialization (function): A function that generates a new position vector with random values.
        vector (list or set): The position vector. We use a set for CNP

    """

    def __init__(self, dimension, max_value, operations, initialization, vector=None):
        """
        Initializes the position with a vector attribute. If the vector attribute is not provided, it is initialized
        using the initialization function.

        Args:
            dimension (int): The number of dimensions of the position vector. For CNP it's the number of nodes to be deleted
        max_value (int): The maximum value of the position vector elements. For CNP it's the number of swarms
            max_value (int): The maximum value of the position vector elements.
            operations (OperationsSet): An object containing functions for performing operations on the position vector.
            initialization (function): A function that generates a new position vector with random values.
            vector (list or set, optional): The position vector. We use a set for CNP
        """
        assert vector is None or dimension == len(vector)
        self.max_value = max_value
        self.dimension = dimension
        self.operations = operations
        self.initialization = initialization
        if vector is None:
            self.vector = initialization(dimension, max_value)
        else:
            self.vector = vector

    def __sub__(self, other):
        """
        The subtraction operator for two Position objects. It returns a new object of the "Velocity" class.
        It uses the difference_operator from the operations attribute to calculate the velocity vector.

        Args:
            other (Position): The other position to calculate the velocity from.

        Returns:
            Velocity: A new velocity object.
        """
        return Velocity(
            self.dimension,
            self.max_value,
            self.operations,
            self.initialization,
            self.operations.difference_operator(self, other),
        )

    def __add__(self, velocity):
        """
        The addition operator for a Position object and a Velocity object. It returns a new object of the "Position" class.
        It uses the addition_operator from the operations attribute to calculate the new position vector.

        Args:
            velocity (Velocity): The velocity to be added to the position.

        Returns:
            Position: A new position object.
        """
        return Position(
            self.dimension,
            self.max_value,
            self.operations,
            self.initialization,
            self.operations.addition_operator(self, velocity),
        )
