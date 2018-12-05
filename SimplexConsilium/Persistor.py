import json


class Persistor:

    def __init__(self, project_name: str):
        self.project_name = project_name

    def persistent_project(self, project_dict: dict):
        with open(self.project_name+".json", 'w') as project_file:
            project_file.write(json.dumps(project_dict))
