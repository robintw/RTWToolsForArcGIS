# ------ Snap Point to Line ------
# Author: Robin Wilson (robin@rtwilson.com)
# Description: Move the points in points so that they
#              lie on top of the nearest line
# --------------------------------

import arcgisscripting, sys

gp = arcgisscripting.create()

points = sys.argv[1]
lines = sys.argv[2]

# Load the Analysis toolbox so that the Near tool is available
gp.toolbox = "analysis"

# Perform the Near operation looking for the nearest line
# (from the lines Feature Class) to each point (from the
# points Feature Class). The third argument is the search
# radius - blank means to search as far as is needed. The
# fourth argument instructs the command to output the
# X and Y co-ordinates of the nearest point found to the
# NEAR_X and NEAR_Y fields of the points Feature Class
gp.near(points, lines, "", "LOCATION")

# Create an update cursor for the points Feature Class
# making sure that the NEAR_X and NEAR_Y fields are included
# in the return data
rows = gp.UpdateCursor(points, "", "", "NEAR_X, NEAR_Y")

row = rows.Next()

# For each row
while row:
    # Get the location of the nearest point on one of the lines
    # (added to the file as fields by the Near operation above
    new_x = row.GetValue("NEAR_X")
    new_y = row.GetValue("NEAR_Y")

    # Create a new point object with the new x and y values
    point = gp.CreateObject("Point")
    point.x = new_x
    point.y = new_y

    # Assign it to the shape field
    row.shape = point

    # Update the row data and move to the next row
    rows.UpdateRow(row)
    row = rows.Next()