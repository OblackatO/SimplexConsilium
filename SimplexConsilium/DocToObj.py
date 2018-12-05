from .Goal import Goal
from .SimplexConsilium import SimplexConsilium
from .DateFormat import DateFormat
from .Individual import Individual
from .Boards import Board
import json


class DocToObj:

    def __init__(self):
        self.simplex_project = None

    def initsimplexproject(self, project_file_path: str) -> SimplexConsilium:
        """Converts a dumped SimplexConsilium object
        to an object again.
        """
        with open(project_file_path, 'r') as project_file:
            data = json.project_fileloads(project_file.read())
            simplex_project = SimplexConsilium(data['project_name'])
            self.simplex_project = simplex_project

            if data['todo']:
                self.__deserialization_flow(data['todo'], Board.TODO)
            else:
                self.simplex_project.todo = []

            if data['doing']:
                self.__deserialization_flow(data['doing'], Board.DOING)
            else:
                self.simplex_project.doing = []

            if data['done']:
                self.__deserialization_flow(data['done'], Board.DONE)
            else:
                self.simplex_project.done = []

            if data['individuals']:
                for individual in data['individuals']:
                    self.simplex_project.addindividual(self.__initindividual(individual))
            else:
                self.simplex_project.individuals = []

            return simplex_project

    def __deserialization_flow(self, data: dict, board: Board):
        """Inits Goals and adds them to the project.

        :param data: A dictionary with the data loaded(json.loads) from
        one of the three Goal lists: todo, doing, done.
        """
        for goal in data:
            goal_obj = self.__initgoal(goal)
            for individual in goal['individuals']:
                individual_obj = self.__initindividual(individual)
                goal_obj.addindividual(individual_obj)
            if board == Board.TODO:
                self.simplex_project.addtodo(goal_obj)
            elif board == Board.DOING:
                self.simplex_project.add_doing(goal_obj)
            else:
                self.simplex_project.add_done(goal_obj)

    def __initgoal(self, goal: dict) -> Goal:
        """Converts a dumped Goal dict to an object.

        :param goal: A dictionary with information about a Goal.
        :rtype: Goal
        """
        goal_obj = Goal(name=goal['name'])
        goal_obj.description = goal['description']
        goal_obj.ID = goal['ID']
        if goal['date_type'] == None:
            goal_obj.date_type = None
        else:
            goal_obj.date_type = DateFormat(goal['date_type'])
        goal_obj.init_date = goal['init_date']
        return goal_obj

    def __initindividual(self, individual: dict) -> Individual:
        """Converts a dumped Individual dict to an object.

        :param individual: A dictionary with information about an Individual.
        :return: Individual
        """
        individual_obj = Individual(name=individual['name'])
        return individual_obj
