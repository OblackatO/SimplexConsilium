import argparse
import os
import pathlib
import time
import sys
from beautifultable import BeautifulTable
from SimplexConsilium.SimplexConsilium import SimplexConsilium
from SimplexConsilium.Persistor import Persistor
from SimplexConsilium.DocToObj import DocToObj
from SimplexConsilium.Individual import Individual
from SimplexConsilium.Goal import Goal
from SimplexConsilium.DateFormat import DateFormat

SUFFIX = '.json'


def RemoveGoal(goal_id: int, project: SimplexConsilium):
    """Removes a Goal from a project.

    :param goal_id: The ID of the Goal the be removed.
    :param project: The project where the Goal is in.
    """
    ShowGoal(goal_id, project)
    print()
    areysure = input("Are you sure you want to remove Goal {} (y/n):".format(goal_id))
    if areysure == 'y':
        for goal in project.todo:
            if goal.ID == goal_id:
                project.todo.remove(goal)
                print("Goal {} successfully removed.".format(goal_id))
                return
        for goal in project.doing:
            if goal.ID == goal_id:
                project.doing.remove(goal)
                print("Goal {} successfully removed.".format(goal_id))
                return
        for goal in project.done:
            if goal.ID == goal_id:
                project.todo.remove(goal)
                print("Goal {} successfully removed.".format(goal_id))
    else:
        return


def showdetailedgoal(goal: Goal):
    """Shows a more detailed and structured view
    of some Goal.

    :param goal: The goal to show in detail.
    """
    print("[Name]: {}".format(goal.name))
    print("[Description]: {}".format(goal.description))
    print("[Individuals]:")
    for individual in goal.individuals:
        print("/{}".format(individual.name), end='')
    print("[Starting date]: {}".format(goal.init_date))


def ShowGoal(goal_id: int, project: SimplexConsilium):
    """Shows all the details about a goal, including the starting
    date, if any.

    :param goalID: The ID of the Goal.
    :param project: The project where the Goal to be shown is.
    """
    for goal in project.todo:
        if goal.ID == goal_id:
            showdetailedgoal(goal)
    for goal in project.doing:
        if goal.ID == goal_id:
            showdetailedgoal(goal)
    for goal in project.done:
        if goal.ID == goal_id:
            showdetailedgoal(goal)


def MoveGoalDownward(project: SimplexConsilium):
    """Moves a Goal to the previous board.

    :param project: The project where the Goal should be moved.
    """
    while True:
        ShowProject(project)
        print("[>]Type 'stop' as goal ID, to stop moving goals forward.")
        goal_found = False
        goal_id = input("Goal ID:")
        if goal_id == "stop":
            return
        for goal in project.doing:
            if goal.ID == goal_id:
                project.todo.append(goal)
                project.doing.remove(goal)
                goal_found = not goal_found
        if not goal_found:
            for goal in project.done:
                if goal.ID == goal_id:
                    project.doing.append(goal)
                    project.done.remove(goal)
                    goal_found = not goal_found
        if not goal_found:
            print("[>]Goal: {} already done, or does not exist".format(goal_id))
            continue
        print("Goal was moved.")
        time.sleep(2)
        ClearScreen()


def MoveGoalForward(project: SimplexConsilium):
    """Moves a Goal to the next board.

    :param project: The project where the Goal should be moved.
    """
    while True:
        ShowProject(project)
        print("[>]Type 'stop' as goal ID, to stop moving goals forward.")
        goal_found = False
        goal_id = input("Goal ID:")
        if goal_id == "stop":
            return
        for goal in project.todo:
            if goal.ID == goal_id:
                project.doing.append(goal)
                project.todo.remove(goal)
                goal_found = True
        if not goal_found:
            for goal in project.doing:
                if goal.ID == goal_id:
                    project.done.append(goal)
                    project.doing.remove(goal)
                    goal_found = True
        if not goal_found:
            print("[>]Goal: {} already done, or does not exist".format(goal_id))
            continue
        print("Goal was moved.")
        time.sleep(2)
        ClearScreen()


