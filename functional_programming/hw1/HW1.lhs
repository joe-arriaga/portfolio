YOUR NAME: Joe Arriaga

----------------------------------------------------------------------
CS457/557 Functional Languages, Spring 2018                 Homework 1
----------------------------------------------------------------------

This is a literate Haskell script (.lhs file) that can be loaded
directly into ghci or compiled with ghc.

In .lhs files, only lines beginning with a > in the left margin
are treated as Haskell code; all other lines (like this one)
are just free-form text. There must be a blank line between   
each block of Haskell lines and non-Haskell lines.

> module HW1 where

----------------------------------------------------------------------
Reading: Reach Chapters 1-3 from the textbook (note that Chapters 1-2
are available for free on-line).  Test your understanding by working
through the exercises at the end of each chapter; in most cases, the
solutions are included at the end of the book.  You are not expected
to turn in your solutions to the exercises from Chapters 1 and 2.
Note that some of these exercises ask you to define new functions like
"product", "last", or "init" ... but those particular functions are
already defined in the standard prelude, so you will get an error if
you try to define a new version.  In these cases, you can just pick a
different name, such as "product1", "mylast", or "otherinit".

----------------------------------------------------------------------
For Credit Exercises:  Your solutions to the following questions are
due by email to cs457acc@pdx.edu at the start of class (2pm) on April 11.

Mailing instructions: Your mail should have the subject line "HW1".
The body of the mail message is unimportant. Your mail should have
the following attachments:

(i) a copy of this literate Haskell file, with answers and missing
    definitions filled in.
(ii) a .txt or .ppm file containing your fractal graphic in answer
     to question 3.  
(ii) one or more .lhs files showing the code that produced
     your fractal graphic in question 3.

Some of the problems below will be worked during class; your
submission script can include answers for these, but they will not be
graded.

----------------------------------------------------------------------
Question 1 (Jones): 
-------------------
Explain what the following Haskell function does:

> dup    :: (a -> a -> a) -> a -> a
> dup f x = f x x

ANSWER:
'dup' takes a function and a parameter. The function takes two arguments of the
same type and produces a value also of that type. The parameter can be any type.
'dup' causes the provided function 'f' to use the parameter 'x' for both its
arguments.

Now consider the following two functions, and show how each of them
can be rewritten using dup:

> double  :: Integer -> Integer
> double n = 2 * n

> double' :: Integer -> Integer
> double' n = dup (+) n
> -- or just:
> --  double' = dup (+)
> 

> square  :: Integer -> Integer
> square n = n * n

> square'  :: Integer -> Integer
> square' n  = dup (*) n
> -- or just:
> --   square' = dup (*)
	
----------------------------------------------------------------------
Question 2 (Thompson):
----------------------
USING NO EXPLICIT RECURSION, define a function 

> memberCount :: Eq a  => [a] -> a -> Int
> memberCount xs x = (length . filter (== x)) xs

such that (memberCount xs x) returns the number of times the item x
appears in the list xs.

Use memberCount to define a function

> member :: Eq a => [a] -> a -> Bool
> member xs x = if memberCount xs x > 0
>               then True
>               else False

such that (member xs x) returns True iff x appears in xs.

Use memberCount to define a function

> once :: Eq a => [a] -> [a]
> once xs = filter (\x -> (memberCount xs x) == 1) xs

that returns a list of the items that occur exactly once in the argument list.
For example, once [2,4,2,1,4,3] = [1,3].


----------------------------------------------------------------------
Question 3 (Jones):
-------------------
Experiment with the fractal program that we constructed in class, 
which is available (in several variants) from the class web page. 
Your goal is to produce a new and attractive fractal image, no bigger
than a page, by modifying some (or all) of the parameters such as the
range of points, the size of the grid, the characters in the palette, or
even the fractal function.   Every student should submit a different
image.  Be sure to describe the changes that you've made.  The purpose
of this question is to make sure that you understand how the fractal
program works, and that you are comfortable modifying and running it.
So make sure that you achieve those goals, but don't spend too long on
this question (although we might give "artistic" awards for especially
nice images). 

