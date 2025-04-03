from typing import cast, Any

import Rhino.Geometry as rg #type:ignore
import math
import ghpythonlib.treehelpers as th #type:ignore

# DECLARE INPUT VARIABLES OF PYTHON COMPONENT
x_points = cast(int, x_points)  # type: ignore
y_points = cast(int, y_points)  # type: ignore

#START CONDING HERE 
# create series of point along the X axis, the number of points is given by x_points
# the X coordinate of the point at each iteration should be incremented by 10
# the Y coordinate of the point at each iteration should be 0
#store the point in a list a=[]
a = []
for i in range(x_points):
    a.append(rg.Point3d(i*10, 0, 0))
#create a second list of points b=[], that corresponds with the list a, but this time
# assign the Y coordinate of each point to a value that comes from an external input which is y_points,
# store the in list b=[]
b = []
for i in range(x_points):
    b.append(rg.Point3d(i*10, y_points, 0))
#initialize another empty list to store some lines
#make another for loop that iterates through each point in any of the list BY INDEX
#within this loop, make a line that draws from points in both lists with the same index
#and append that line to the line list. output the result
line_list = []
for i in range(x_points):
    line = rg.Line(a[i], b[i])
    line_list.append(line)
#give the list of line as output c=[]
c = line_list

#initialize another empty list to store some curves
#interate through every line in the line list with  'for' loop 
#inside the scope of this 'for' loop, create an empty list to store the division points
#inside the 'for' loop, convert each line to a nurbs curve, store them in a list of curves 
list_curve = []
for i in range(len(line_list)):
    curve = line_list[i].ToNurbsCurve()
    list_curve.append(curve)
#output the result as d=[]
d = list_curve

#divide the new curve into 10 points by applying DivideByCount() method (see rhinocommo) and store the result in nested list parameters = []

parameters = []
for i in range(len(list_curve)):
    parameters.append(list_curve[i].DivideByCount(10, True))
#you need to iterate through the list of params with another for loop and get the point per each param 
#using Line.PointAt(), and there the points in the list of divison points allDivPts = [] #this will be a list of lists
allDivPts = []
#iterate through the each line in the line list with  'for' loop
for i in range(len(list_curve)):
    #generate list for points per curve at the parameter points_at=[]
    points_at = []  
    #iterate through the parameter points of the curve with 'for' loop
    for j in range(len(parameters[i])):
        #get the point on line [i] at parameter [j]
        point = list_curve[i].PointAt(parameters[i][j])
        points_at.append(point)
    allDivPts.append(points_at)
#output the result as e=[] with python grasshopper th.list_to_tree
e = th.list_to_tree(allDivPts)

#5.- apply sine function to points
#here we will use the sin() the math library to move the points in Z
#first, create a nested for loop to iterate the nested list by index
#second, transfor the pt to a vector3d
#third, get the vector length (it´s one of it´s properties)
#forth, create a variable that will be the magnitude of displacement, by passign the vector length to the math.sin() function
#fifth, create another 3d vector, which is is the Z vector times the previous variable
#sixth, get a new point by substracting the point to the vector (literally, a point - a vector results in another point)
#finally, append that point to a list, and then append that list to the nested list


allMovedPts = [] #list of all moved points
for i in range(len(allDivPts)):
    MovedPoints  = [] #list of moved points for each curve
    for j in range(len(allDivPts[i])):
        #get the point at index [j] in the list of points at index [i]
        point = allDivPts[i][j]
        #get the vector length of the point
        vector_length = math.sqrt(point.X**2 + point.Y**2 + point.Z**2)
        #create a variable that will be the magnitude of displacement, by passign the vector length to the math.sin() function
        displacement = math.sin(vector_length)
        #create another 3d vector, which is is the Z vector times the previous variable
        z_vector = rg.Vector3d(0, 0, displacement)
        #get a new point by substracting the point to the vector (literally, a point - a vector results in another point)
        new_point = point - z_vector
        MovedPoints.append(new_point)
    allMovedPts.append(MovedPoints)
#output the result as f=[]
f = th.list_to_tree(allMovedPts)   