def AddIndividualToGoal(project: SimplexConsilium):
    """Adds individuals to Goals. Please note that it is also possible to add
    Individuals to done Goals, because some Individuals might have worked on
    some Goal that is already done, but he/she was not added to that Goal when it
    was on the TODO or DOING lists.
    """
    print("[>]Type 'stop' as goal ID, to stop adding individuals to goals.")
    while True:
        goal_id = input("Goal ID:")
        if goal_id == "stop":
            return
        individual_name = input("Individual name:")
        desired_goal = None
        for goal in project.todo:
            if goal.ID == goal_id:
                desired_goal = goal
        for goal in project.doing:
            if goal.ID == goal_id:
                desired_goal = goal
        for goal in project.done:
            if goal.ID == goal_id:
                desired_goal = goal
        if desired_goal is not None:
            desired_individual = None
            for individual in project.individuals:
                if individual.name == individual_name:
                    desired_individual = individual
                    desired_goal.addindividual(individual)
            if desired_individual is None:
                print("[>]There is no Individual named:{}".format(individual_name))
                continue
        else:
            print("[>]There is no such goal: {}".format(goal_id))
        print("Individual:{} added to Goal:{}".format(individual_name, goal_id))


def ShowIndividuals(project: SimplexConsilium):
    """Shows individuals from a project.

    :param project: The project from where the individuals
    should be shown.
    """
    str_list = ', '.join(str(individual) for individual in project.individuals)
    print("[Project Individuals]: {} \n".format(str_list))


def Exit(project: SimplexConsilium):
    """Exits a loaded project and saves all changes
    made to it.

    :param project: The loaded project to exit from.
    """
    SaveChanges(project)
    print("[>]All changes were saved.")
    print("[>]Exiting...")
    time.sleep(3)
    sys.exit(0)


def SaveChanges(project: SimplexConsilium):
    """Persists all the changes made to a project in
    a json file.

    :param project: The project for which the changes should be changed.
    """
    persistor = Persistor(project.project_name)
    persistor.persistent_project(project.todoc())
    print("[>]Changes were saved.")
    time.sleep(2)
    ClearScreen()


def CreateGoals(project: SimplexConsilium):
    """Creates a number X of goals and adds them to the project.
    The created goals are automatically added to the TODO list of
    the project.

    :param project: The project where the goals should be added.
    """

    ClearScreen()
    while True:
        print("[>]Type 'stop' as goal name, to stop adding goals.")
        name = input("Goal name:")
        if name == 'stop':
            return
        description = input("Goal description:\n")
        goal = Goal(name)
        goal.description = description
        goal.createhash()
        init_date = input("Specific date to init goal(Y/N)?:")
        if init_date == 'Y':
            date_format = input("Date format\n"
                                "[1].BigEndian (<year>-<month>-<day>)\n"
                                "[2].LittleEndian (<day>-<month>-<year>)\n"
                                "[3].MiddleEndian (<month>-<day>-<year>)\n"
                                "Option:")
            if date_format == "1":
                goal.date_type = DateFormat.BigEndian
            elif date_format == "2":
                goal.date_type = DateFormat.LittleEndian
            elif date_format == "3":
                goal.date_type = DateFormat.MiddleEndian

            init_date = input("Init date:")
            goal.init_date = init_date
        project.addtodo(goal)
        print("Goal: '{}' added.".format(goal.name))
        time.sleep(2)
        ClearScreen()


def AddIndividuals(project: SimplexConsilium):
    """Adds a list of Individuals to a SimplexConsilium project.

    :param project: The project where the individuals should be added.
    """

    ClearScreen()
    while True:
        print("[>]Type 'stop' as name, to stop adding individuals.")
        name = input("Name:")
        if name == 'stop':
            return
        if project.addindividual(Individual(name=name)):
            print("[>]Individual: {} added.".format(name))
        else:
            print("[>]Individual: {} ALREADY ADDED".format(name))
        time.sleep(2)
        ClearScreen()


def ShowProject(project: SimplexConsilium):
    """Shows TODO, DOING and DONE boards on the screen, with
    their corresponding goals.

    :param project: An instance of SimplexConsilium.
    """
    ClearScreen()
    got_goals = False
    max_index = len(project.todo)
    if len(project.doing) > max_index:
        max_index = len(project.doing)
    if len(project.done) > max_index:
        max_index = len(project.done)

    table = BeautifulTable()
    table.column_headers = ["TODO", "DOING", "DONE"]
    for index in range(0, max_index):
        goals = project.gather_goals_description_by_index(index)
        table.append_row([goals['0'], goals['1'], goals['2']])
        got_goals = True
    if not got_goals:
        table.append_row(["Project empty :(", "Project empty :(", "Project empty :("])
    print(table)
    print()


