{-# #-}

{-  YOUR NAME: Joe Arriaga

----------------------------------------------------------------------
CS457/557 Functional Languages, Spring 2018                 Homework 4
----------------------------------------------------------------------

-}

module HW4 where
import DotTrees
              
{- 
----------------------------------------------------------------------
For Credit Exercises:  Your solutions to the following questions are
due by email to cs457acc@pdx.edu at the start of class (2pm) on May 2.

Mailing instructions: Your mail should have the subject line "HW4".
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
Question 1 (Jones, with modifications):
------------------
Give the most general possible types for each of the following 
expressions (or else explain why you think the expression is ill-typed).
 i) not . head 
 ii) let g x = if x then [True] else [] in \y -> let z = g y in y
 iii) (\w -> let x = [] in let c = [x,w] in head c) [False]
 etc.
 d) (\f -> (f True,f [])) (:[])
 e) let f = (:[]) in (f True, f [])
 f) [ [], [[]], [[[]]], [[[[]]]], [[[[[    ]]]]] ]
 g) [ [], [[]], [[[]]], [[[[]]]], [[[[[True]]]]] ]
 h) [ [True], [[]], [[[]]], [[[[]]]], [[[[[]]]]] ]
 i) map map
 j) map (map not)
 k) map . map
 l) (map , map)
 m) [ map id, reverse, map not ]

You may use ghci to help you answer these questions, but you
are strongly encouraged to try and figure out an answer for yourself
first, without typing it in. 

ANSWER:
i) [Bool] -> Bool
ii) 
  Bool ->                  let z = g y ???
iii) 
d) 
e) ill-typed because the definition of f does not use (:) correctly
f) 
  \f [[]] -> [ [], f [[]] ]
  \f [x] -> [x, f [x] ]
g) 
h) 
i) [a ->b] -> [[a] -> [b]]
j) [[Bool]] -> [[Bool]]
k)
l) ((a -> b) -> [a] -> [b], (c -> d) -> [c] -> [d])
m) [ [Bool]->[Bool] ]

-}

{-

----------------------------------------------------------------------
Question 2 (Jones):
-------------------

File DotTree.hs contains the code from lecture that allows a wide
variety of trees to be visualized as .dot files.  The Tree and
LabeledTree classes are appropriate for many algebraic datatypes
that are essentially tree-like, even if we don't explicitly
call them trees (e.g. the Expr type).

In this question we explore how to use the DotTree infrastructure
to draw tree-like pictures to visualize a broader range of datatypes,
including lists, pairs, and more.  For example, we'd like to display
the value 

ex1 = [(1,True),(2,False)]

as the graph described by the file ex1.dot.

[Recall that to display a .dot file, you need to install the graphviz tools
(or use them on the linuxlab machines), execute

dot -Tpng foo.dot > foo.png

and then display foo.png in your favorite browser or other viewer.]

The basic idea is to define a universal datatype for vizualization trees

-}

data VizTree = VizNode String [VizTree]

{-

and then write functions to map different datatypes to VizTree.

Naturally, we will create a class of such "visualizable datatypes"

-}

class Viz a where
  toVizTree :: a -> VizTree      	

{-

and make various types instances of that class. For example:

-}

instance Viz Integer
  where toVizTree n = VizNode (show n) []	 	

instance (Viz a, Viz b) => Viz (a, b)
  where toVizTree (a, b) = VizNode "Pair" [toVizTree a, toVizTree b]

instance Viz a => Viz [a]
  where toVizTree []     = VizNode "[]" []   
        toVizTree (x:xs) = VizNode ":" [toVizTree x,toVizTree xs]
{-

We can use the existing DotTree mechanisms to generate a .dot file
from a VizTree. (Note that a VizTree is essentially just a 
RoseTree specialized to Strings.)

Plugging everything together, we can write a function

-}

viz :: Viz a => String -> a -> IO ()
viz s = toDot s . toVizTree

{-

that takes a value and generates a file tree.dot containing
the vizualization of that value.  For example, the ex1.dot
file was produced by executing 

viz "ex1" ex1
	
Here are your tasks:

(a) Write appropriate instance declarations to make VizTree a
member of classes Tree and LabeledTree.
-}
instance Tree (VizTree) where
  subtrees (VizNode s t) = t

instance LabeledTree (VizTree) where
  label (VizNode s t) = s

{-
(b) Write appropriate instance declarations to make the 
following types into members of class Viz:

Bool
Char
Int
triples (,,)
Maybe a
BinTree a

Be sure to test your functions, e.g. on the value

Leaf (Just (True,'a',42::Int)) :^: Leaf Nothing
-}

