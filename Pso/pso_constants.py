# !/usr/bin/env python3
import random

from .pso_cndp_operations import OperationsSet


DEFAULT_OPERATIONS = OperationsSet(
    lambda x, y: [x.vector[i] - y.vector[i] for i in range(len(x.vector))],
    lambda x, y: [
        (
            random.randint(0, x.max_value - 1)
            if round(x.vector[i] + y.vector[i]) >= x.max_value
            or round(x.vector[i] + y.vector[i]) < 0
            else round(x.vector[i] + y.vector[i])
        )
        for i in range(len(x.vector))
    ],
    lambda x, y: list(map(lambda z: z * y, x.vector)),
    lambda x, y: [x.vector[i] + y.vector[i] for i in range(len(x.vector))],
)


DEFAULT_OPERATIONS_CONTINUOUS = OperationsSet(
    lambda x, y: [x.vector[i] - y.vector[i] for i in range(len(x.vector))],
    lambda x, y: [
        (
            random.randint(0, x.max_value - 1)
            if x.vector[i] + y.vector[i] >= x.max_value or x.vector[i] + y.vector[i] < 0
            else x.vector[i] + y.vector[i]
        )
        for i in range(len(x.vector))
    ],
    lambda x, y: list(map(lambda z: z * y, x.vector)),
    lambda x, y: [x.vector[i] + y.vector[i] for i in range(len(x.vector))],
)

RANDOM_INIT = lambda dimension, max_value: [
    random.randint(0, max_value - 1) for _ in range(dimension)
]
RANDOM_INIT_INERTIA = lambda dimension, max_value: [
    random.randint(0, max_value - 1) for _ in range(dimension)
]
NULL_INIT_INERTIA = lambda dimension, max_value: [0 for _ in range(dimension)]

SET_RANDOM_INIT = lambda dimension, max_value: set(
    random.sample(range(0, max_value), k=dimension)
)
REPLACEMENT_NULL_INIT_INERTIA = lambda dimension, max_value: {}
