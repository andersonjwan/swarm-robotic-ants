from pyrep import PyRep
import numpy as np
from numpy import linalg as la

class Unit():
    def __init__(self, pyrep: PyRep):
        self._pyrep = pyrep

        # unit traits
        self.max_speed = 1.0
        self.max_force = 5.0

    def getLocation(self):
        ints, floats, strings, byte = self._pyrep.script_call(
            function_name_at_script_name='getLocation@unitScript',
            script_handle_or_type=1,
            ints=(),
            floats=(),
            strings=(),
            bytes=''
        )

        return np.array([floats[0], floats[1]])

    def getVelocity(self):
        ints, floats, strings, byte = self._pyrep.script_call(
            function_name_at_script_name='getVelocity@unitScript',
            script_handle_or_type=1,
            ints=(),
            floats=(),
            strings=(),
            bytes=''
        )

        return np.array([floats[0], floats[1]])

    def applyForce(self, force):
        self._pyrep.script_call(
            function_name_at_script_name='applyForce@unitScript',
            script_handle_or_type=1,
            ints=(),
            floats=([force[0], force[1]]),
            strings=(),
            bytes=''
        )

    def seek(self, target) -> float:
        position = self.getLocation()
        desired  = np.subtract(target, position)
        desired = (desired / la.norm(desired)) * self.max_speed

        steer = np.subtract(desired, self.getVelocity())
        steer = np.clip(steer, None, self.max_force)

        self.applyForce(steer)
        return la.norm(target - position)