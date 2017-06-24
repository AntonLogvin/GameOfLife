import json

class Configuration:

    def __init__(self, j):
        # self.cellwidth = cellwidth;
        # self.cellhight = cellhight;
        # self.startCellsList = startCellsList;
        object = json.loads(j)
        self.__dict__ = object

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
