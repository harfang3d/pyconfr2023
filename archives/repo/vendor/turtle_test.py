# turtle creation
import turtle                # import the turtle module
t = turtle.Turtle()          # create your turtle and give him or her a name

# screen setup (optional)
screen = turtle.Screen()     # create the screen
screen.setup(800, 600)       # set up the screen to be 800 x 600
screen.bgcolor("lightblue")  # set the color

# turtle properties
t.clear()                    # clear the current drawing
t.shape("turtle")            # can be "classic", "arrow", "circle", or "turtle"
t.color("red")               # set the color
t.pensize(5)                 # set the pen size for drawing
t.speed(10)                  # set turtle speed, and 0 is the fastest

# doodle around
t.write('Hey Dude!')         # write something
t.write('Hi', font=('Arial', 60, 'normal')) # change font and size
t.up()                       # lift up the pen so that no trace is left
t.goto(20, 100)              # move to position (20, 30)
t.down()                     # put down the pen to leave a trace
t.stamp()                    # stamp the shape
t.forward(100)               # move forward 100 pixels
t.left(90)                   # turn left 90 degrees
t.backward(50)               # move backward 50 pixels
t.right(90)                  # turn right 90 degrees

# draw circles
t.circle(20)                 # draw a circle with radius 20
t.begin_fill()               # begin_fill and end_fill will fill the area
t.circle(-30)                # draw a circle with radius 30 ("-" makes it clockwise)
t.end_fill()
t.circle(40, 180)            # draw a portion of circle - 180 out of the full circle (360 degrees)
t.hideturtle()               # hide the turtle shape
t.showturtle()               # show the turtle shape

