{-  YOUR NAME: Joe Arriaga

-----------------------------------------------------------------------------
CS457/557 Functional Languages, Spring 2018                 Homework 3 part 2
-----------------------------------------------------------------------------

-}

module HW3part2 where
import Graphics.Gloss
       
{- 
----------------------------------------------------------------------
For Credit Exercises:  Your solutions to the following questions are
due by email to cs457acc@pdx.edu at the start of class (2pm) on April 25.

Mailing instructions: Your mail should have the subject line "HW3p2".
The body of the mail message is unimportant. Your mail should have
the following attachments:

a copy of this Haskell file, with answers and missing
    definitions filled in.

-}

{-

----------------------------------------------------------------------
Question 3:
-----------

This question involves the use of the Haskell Gloss library for generating
graphics to the screen using the OpenGL API.  

Do "cabal install gloss" to download and install the gloss package
and its dependencies first.

You'll want to explore the documentation at https://hackage.haskell.org/package/gloss  
For this assignment, you just need to write functions that produce 
a value of type Picture.  To display a picture p, write a function such as 

f = display (InWindow "my picture" (768,512) (20,20)) white p

where the picture will be given a window of size 768x512, offset at (20,20)
from the top left of the screen, with a white background color.

To actually display the picture, you can run ghci with the flag 
-fno-ghci-sandbox, load your .hs file, and evaluate f. 
Alternatively, if you call your function 'main' you can compile 
your .hs with ghc and run the resulting executable. 

To exit from the display function, type escape in the display window.
(Interrupting the Haskell program may be difficult or impossible.)

-}

f p = display (InWindow "my picture" (768,512) (20,20)) white p
{-

(a) You'll see that gloss defines a number of helper functions to define
special cases of pictures, e.g. circleSolid and rectangleWire, in terms
of the existing Picture constructors.

Write a similar helper function 

-}

squareWire :: Point -> Point -> Picture
squareWire (x1,y1) (x2,y2) = lineLoop [(x1,y1), (x2,y1), (x2,y2), (x1,y2)]
{-

such that squareWire p1 p2 produces a (wireframe, unfilled) square 
where p1 and p2 are the endpoints of one of the diagonals.

Math hint: If v = (vx,vy) is a vector, then two perpendicular
vectors of the same length are given by (-vy,vx) and (vy,-vx).

(b) Write a similar helper function

-}

ellipseSolid :: Point -> Point -> Float -> Picture
ellipseSolid = error "fill in here"

{-

such that solidEllipse p1 p2 d produces a solid (filled) ellipse 
where p1 and p2 are the endpoints of one centerline of the ellipse,
and d is length of the perpendicular centerline.

Math hint: If v = (vx,vy) is a vector, the (counterclockwise) 
angle v makes with the x axis is given by arctan(vy/vx).
Note that the Haskell atan function returns an angle in radians.

(c) Write a function

-}

area :: Picture -> Float
area = error "fill in here"

{-
that returns the total area (in square pixels) of the _solid_ elements
of the picture.  More specifically: elements Polygon, ThickCircle,
ThickArc, and Bitmap have area, but Blank, Line, Circle, Arc, and Text
do not.  Be sure to handle Translate, Rotate, and Scale modifiers
appropriately. For simplicity, assume that the area of Pictures
element is just the sum of the areas of the underlying list.

Math hint: Google for the "shoelace formula."

(d) Use the geometric constructors of the gloss library to create a picture

-}

me :: Picture
me = [translate 0 80 Color aquamarine (rectangleSolid 120 20),
     Color magenta (rectangleSolid 20 140),
     translate -40 80 Color rose (thickArc 180 359 60  20)]

{-

containing a big representation of the first letter of your name.
Be inventive; use a variety of shapes and colors. Do _not_ use the 
Text picture element.

-}
