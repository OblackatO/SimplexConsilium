"""
Created on 24th October 2018 by
blackat.
"""

import re
from typing import List
from .Individual import Individual
from .DateFormat import DateFormat
from datetime import datetime


class Goal:

    def __init__(self, name: str):
        """Something that should be accomplished in a project, not a task
        . Refer to theSelect a date type first. description of the project if you want to know more.

        :param name: The name of the goal.
        """
        self.name: str = name
        self.description: str
        self.ID: str = None
        self.individuals: List[Individual] = []
        self.date_type: DateFormat = None
        self.init_date = None

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def individual(self):
        return self.__individual

    @individual.setter
    def individual(self, individual):
        if not isinstance(individual, Individual):
            raise Exception("individual MUST be of type Individual")
            return
        self.__individual = individual

    @property
    def init_date(self):
        return self.__init_date

    @init_date.setter
    def init_date(self, creation_date):
        if not creation_date:
            self.__init_date = None

        if not self.date_type:
            return

        if self.date_type == DateFormat.BigEndian:
            string_match = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', creation_date)
            if string_match:
                self.__init_date = datetime.strptime(creation_date, "%Y-%m-%d")

        string_match = re.match(r'[0-9]{2}-[0-9]{2}-[0-9]{4}', creation_date)
        if self.date_type == DateFormat.LittleEndian:
            if string_match:
                self.__init_date = datetime.strptime(creation_date, "%d-%m-%Y")

        elif self.date_type == DateFormat.MiddleEndian:
            if string_match:
                self.__init_date = datetime.strptime(creation_date, "%m-%d-%Y")

    def createhash(self):
        """In every python session a random seed is established to
        generate a hash, the ID of a Goal is fixed in its creation process."""

        self.ID = str(hash(self))

    def addindividual(self, individual: Individual):
        """Adds an Individual to accomplish the goal.

        :param individual: The Individual to add.
        """
        if individual not in self.individuals:
            self.individuals.append(individual)
        else:
            raise Exception("Individual: {} is already in this goal".format(individual.name))

    def removeindividual(self, individual: Individual):
        """Removes an Individual from a the Goal.

        :param individual: The Individual to remove.
        """
        if individual not in self.individuals:
            self.individuals.remove(individual)
        else:
            raise Exception("Individual: {} could not be found".format(individual.name))

    def __hash__(self):
        """Bitwise or on two main attributes: Name and description."""
        name_hash = hash(self.name)
        description_hash = hash(self.description)
        return (name_hash | description_hash) % 10000

    def __eq__(self, other):
        """Two goals that have the same name and description
        should be considered equal. It does not matter if the creation
        date is different or the assigned Individuals are also different.
        """
        if not isinstance(other, Goal):
            return False
        return(self.name == other.name and
               self.description == other.description)

    def __str__(self):
        description = "     [Name]--[ID]:"+self.name+" -- "+self.ID+""
        description += "    [Description]:"+self.description+""
        description += "    [Individuals]:"
        for individual in self.individuals:
            description += "/"+individual.name
        return description

    def todoc(self):
        """Converts the object to json to be stored in
        a json file.
        """
        if not self.date_type:
            date_type_doc = None
        else:
            date_type_doc = self.date_type.value
        return {"name": self.name,
                "description": self.description,
                "ID": self.ID,
                "individuals": [individual.todoc() for individual in self.individuals],
                "date_type": date_type_doc,
                "init_date": str(self.init_date)
                }
