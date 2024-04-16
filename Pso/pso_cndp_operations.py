""" Replacement Operations """

import copy
import math
import random


class OperationsSet:
    """

    A set of operations that can be performed on position and velocity vectors.

    """

    def __init__(
        self,
        difference_operator,
        addition_operator,
        multiplication_by_scalar,
        addition_velocity,
    ):
        """

        Initializes the operations set with the provided functions.



        Args:

            difference_operator (function): Calculates the velocity vector from two position vectors.

            addition_operator (function): Calculates the new position vector from a position vector and a velocity vector.

            multiplication_by_scalar (function): Multiplies a velocity vector by a scalar number.

            addition_velocity (function): Calculates the new velocity vector from two velocity vectors.

        """

        self.difference_operator = difference_operator

        self.addition_operator = addition_operator

        self.multiplication_by_scalar = multiplication_by_scalar

        self.addition_velocity = addition_velocity


def r_position_difference(position1, position2):
    """Calculates the difference between two position vectors."""

    pos1_minus_2 = position1.vector - position2.vector

    pos2_minus_1 = position2.vector - position1.vector

    replacements = {}

    for coordinate2, coordinate1 in zip(pos2_minus_1, pos1_minus_2):

        replacements[coordinate2] = coordinate1

    return replacements


def apply_velocity(position, velocity):
    """Applies velocity changes to a position."""

    new_vector = copy.deepcopy(position.vector)

    for i in velocity.vector:

        if i not in new_vector:

            if (
                velocity.vector[i] not in velocity.vector
                and velocity.vector[i] in new_vector
            ):

                new_vector.remove(velocity.vector[i])

                new_vector.add(
                    random.choice(
                        list(
                            set(range(0, position.max_value))
                            - new_vector
                            - set(velocity.vector.keys())
                            - set(velocity.vector.values())
                        )
                    )
                )

        elif velocity.vector[i] not in new_vector:

            new_vector.remove(i)

            new_vector.add(velocity.vector[i])

    assert len(new_vector) == len(position.vector)

    return new_vector


def r_velocity_multiply_scalar(velocity, scalar):
    """Multiplies a velocity vector by a scalar."""

    l = len(velocity.vector)

    new_vector = {}

    if scalar <= 1:

        number_of_elements_to_keep = math.floor(scalar * l) + int(
            random.random() <= scalar * l % 1
        )

        keep = random.sample(list(velocity.vector.keys()), k=number_of_elements_to_keep)

        for coordinate in keep:

            new_vector[coordinate] = velocity.vector[coordinate]

    elif scalar > 1:

        scalar -= 1

        number_of_over_changes = min(
            scalar * l + int(random.random() <= scalar * l % 1), l
        )

        change = random.sample(velocity.vector.keys(), k=number_of_over_changes)

        new_vector = copy.deepcopy(velocity.vector)

        for coordinate in change:

            new_vector[coordinate] = random.choice(
                list(
                    set(range(0, velocity.max_value))
                    - new_vector.keys()
                    - velocity.vector.keys()
                    - velocity.vector.values()
                )
            )

    else:

        raise Exception("scalar<0")

    return new_vector


def velocity_plus_velocity(velocity_1, velocity_2):
    """Combines two velocity vectors."""

    new_vector = {}

    for coordinate1 in velocity_1.vector:

        if coordinate1 in velocity_2.vector:

            if velocity_2.vector[coordinate1] in new_vector.values():

                choice = 0

            else:

                choice = random.randint(0, 1)

        else:

            choice = 0

        new_vector[coordinate1] = [velocity_1.vector, velocity_2.vector][choice][
            coordinate1
        ]

    for coordinate2 in velocity_2.vector:

        if (
            coordinate2 not in velocity_1.vector
            and velocity_2.vector[coordinate2] not in new_vector.values()
        ):

            new_vector[coordinate2] = velocity_2.vector[coordinate2]

    return new_vector


REPLACEMENT_OPERATIONS = OperationsSet(
    r_position_difference,
    apply_velocity,
    r_velocity_multiply_scalar,
    velocity_plus_velocity,
)