def ClearScreen():
    """Clears screen according to OS."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def LoadProject(project_name: str):
    if not ProjectExist(project_name):
        print("Project: {} does not exist".format(project_name))
    docobj_converter = DocToObj()
    loaded_project = docobj_converter.initsimplexproject(project_name + SUFFIX)
    choice = None
    ClearScreen()
    print("Project: {} has been loaded.".format(loaded_project.project_name))
    time.sleep(2)
    while choice != "e":
        print("[1].Show project")
        print("[2].Add Individual(s)")
        print("[3].Create Goal(s)")
        print("[4].Add Individual(s) to Goal")
        print("[5].Move Goal forward.")
        print("[6].Move Goal downward.")
        print("[7].Show Goal")
        print("[8].Remove Goal")
        print("[9].Save changes")
        print("[e].Exit")
        choice = input("Input:")
        if choice == "1":
            ShowProject(loaded_project)
        elif choice == "2":
            AddIndividuals(loaded_project)
        elif choice == "3":
            CreateGoals(loaded_project)
        elif choice == "4":
            ShowProject(loaded_project)
            ShowIndividuals(loaded_project)
            AddIndividualToGoal(loaded_project)
            ClearScreen()
        elif choice == "5":
            ShowProject(loaded_project)
            MoveGoalForward(loaded_project)
            ClearScreen()
        elif choice == "6":
            ShowProject(loaded_project)
            MoveGoalDownward(loaded_project)
            ClearScreen()
        elif choice == "7":
            while True:
                ShowProject(loaded_project)
                print("[>]Type 'stop' as goal ID, to stop seeing goals.")
                goal_id = input("goal ID:")
                if goal_id == 'stop':
                    break
                ShowGoal(goal_id=goal_id, project=loaded_project)
                y_n = input("Continue(y/n)?:")
                if y_n == 'y':
                    continue
                else:
                    ClearScreen()
                    break
        elif choice == "8":
            while True:
                ShowProject(loaded_project)
                print("[>]Type 'stop' as goal ID, to stop seeing goals.")
                goal_id = input("goal ID:")
                if goal_id == 'stop':
                    break
                RemoveGoal(goal_id, loaded_project)
                y_n = input("Continue(y/n)?:")
                if y_n == 'y':
                    continue
                else:
                    ClearScreen()
                    break
        elif choice == "9":
            SaveChanges(loaded_project)
        elif choice == "e":
            Exit(loaded_project)


def ProjectExist(project_name: str):
    """Verifies if project exists in cwd.

    :param project_name: Name of the project
    """
    path = pathlib.Path('.')
    files = [file for file in path.iterdir() if file.is_file()]
    return pathlib.Path(project_name + SUFFIX) in files


def DeleteProject(project_name: str):
    """Deletes a project from the cwd.

    :param project_name: Name of the project to be removed.
    """
    pathlib.Path(project_name + SUFFIX).unlink()


def CreateProject(project_name: str):
    """Creates a project in the cwd.

    :param project_name: The name of the project.
    """
    project = SimplexConsilium(project_name)
    persistor = Persistor(project_name)
    persistor.persistent_project(project.todoc())


def ArgsHandler():
    """Flow of arguments. Several options shall be specified in one only command.
    Something worth noticing:
        The option -sc is the 1st one to be taken in consideration.
        The option -sd is the 2nd one to be taken in consideration.
        The option -sl is the 3th one to be taken in consideration.
    """
    description = '''
    Simple project manager made to aim simplicity, for command line freaks and alike.
    Github: https://github.com/OblackatO/SimplexConsilium
    Author: Pedro Gomes (blackat)
    Email: OblackatO@yandex.com
    '''
    epilog = "License:GPL-3.0"
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)  # usage=usage)
    parser.add_argument('-sc', '--simplexcreate', metavar=" ", help='Creates a new project: -sc <project_name>')
    parser.add_argument('-sd', '--simplexdelete', metavar=" ", help='Deletes a project: -sd <project_name>')
    parser.add_argument('-sl', '--simplexload', metavar=" ", help='Loads an existing project: -sl <project_name>')
    arguments, unknown_arguments = parser.parse_known_args()

    if unknown_arguments:
        print("[>]Unknown arguments: {}".format(unknown_arguments))
        sys.exit()

    if arguments.simplexcreate:
        if ProjectExist(arguments.simplexcreate):
            print("[>]Project already create in cwd.")
            sys.exit()
        CreateProject(arguments.simplexcreate)
        print("[>]Project: {} created.".format(arguments.simplexcreate))
    if arguments.simplexdelete:
        if not ProjectExist(arguments.simplexdelete):
            print("[>]Project does not exist.")
            sys.exit()
        DeleteProject(arguments.simplexdelete)
        print("[>]Project: {} deleted.".format(arguments.simplexdelete))
    if arguments.simplexload:
        if not ProjectExist(arguments.simplexload):
            print("[>]Project does not exist.")
            sys.exit()
        LoadProject(arguments.simplexload)


def main():
    ArgsHandler()


if __name__ == "__main__":
    main()
