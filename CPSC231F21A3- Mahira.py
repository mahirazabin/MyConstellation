
# Description: Write a program which takes in files, reads them and displays what's inside.


import fileinput
import sys
import os
import turtle

# STARTER CONSTANTS
BACKGROUND_COLOR = "black"
WIDTH = 600
HEIGHT = 600
# AXIS CONSTANTS
AXIS_COLOR = "blue"
# STAR CONSTANTS
STAR_COLOR = "white"  # Named Stars
STAR_COLOR2 = "grey"  # Unnamed Stars

def get_color(constellation_counter):
    if constellation_counter % 3 == 0:
        return "red"
    elif constellation_counter % 3 == 1:
        return "green"
    elif constellation_counter % 3 == 2:
        return "yellow"



def setup():
    """
    Setup the turtle window and return drawing pointer
    :return: Turtle pointer for drawing
    """
    turtle.bgcolor(BACKGROUND_COLOR)
    turtle.setup(WIDTH, HEIGHT, 0, 0)
    screen = turtle.getscreen()
    screen.delay(delay=0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer = turtle
    pointer.hideturtle()
    pointer.speed(0)
    pointer.up()
    return pointer


def argumentHandler(argv):
    """
    :param argv: Is the list of arguments sent to the program
    :return: [bool -names, stars-location-file ]
    """
# case1: argv = ["-names", "-names"]
# case2: argv = ["amin.dat", "amin.dat"]
# case3: argv = ["amin.dat", "-names"]
# case4: argv = ["-names", "amin.dat"]

    foundNames = False
    starLoc = None

    if len(argv) > 2:
        print("Error; inputs cannot be more than 3")
        exit()


    elif len(argv) == 2:
        for i in argv:
            if i == '-names':
                if foundNames == False:
                    foundNames = True
                else:
                    print('Neither args are star location file.')
                    exit()
            else:
                if starLoc is None:
                    starLoc = i

                else:
                    print('Neither args are -names.')
                    exit()


    elif len(argv) == 1 :
        i = argv[0]
        if i == '-names':
            foundNames = True
        else:
            starLoc = i


    if starLoc is None:
        starLoc = input('Enter your star-location-file:')
    if not os.path.isfile(starLoc):
        print('Error! No ' + starLoc + ' exists.')
        exit()
    return foundNames, starLoc


def star_files(filename):
    try:
        inStarFile = open(filename, 'r')
    except:
        sys.exit("Input file is not valid.")

    #Lists and dictionaries to store star info
    star_list = []
    star_dict = {}

    for line in inStarFile:
        line = line.strip()
        star_info_list = line.split(",")




        if star_info_list[6] != "":
            name = star_info_list[6].split(";")[0]
        else:
            name = None
        x = float(star_info_list[0])
        y = float(star_info_list[1])
        mag = float(star_info_list[4])
        star_list.append([x,y,mag,name])
        
        num = 1

        if  name is not None:
            for name in star_info_list[6].split(";"):
                star_dict[name] = [x,y,mag]


    inStarFile.close()
    return star_list, star_dict


def constellation_file(filename):
    try:
        constFile = open(filename, 'r')
    except:
        sys.exit("Input file is not valid.")
    
    constName = constFile.readline()
    edges = []

    for line in constFile:
        line = line.strip()
        values = line.split(",")
        edges.append(values)
    

    constFile.close()

    return constName, edges

def screen_coord(star_x, star_y):

    calc_x_coord = (star_x + 1) * WIDTH/2
    calc_y_coord = (star_y + 1) * HEIGHT/2

    return calc_x_coord, calc_y_coord


def draw_constellation(pointer, constName, edges, star_dict, color):

    for edge in edges:
        star1_name = edge[0]
        star1_info = star_dict.get(star1_name)
        star1_x, star1_y = star1_info[0], star1_info[1]
        star2_name = edge[1]
        star2_info = star_dict.get(star2_name)
        star2_x, star2_y = star2_info[0], star2_info[1]
        pointer.penup()
        star1_x, star1_y = screen_coord(star1_x, star1_y)
        star2_x, star2_y = screen_coord(star2_x, star2_y)
        pointer.goto(star1_x, star1_y)
        pointer.pendown()
        pointer.color(color)
        pointer.goto(star2_x, star2_y)

    


def draw_line(pointer, x_begin, y_begin, x_end, y_end):
    pointer.goto(x_begin, y_begin)
    pointer.pendown()
    pointer.goto(x_end, y_end)
    pointer.penup()


def draw_axes(pointer):

    # list containing axis labels
    labels_axis = []

    # pointer variable for iterating over label dictionary
    label_pointer = -1

    # loop to populate axis labels list
    for value in range(-100, +125, +25):
        labels_axis.append(value/100)

    # set pointer color for axes
    pointer.color(AXIS_COLOR)
    
    WIDTH_STEP = int(WIDTH / 8)
    WIDTH_HALF = int(WIDTH/2)
    HEIGHT_STEP = int(HEIGHT / 8)
    HEIGHT_HALF = int(HEIGHT/2)

    # draw horizontal axis
    draw_line(pointer,0,HEIGHT_HALF,WIDTH,HEIGHT_HALF)
    # draw horizontal axis ticks and labels
    for step in range(0, WIDTH + WIDTH_STEP, WIDTH_STEP):
        draw_line(pointer, step, HEIGHT_HALF-10, step, HEIGHT_HALF +10)

        #axis ticks drawn

        pointer.setpos( step, HEIGHT_HALF-30)
        pointer.pendown()
        if (label_pointer < len(labels_axis)):
            label_pointer = label_pointer + 1
            pointer.write(labels_axis[label_pointer], align = "left")
        pointer.penup()
        #label draw done

    # draw vertical axis
    draw_line(pointer, WIDTH_HALF, 0, WIDTH_HALF, HEIGHT)

    #reset label_pointer value for use in y axis loop
    label_pointer = -1

    #draw vertical axis ticks and labels
    
    for step in range(0, HEIGHT + HEIGHT_STEP, HEIGHT_STEP):
        draw_line(pointer, WIDTH_HALF-10, step, WIDTH_HALF+10, step)
        #axis ticks drawn

        pointer.setpos(WIDTH_HALF-30, step)
        pointer.pendown()
        if (label_pointer < len(labels_axis)):
            label_pointer = label_pointer + 1
            pointer.write(labels_axis[label_pointer], align= "left")
        pointer.penup()
        #label draw done

def draw_star(pointer, x, y, mag, name, need_name):
    diameter = 10 / (mag + 2)
    pointer.penup()
    x, y = screen_coord(x, y)
    pointer.goto(x,y)
    pointer.pendown()
    if name != None:
        pointer.color(STAR_COLOR)
        pointer.dot(diameter)
        if(need_name == True):
            pointer.penup()
            pointer.goto(x, y + diameter + 10)
            pointer.pendown()
            pointer.write(name, font=("Arial", 5, "normal"))
    else:
        pointer.color(STAR_COLOR2)
        pointer.dot(diameter)

def draw_stars(pointer, starList, need_name):
    for star in starList:
        draw_star(pointer, star[0], star[1], star[2], star[3], need_name)
    

def main():
    """
    Main constellation program
    :return: None
    """
    # Handle arguments
    need_name, starLocFile = argumentHandler(sys.argv[1:])
    # print(need_name, starLocFile)
    
    pointer = setup()

    # Read star information from file (function)
    starList, starDict = star_files(starLocFile)
    # print()
    # print()
    # print(starDict)
    # print(starList)
    # Turns off draw update until turtle.update() is called
    turtle.tracer(0)

    # Draw Axes (function)
    draw_axes(pointer)
    turtle.update()
    

    # Draw Stars (function)
    draw_stars(pointer, starList, need_name)
    turtle.update()

    
    # Loop getting filenames
    filename = input('Enter constellation file:')
    counter = 0
    while filename != "":
        # Read constellation file (function)
        constName, edges = constellation_file(filename)
        # Draw Constellation (function)
        color = get_color(counter)
        draw_constellation(pointer, constName, edges, starDict, color)
        turtle.update()
        # Draw bounding box (Bonus) (function)
        turtle.update()

        # Next filename
        counter += 1
        filename = input('Enter constellation file:')


main()
print("\nClick on window to exit!\n")
turtle.exitonclick()
