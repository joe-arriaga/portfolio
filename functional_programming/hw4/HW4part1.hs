{-  YOUR NAME: [Fill in here! ]

----------------------------------------------------------------------
CS457/557 Functional Languages, Spring 2018                 Homework 4
----------------------------------------------------------------------

-}

module HW4 where
       
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
 a) not . head 
 b) let g x = if x then [True] else [] in \y -> let z = g y in y
 c) (\w -> let x = [] in let c = [x,w] in head c) [False]
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

-}

{- (MUCH) MORE TO COME!! -}