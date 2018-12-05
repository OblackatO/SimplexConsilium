"""
Created on 25th October 2018 by
blackat.
"""

from typing import List
from .Goal import Goal
from .Individual import Individual


class SimplexConsilium:

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.todo: List[Goal] = []
        self.doing: List[Goal] = []
        self.done: List[Goal] = []
        self.accomplished = False
        self.individuals: List[Individual] = []

    def addtodo(self, goal: Goal):
        """Adds a Goal to the TODO list.

        :rtype: False if Goal already in TODO list.
        :param goal: Some Goal to be added to the TODO list.
        """
        if goal not in self.todo:
            self.todo.append(goal)
            return
        return False

    def add_doing(self, goal: Goal):
        """Adds a Goal to the DOING list.

        :rtype: False if Goal already in DOING list.
        :param goal: Some Goal to be added to the DOING list.
        """
        if goal not in self.doing:
            self.doing.append(goal)
            return
        return False

    def add_done(self, goal: Goal):
        """Adds a Goal to the DONE list.

        :rtype: False if Goal already in DONE list.
        :param goal: Some Goal to be added to the DOING list.
        """
        if goal not in self.doing:
            self.done.append(goal)
            return
        return False

    def removetodo(self, goal: Goal):
        """Removes a Goal from the TODO list.

        :rtype: False if Goal is not in TODO list.
        :param goal: Some Goal to be removed from the TODO list.
        """
        if goal not in self.todo:
            self.todo.remove(goal)
            return
        return False

    def removedoing(self, goal: Goal):
        """Removes a Goal from the DOING list.

        :rtype: False if Goal is not in DOING list.
        :param goal: Some Goal to be removed from the DOING list.
        """
        if goal not in self.doing:
            self.doing.remove(goal)
            return
        return False

    def addindividual(self, individual: Individual) -> bool:
        """Adds an individual to the project.

        :param individual: The individual to add to the project.
        """
        if individual.name in [individual.name for individual in self.individuals]:
            return False
        self.individuals.append(individual)
        return True

    def removeindividual(self, individual: Individual):
        """Removes an individual from the project. The individual will
        also be removed from all the goals of the project, except the
        done goals.

        :param individual: The individual to remove from the project.
        """

        for goal in self.todo:
            if individual in goal.individuals:
                goal.individuals.remove(individual)
        for goal in self.doing:
            if individual in goal.individuals:
                goal.individuals.remove(individual)

    def gather_goals_description_by_index(self, index: int) -> dict:
        """Gets description of the Goals of all three
        boards: TODO, DOING, DONE, according to a specified index.

        :param index: The position to get the Goals of each Board.
        """
        goals = dict()
        has_todo = False
        has_doing = False
        has_done = False
        for goal in self.todo:
            if self.todo.index(goal) == index:
                goals['0'] = str(goal)
                has_todo = True
        for goal in self.doing:
            if self.doing.index(goal) == index:
                goals['1'] = str(goal)
                has_doing = True
        for goal in self.done:
            if self.done.index(goal) == index:
                goals['2'] = str(goal)
                has_done = True

        if not has_todo:
            goals['0'] = ""
        if not has_doing:
            goals['1'] = ""
        if not has_done:
            goals['2'] = ""

        return goals

    @property
    def accomplished(self):
        for goal in self.doing:
            if not goal.accomplished:
                return False
        for goal in self.todo:
            if not goal.accomplished:
                return False
        return True

    @accomplished.setter
    def accomplished(self, isaccomplished:bool):
        if isaccomplished:
            for goal in self.doing:
                goal.accomplished = True
            for goal in self.todo:
                goal.accomplished = True
            self.__accomplished = True
        else:
            self.__accomplished = False

    def todoc(self):
        """Converts the object to json to be stored in
        a json file.
        """
        return {"project_name": self.project_name,
                "todo": [goal.todoc() for goal in self.todo],
                "doing": [goal.todoc() for goal in self.doing],
                "done": [goal.todoc() for goal in self.done],
                "individuals": [individual.todoc() for individual in self.individuals]}

