from turtle import Turtle


class Tool:
    def __init__(self):
        self.t = Turtle()
        self.x = 0
        self.y = 0
        self.z = 0
        self.command = []

    def forward(self, value):
        self.t.forward(value)
        self.x, self.y = self.t.position()
        g_command = "G01 X{} Y{}".format(self.x, self.y)
        print g_command
