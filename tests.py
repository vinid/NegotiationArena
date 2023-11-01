from objects.utils import *
from objects.resource import *
from objects.goal import *

g1 = Goal({"X": 15, "Y": 15, "Z": 15})

p1 = Resources({"X": 25, "Y": 5})
p2 = Resources({"X": 5, "Y": 25, "Z": 30})
p3 = Resources({"X": 15, "Y": 15, "Z": 15})
p4 = Resources({"X": 35, "Y": 15, "Z": 15})
p5 = Resources({"X": 35, "Y": 15, "Z": 15, "N": 100})

assert g1.goal_reached(p1) == False
assert g1.goal_reached(p2) == False
assert g1.goal_reached(p3) == True
assert g1.goal_reached(p4) == True
assert g1.goal_reached(p5) == True
assert g1.equal(p3) == True
assert g1.equal(p2) == False
assert p2.equal(p2) == True