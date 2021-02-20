{-  YOUR NAME: Joe Arriaga

----------------------------------------------------------------------
CS457/557 Functional Languages, Spring 2018                 Homework 5
----------------------------------------------------------------------
-}

module HW5 where
import Control.Monad
import Data.List
              
{- 
----------------------------------------------------------------------
For Credit Exercises:  Your solutions to the following questions are
due by email to cs457acc@pdx.edu at the start of class (2pm) on May 16.

Mailing instructions: Your mail should have the subject line "HW5".
The body of the mail message is unimportant. Your mail should have
the following attachments:

a copy of this Haskell file, with answers and missing
    definitions filled in.

Some of the problems below will be worked during class; your
submission script can include answers for these, but they will not be
graded.

-}

{-

----------------------------------------------------------------------
Question 1 
------------------

(a) Define a function

-}

same :: IO Bool
same = do x <- getLine
          y <- getLine
          if x == y then
            do putStrLn ("yes")
               return True
          else 
            do putStrLn("no")
               return False
{-

that (i) reads two lines from standard input; (ii) if the two lines are identical, prints ``yes'' 
and otherwise prints ``no''; (iii) returns the value True iff the two lines are identical.


(b) Define a function 

-}

average :: IO ()
average = do n <- getLine
             xs <- replicateM (read n) getLine
             let lst = (map (\x -> (read x :: Int)) xs)
             print (calculateAverage lst)


calculateAverage xs = realToFrac (sum xs) / genericLength xs

{-
that reads a number (call it n) from standard input, then reads a further
n numbers, and finally prints out their average on standard output.  You can assume that each number appears on 
a separate line of the input.  You can convert strings to numbers using the read function from the Prelude.
Try to keep the core functionality (computing the average) separate from the IO processing as much as possible.

(c) Define a function 

-}

while :: IO Bool -> IO () -> IO ()
while test oper = do cond <- test
                     if cond then
                        do oper
                           while test oper
                     else
                        putStrLn "Ending"

{-

such that (while test oper) repeatedly performs oper as long as test equals True.

Here's an example of how this function might be used (using the  'same' function from part (a)):

while same
      (putStrLn " - not different yet")

-}

{- 
----------------------------------------------------------------------
Question 2 (Hudak) 
-----------

The following code from Paul Hudak, "The Haskell School of Expression,"
defines types of Shapes and Regions,
intended to represent regions of the plane. They 
given meaning via `containsS` and `containsR` operators.

Instructions for the question are below the code...

-}

data Shape = Rectangle Side Side
           | Ellipse Radius Radius
           | RtTriangle Side Side
           | Polygon [Vertex]
     deriving Show

type Radius = Float
type Side   = Float
type Vertex  = (Float,Float)

square s = Rectangle s s

circle r = Ellipse r r

type Coordinate = (Float,Float)

containsS :: Shape -> Coordinate -> Bool
(Rectangle s1 s2) `containsS` (x,y)
   = let t1 = s1/2; t2 = s2/2
     in (-t1<=x) && (x<=t1) && (-t2<=y) && (y<=t2)
(Ellipse r1 r2) `containsS` (x,y)
   = (x/r1)^2 + (y/r2)^2 <= 1
(Polygon pts) `containsS` p
   = let leftOfList = map (isLeftOf p) 
                          (zip pts (tail pts ++ [head pts]))
     in and leftOfList
(RtTriangle s1 s2) `containsS` p
   = (Polygon [(0,0),(s1,0),(0,s2)]) `containsS` p

infixr 5 `Union`
infixr 6 `Intersect`

data Region = Shape Shape             -- primitive shape
            | Translate Vector Region -- translated region
            | Scale      Vector Region -- scaled region
            | Complement Region -- inverse of region
            | Region `Union` Region   -- union of regions
            | Region `Intersect` Region -- intersection of regions
            | Region `Xor` Region -- XOR of regions
            | Empty                   -- empty region
            | HalfPlane Vector Vector -- infinite region to the left of the line
                                      -- formed by the two point vectors
     deriving Show

type Vector = (Float,Float)

r1 `difference` r2 = r1 `Intersect` (Complement r2)

univ = Complement Empty

isLeftOf :: Coordinate -> Ray -> Bool
(px,py) `isLeftOf` ((ax,ay),(bx,by))
       = let (s,t) = (px-ax, py-ay)
             (u,v) = (px-bx, py-by)
         in  s*v >= t*u

type Ray = (Coordinate, Coordinate)

containsR :: Region -> Coordinate -> Bool
(Shape s) `containsR` p
   = s `containsS` p
(Translate (u,v) r) `containsR` (x,y)
   = let p = (x-u,y-v) in r `containsR` p
(Scale (u,v) r) `containsR` (x,y)
   = let p = (x/u,y/v) in r `containsR` p
(Complement r) `containsR` p 
   = not (r `containsR` p)
(r1 `Union` r2)     `containsR` p
   = r1 `containsR` p || r2 `containsR` p
(r1 `Intersect` r2) `containsR` p
   = r1 `containsR` p && r2 `containsR` p
(r1 `Xor` r2) `containsR` p
   = let a = r1 `containsR` p
         b = r2 `containsR` p
     in (a || b) && not (a && b)
Empty `containsR` p 
   = False
(HalfPlane p1 p2) `containsR` p
   = p `isLeftOf` (p1,p2)

--TESTS
halfPlane_test1 = (HalfPlane (0,0) (10,0)) `containsR` (1,1)
halfPlane_test2 = (HalfPlane (10,0) (0,0)) `containsR` (1,1)

{- 
Your job is to make the following modifications to the code above:

(a) Add a constructor HalfPlane to the Region data type such that
HalfPlane p1 p2 denotes the infinite region, or half plane, to the
left of the line formed by the two points p1 and p2. Extend the 
definition of containsR to include this constructor.

(b) Suppose we had no Polygon Shape constructor.  To replace it,
define a function 

polygon :: [Coordinate] -> Region

that realizes convex polygons as a Region 
in terms of HalfPlane (and possibly other constructors).
Naturally, we want

polygon xs `containsR` p == (Polygon xs) `containsS` p

-}

polygon :: [Coordinate] -> Region
polygon []    = Empty
polygon [x]   = Empty
polygon [x,y] = Empty
polygon pts   = foldr Intersect univ partial_regions
                 where partial_regions = map (\(x,y) -> HalfPlane x y) (zip pts (tail pts ++ [head pts]))

--TESTS
poly_shape = [(0,0), (2,0), (2,2), (0,2)]
polygon_test1 = (polygon poly_shape) `containsR` (1,1)
polygon_test2 = (polygon poly_shape) `containsR` (3,1)
polygon_test3 = (polygon (reverse poly_shape)) `containsR` (1,1)
{-

----------------------------------------------------------------------
Question 3 
-----------


Just as a set containing elements of type a can be represented by a function of type 
(a -> Bool), so a dictionary (finite map) with keys of type k and values
of type  v can be represented by a function of type 

-}

type Dict k v = k -> Maybe v

{-
Suppose we want to define an abstract data type of such dictionaries.
(This would be the body of a suitable module definition, but we omit
the module framework here.)

Complete the following implementation by giving definitions of find and insert.
Assume that inserting with a key that is already present replaces
the old value with the new one.
(Hint: Let the types be your guide!)
-}

empty :: Dict k v
empty = \k -> Nothing

find :: Dict k v -> k -> Maybe v
find dict key = dict key

insert :: Eq k => Dict k v -> k -> v -> Dict k v
insert dict key value = \key -> Just value
