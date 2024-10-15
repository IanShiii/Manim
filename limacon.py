from manim import *
from numpy import *
from math import *

innerRadius = 0.8
outerRadius = 0.8

#parametric form of limacon
def limaconParametric(theta):
    x = (innerRadius + outerRadius * cos(theta)) * cos(theta)
    y = (innerRadius + outerRadius * cos(theta)) * sin(theta)
    z = 0
    return (x, y, z)

# def spinOuterCircle(circle: Circle):
#     innerCircleTheta = acos(circle.get_x() / (innerRadius + outerRadius))
#     innerCircleTheta = innerCircleTheta if circle.get_y() > 0 else (2 * PI - innerCircleTheta)

def getOuterCircleTheta(outerCircle: Circle):
    try:
        innerCircleTheta = acos(outerCircle.get_x() / (innerRadius + outerRadius))
        innerCircleTheta = (innerCircleTheta if outerCircle.get_y() > 0 else (2 * PI - innerCircleTheta))
        return (1 + (innerRadius / outerRadius)) * innerCircleTheta
    except:
        return 0

class Limacon(Scene):
    
    def construct(self):
        title = Text("Limacons", font_size=65)
        line = Line(title.get_center(), np.array((0.0, 3.1, 0.0)))
        innerCircle = Circle(innerRadius).set_stroke(width=4)
        outerCircle = Circle(outerRadius).scale(0.95).set_stroke(width=4)
        outerCircle.set_x(innerRadius + outerRadius)

        dot = Dot(color=RED).move_to(outerCircle.get_start())
        dot.add_updater(lambda dot: dot.move_to(outerCircle.point_at_angle(getOuterCircleTheta(outerCircle))))

        self.wait(0.5)

        self.play(Write(title))
        self.play(MoveAlongPath(title, line))
        self.play(Create(innerCircle))
        self.play(Create(outerCircle))
        self.play(Create(dot))
        trace = TracedPath(dot.get_last_point).set_stroke(color=WHITE, width=1.5).make_smooth()
        self.add(trace)

        self.play(Rotate(outerCircle, angle=2*PI, about_point=ORIGIN).set_run_time(2.0))

        limacon = ParametricFunction(limaconParametric, (0, 2 * PI)).shift(LEFT * (1.0 - 0.95) * outerRadius).scale(1.97).set_stroke(color=WHITE, width=1.5)
        self.add(limacon)
        self.remove(trace.clear_updaters())

        self.wait(0.75)

        self.play(FadeOut(innerCircle, outerCircle, dot).set_run_time(1.0))
        self.wait(0.3)
        self.play(limacon.animate.move_to(np.array((0, 0, 0))))
        self.wait(0.6)

        self.play(Succession(FadeOut(title).set_run_time(1.0), FadeOut(limacon).set_run_time(1.0)))
        self.wait(1.5)