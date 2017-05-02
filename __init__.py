from __future__ import division
from turtle import Turtle
import math, time


def angle(x1, y1, x2, y2):
    if x1 == x2:
        return 90
    else:
        return math.atan((y2 - y1)/(x2 - x1))*180/math.pi

class Tool:
    def __init__(self):
        self.commands = ["G90 G00 X0 Y0 Z5 S500 M3",
                         "G00 Z-5 F100"]
        self.t = Turtle()
        self.least_count = 4

    # this is only for visualization
    def change_speed(self, speed):
        if speed <= 10 and speed >= 1:
            self.t.speed(speed)
            print "Speed changed"
        else:
            raise ValueError("Enter values only between 1 - 10. 1 being slowest, 10 being the fastest")
            print "No change in speed!"

    def setheading(self, angle):
        self.t.setheading(angle)
        print "Heading changed"

    def forward(self, value):
        """
        move the tool in forward direction
        """
        self.t.forward(value)
        to_x, to_y = self.t.position()
        g_command = "G01 X{} Y{}".format(round(to_x), round(to_y))
        self.commands.append(g_command)
        print g_command

    def backward(self, value):
        """
        move the tool in backward direction
        """
        self.t.backward(value)
        g_command = "G01 X{} Y{}".format(*self.t.position())
        self.commands.append(g_command)
        print g_command

    def up(self, value):
        """
        move the tool in y axis direction
        """
        self.t.setheading(90)
        self.t.forward(value)

    def down(self, value):
        """
        move the tool in negative y axis
        """
        self.t.setheading(270)
        self.t.forward(value)

    def right(self, angle):
        """
        Turn the tool in right hand
        side direction
        """
        self.t.right(angle)
        print "A right turn"

    def left(self, angle):
        """
        Turn the tool in left hand side direction
        """
        self.t.left(angle)
        print "A left turn"

    def goto(self, x, y):
        """
        Send the tool to the given location
        """
        curr_x, curr_y = self.t.position()
        self.t.setheading(angle(curr_x, curr_y, x, y))
        self.t.goto(x, y)
        g_command = "G01 X{} Y{}".format(*self.t.position())
        self.commands.append(g_command)
        print g_command

    def rapid_move(self, x, y):
        """
        Move the tool rapidly.
        Turtle: pu()
        """
        # turtle pen up
        self.t.pu()
        # turtle goto point
        self.t.goto(x, y)
        # turtle pen down
        self.t.pd()
        g_command = "G00 X{} Y{} Z5".format(x, y)
        print g_command
        self.commands.append(g_command)
        g_command = "G00 Z-5"
        print g_command
        self.commands.append(g_command)


    def arc_angle(self, radius, angle, cw = True):
        g_command = "G03 "
        if cw == True:
            radius *= -1
            g_command = "G02 "
        # current postion of the turtle
        curr_x, curr_y = self.t.position()
        # draw the turtle after 50% of circle
        self.t.circle(radius, angle/2)
        # get the current position
        middle_x, middle_y = self.t.position()
        # draw the remaining circle
        self.t.circle(radius, angle/2)
        # get the position at the end
        end_x, end_y = self.t.position()
        # slope of bisector of chord 1
        if end_y == curr_y:
            m1 = 90
        else:
            m1 = -1*((end_x - curr_x)/(end_y - curr_y))
        # slope of bisector of chord 2
        if middle_y == end_y:
            m2 = 90
        else:
            m2 = -1*((middle_x - end_x)/(middle_y - end_y))
        # mid point of chord 1
        mid_1 = ((end_x + curr_x)/2,(end_y + curr_y)/2)
        # mid point of chord 2
        mid_2 = ((middle_x + end_x)/2, (middle_y + end_y)/2)
        # intercept of line 1
        c1 = mid_1[1] - m1 * mid_1[0]
        # intercept of line 2
        c2 = mid_2[1] - m2 * mid_2[0]
        # center of the circle x cordinate
        cen_x = (c1 - c2)/(m2 - m1)
        # center of the circle y cordinate
        cen_y = m1*cen_x + c1
        # relative i
        i = -1*round(curr_x - cen_x, self.least_count)
        # relative j
        j = -1*round(curr_y - cen_y, self.least_count)
        g_command += "X{} Y{} I{} J{}".format(round(end_x, self.least_count),
         round(end_y, self.least_count), i, j)
        self.commands.append(g_command)
        print g_command

    def arc_centre(self, cen_x, cen_y, to_x, to_y, cw = True):
        # get the current position
        curr_x, curr_y = self.t.position()
        # find the radius of the circle
        radius = math.sqrt((cen_x - curr_x)**2 + (cen_y - curr_y)**2)
        # find the radius using the to position
        check_radius = math.sqrt((cen_x - to_x)**2 + (cen_y - to_y)**2)
        # check if the radius matches
        if radius != check_radius:
            raise ValueError("Please check the values you have entered")
            return None
        # slope of the line joining current and center
        tetha1 = angle(curr_x, curr_y, cen_x, cen_y)
        # slope of the line joining center and to
        tetha2 = angle(to_x, to_y, cen_x, cen_y)
        # angle between two lines
        tetha = abs(tetha1 - tetha2)
        # send the values to the arc_angle method
        self.arc_angle(radius, tetha, cw)

    def arc(self, radius, to_x, to_y, cw = True):
        # current position of the tool
        curr_x, curr_y = self.t.position()
        # linear distance between curr and to
        d = math.sqrt((curr_x - to_x)**2 + (curr_y - to_y)**2)
        # distance between curr and perpendicular bisector
        d = d/2
        # getting the angle
        tetha = math.asin(d/radius)*180/math.pi
        # two times the tetha will give total angle
        angle = 2*tetha
        # give the values to arc_angle
        self.arc_angle(radius, angle, cw)


    def arc_center_angle(self, cen_x, cen_y, angle, cw = True):
        g_command = "G03 "
        if cw == True:
            g_command = "G02 "
        curr_x, curr_y = self.t.position()
        radius = math.sqrt((curr_x - cen_x)**2 + (curr_y - cen_y)**2)
        # slope of perpendicular line joining curr and cen
        m = -1*((cen_x - curr_x)/(cen_y - curr_y))
        # change the heading to turn the turtle
        self.t.setheading(math.atan(m)*180/math.pi)
        # draw arc angle
        self.arc_angle(radius, angle, cw)

    def circle_center(self, cen_x, cen_y, radius, cw = True):
        g_command = "G03 "
        if cw == True:
            radius *= -1
            g_command = "G02 "
        self.rapid_move(cen_x, cen_y-radius)
        self.t.circle(radius)

    def square(self, side):
        for i in xrange(4):
            self.t.forward(side)
            self.t.right(90)
        print "Square of Side {} drawn".format(side)


    def generate_g_code(self):
        close_commands = ["G00 X0 Y0 Z0 M5", "M30"]
        self.commands.extend(close_commands)
        print "================================================"
        print "================ G Commands ===================="
        print "================================================"
        final_code = "\n"
        i = 1
        for command in self.commands:
            final_code += "N{} ".format(i) + command + "\n"
            i += 1
        print final_code
        print "================================================"