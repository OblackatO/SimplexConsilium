"""
Created on 25th October 2018 by
blackat.
"""

import uuid


class Individual:

    def __init__(self, name: str):
        """Someone that accomplishes a goal.

        :param name: Name of the Individual.
        """
        self.name = name

    def todoc(self):
        """Converts the object to json to be stored in
        a json file.
        """
        return {"name": self.name}

    def __str__(self):
        return self.name