You should submit your result image as .txt file
(for an ascii graphic) or as a .ppm file (for a PPM graphic).
You should also submit any modified .lhs files you used
to produce that graphic. These files should be attachments
in your submission email.

Answer:
By changing the formula used in the 'next' function the program produces a
different set of points for the set and the shape in the image changes.
By simply tweaking the numerical factor in the formula used to calculate the
second component of the pair the mandelbrot image can be stretched or compressed
in very interesting ways. The image of the entire set is easiest to see
because the change leaves the set within the same region. The effects also
affect the other regions but because the stretching or compressing causes
many of the points to be translated across the image the borders of the image
must also be moved to show interesting parts of the set.  

----------------------------------------------------------------------
Question 4 (Jones):
-------------------
The Haskell prelude includes an operator !! for selecting a numbered
element of the list, with the first element starting at index 0.  For
example, [1..10] !! 0 is 1, while [1..10] !! 7 is 6.  Give a
definition for a Haskell function revindex that performs the same
indexing function as (!!) except that it starts counting from the end
of the input list.  For example, revindex [1..10] 0 should return 10,
while revindex [1..10] 7 whould return 3.

ANSWER: [write your function definition here]

> revindex :: [a] -> Int -> a
> revindex xs i = (reverse xs) !! i

----------------------------------------------------------------------
Question 5 (Jones):
-------------------
WITHOUT USING ANY EXPLICIT RECURSION, given Haskell definitions for
the following functions:

> powerOfTwo :: Int -> Integer
> powerOfTwo n = (!!) (iterate (2*) 1) n

  (powerOfTwo n) returns the value of 2 to the power n.  For example,
  powerOfTwo 8 should return 256.  Of course, your answer should *not*
  use the built in Haskell functions for raising a value to a power!

> logTwo :: Integer -> Int
> logTwo 0 = 1
> logTwo v = length (takeWhile (<=v) (iterate (2*) 1))

  (logTwo v) returns the smallest integer n such that v <= powerOfTwo n.
  [To put it another way, (logTwo v) returns the number of bits that are
  needed to represent any integer between 0 and v-1.]

> copy :: Int -> a -> [a]
> copy n x = take n (repeat x)

  (copy n x) returns a list containing n copies of the value x.  For
  example, copy 3 True should give [True, True, True].  (The Haskell
  prelude includes a similar function called replicate; of course, you
  should not use replicate in your answer.)

> multiApply :: (a -> a) -> Int -> a -> a
> multiApply f n x = (!!) (iterate f x) n

  (multiApply f n x)  returns the value that is obtained when the
  function f is applied n times to the value x.  For example,
  multiApply square 2 2, should return 16, while
  multiApply not 0 True will return True.

Now suppose that we define the following function using multiApply:

> q f n m x = multiApply (multiApply f n) m x

What is the type of this function, and what exactly does it do?

ANSWER:
q :: (a -> a) -> Int -> a -> a
It applies f composed with itself n*m times to x.

----------------------------------------------------------------------
Question 6 (Jones):  
-------------------
Consider the following fragment of Haskell code:

> strange xs = head (head (reverse (takeWhile notnull (iterate twirl xs))))
> notnull xs = not (null xs)
> twirl xs   = reverse (tail xs)

Explain carefully what the function does.  You may want to type this
code in to a Hugs script and try running tests or using the :t command
to provide clues.  Can you suggest an alternative definition for
strange that is more efficient, more concise, and also easier to
understand?

ANSWER:
It gives the middle element of the list 'xs'. If 'xs' has an even number of
elements it "rounds up" and gives the first element of the second half of the
list.

Alternative version here:

> strange' :: [a] -> a
> strange' xs = (!!) xs (div (length xs) 2)

----------------------------------------------------------------------