instance Viz Bool where
  toVizTree n = VizNode (show n) []

instance Viz Char where
  toVizTree n = VizNode (show n) []

instance Viz Int where
  toVizTree n = VizNode (show n) []

instance (Show a, Show b, Show c) => Viz (a,b,c) where
  toVizTree (x,y,z) = VizNode ((show x) ++ (show y) ++ (show z)) []

instance Show a => Viz (Maybe a) where
  toVizTree Nothing = VizNode "" []
  toVizTree (Just a) = VizNode (show a) []

instance Show a => Viz (BinTree a) where
  toVizTree (Leaf x) = VizNode (show x) []
  toVizTree (l:^:r) = VizNode "" [toVizTree l, toVizTree r]
  

{-
(c) What happens when you visualize a String? 
What happens if you try to improve that visualization
by declaring an instance of the form below?

instance Viz String 
  where toVizTree s = VizNode (show s) []

Note: to follow the recommendations in the error message,
you can add the following pragma between the # marks in the very
first line of this file:

LANGUAGE TypeSynonymInstances,FlexibleInstances

But this still won't really help!  What is going on?

-}


{-
Question 3 (Hudak):
-------------------

Consider the type

-}

data Rainbow  = Red | Orange | Yellow | Green | Blue | Indigo | Violet
  deriving (Show,Eq,Ord,Enum,Bounded)
{-
instance Rainbow (Enum a) where
  toEnum 0 = Red
       | 1 = Orange
       | 2 = Yellow
       | 3 = Green
       | 4 = Blue
       | 5 = Indigo
       | 6 =Violet

  fromEnum Red = 0
       | Orange = 1
       | Yellow = 2
       | Green = 3
       | Blue = 4
       | Indigo = 5
       | Violet = 6
-}

{-

If you uncomment the deriving clause, ghc will produce instances of
the five named classes for you, but it won't show you the code for
these instances.  Your task is to write instance declarations for Eq,
Ord, Enum, and Bounded by hand. (You can continue to derive Show,
which is useful for debugging.) Your instances should match the
behavior of the derived instances.

The definitions of these classes are given below for your reference.
Hint: You can save yourself a quadratic amount of typing by looking
carefully at the definitions of the Ord and Enum classes.  But be
careful of corner cases!

-- Equality and Ordered classes  
 
class  Eq a  where  
    (==), (/=) :: a -> a -> Bool  
 
        -- Minimal complete definition:  
        --      (==) or (/=)  
    x /= y     =  not (x == y)  
    x == y     =  not (x /= y)

class  (Eq a) => Ord a  where  
    compare              :: a -> a -> Ordering  
    (<), (<=), (>=), (>) :: a -> a -> Bool  
    max, min             :: a -> a -> a  
 
        -- Minimal complete definition:  
        --      (<=) or compare  
        -- Using compare can be more efficient for complex types.  
    compare x y  
         | x == y    =  EQ  
         | x <= y    =  LT  
         | otherwise =  GT  
 
    x <= y           =  compare x y /= GT  
    x <  y           =  compare x y == LT  
    x >= y           =  compare x y /= LT  
    x >  y           =  compare x y == GT

-- note that (min x y, max x y) = (x,y) or (y,x)  
    max x y  
         | x <= y    =  y  
         | otherwise =  x  
    min x y  
         | x <= y    =  x  
         | otherwise =  y

-- Enumeration and Bounded classes  
 
class  Enum a  where  
    succ, pred       :: a -> a  
    toEnum           :: Int -> a  
    fromEnum         :: a -> Int  
    enumFrom         :: a -> [a]             -- [n..]  
    enumFromThen     :: a -> a -> [a]        -- [n,n'..]  
    enumFromTo       :: a -> a -> [a]        -- [n..m]  
    enumFromThenTo   :: a -> a -> a -> [a]   -- [n,n'..m]  
 
        -- Minimal complete definition:  
        --      toEnum, fromEnum  
        --  
    succ             =  toEnum . (+1) . fromEnum  
    pred             =  toEnum . (subtract 1) . fromEnum  
    enumFrom x       =  map toEnum [fromEnum x ..]              -- produced by [x..]
    enumFromTo x y   =  map toEnum [fromEnum x .. fromEnum y]   -- produced by [x..y]
    enumFromThen x y =  map toEnum [fromEnum x, fromEnum y ..]  -- produced by [x,y..]
    enumFromThenTo x y z =                                      -- produced by [x,y..z]
                        map toEnum [fromEnum x, fromEnum y .. fromEnum z]
class  Bounded a  where  
    minBound         :: a  
    maxBound         :: a

-}

