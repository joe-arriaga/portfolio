YOUR NAME: Joe Arriaga

----------------------------------------------------------------------
CS457/557 Functional Languages, Spring 2017                 Homework 2
----------------------------------------------------------------------

This is a literate Haskell script that can be loaded directly into ghci.

>module HW2 where
> import Data.List(inits)

----------------------------------------------------------------------
For Credit Exercises:  Your solutions to the following questions are
due by email to cs457acc@pdx.edu at the start of class (2pm) on April 18.

Mailing instructions: Your mail should have the subject line "HW2".
The body of the mail message is unimportant. Your mail should have
the following attachments:

a copy of this literate Haskell file, with answers and missing
    definitions filled in.

Some of the problems below will be worked during class; your
submission script can include answers for these, but they will not be
graded.

----------------------------------------------------------------------
Question 1 (Jones):
-------------------
Explain what each of the following functions does.  (Note that
your answers should reflect the behavior of each function at a
high-level and should not just be a restatement of the Haskell
syntax.  For example, you could say that (sum . concat) is a
function that "adds up all of the values in a list of list of
numbers", but you wouldn't get credit for saying that it is
"the composition of the sum and concat functions".)

 a) odd . (1+)
 b) odd . (2*)
 c) ([1..]!!)
 d) (!!0)
 e) reverse . reverse
 f) reverse . tail . reverse
 g) map reverse . reverse . map reverse

ANSWER:
a) Given an integer, determines if the integer argument is even
b) Given an integer, returns False. The integer argument is multiplied by two
   which makes it even, then 'odd' will always return False.
c) Given an integer, increments it by one.
d) Given a list, returns the first element of the list.
e) Given a list, returns the list.
f) Given a list, removes the last element from the list.
g) Given a list of lists, reverses the order of the lists.

----------------------------------------------------------------------
Question 2 (Hutton):
--------------------

Do textbook Ch. 5, questions 6 and 9.

Define factors:

> factors :: Int -> [Int]
> factors n = [x | x <- [1..n], n `mod` x == 0]

Define perfects:

> perfects :: Int -> [Int]
> perfects m = [n | n <- [1..m], (sum (init (factors n))) == n]

Define scalarproduct:

> scalarproduct :: [Int] -> [Int] -> Int
> scalarproduct xs ys = sum [(xs !! i) * (ys !! i) | i <- [0..((length xs)-1)]]

*Note: Assuming that length xs == length ys

----------------------------------------------------------------------
Question 3:
-----------

The function

> isPrefixOf :: Eq a => [a] -> [a] -> Bool

answers whether the first argument is a prefix
of the second. Equivalently, isPrefixOf xs ys
returns true iff there exists a list zs such
that xs++zs = ys.	
      
(a) Define isPrefixOf using a list comprehension.
(Hint: use the inits function defined in class,
which can be imported from the Data.List module.)

> isPrefixOf xs ys = foldr (||) False [xs == a | a <- inits ys]

(b) Give an alternative definition of isPrefixOf
(call it isPrefixOf') using explicit recursion.

> isPrefixOf' []     []                 = True
> isPrefixOf' []     _                  = True
> isPrefixOf' _      []                 = False
> isPrefixOf' (x:xs) (y:ys) | x == y    = isPrefixOf' xs ys
>                           | otherwise = False

----------------------------------------------------------------------
Question 4 (Hutton):
--------------------
      
Do textbook Ch. 6 questions 7 and 8:

Define merge:

> merge :: Ord a => [a] -> [a] -> [a]
> merge []     xs                 = xs
> merge xs     []                 = xs
> merge (x:xs) (y:ys) | x <= y    = x : merge xs (y:ys)
>                     | otherwise = y : merge (x:xs) ys

Define msort (and any auxiliary functions you need):

> halve :: Ord a => [a]  -> ([a],[a])
> halve xs = splitAt ((length xs) `div` 2) xs
> 
> msort :: Ord a => [a] -> [a]
> msort [] = []
> msort [x] = [x]
> msort xs = merge (msort l) (msort r)
>   where (l,r) = halve xs

----------------------------------------------------------------------
Question 5:
-----------

(a) Define a function

> inserts :: a -> [a] -> [[a]]
> inserts x []     = [[x]]
> inserts x (y:ys) = (x:y:ys) : (map (y:) rc)
>   where rc = inserts x ys

such that inserts x xs is the list of lists produced
by inserting x into every possible position in xs.
For example, insert 0 [1,2,3] should produce the list
[[0,1,2,3],[1,0,2,3],[1,2,0,3],[1,2,3,0]].
Hint: look at the definitions of inits and subsets
given in class.

(b) Use inserts to define a function 

> perms :: [a] -> [[a]]
> perms [x]    = [[x]]
> perms (x:xs) = concat (map (inserts x) (perms xs))

that returns all permutations of its input list.
Note: this function is defined in Data.List, but
you should not look at that definition (which
in any case you may find quite mysterious!)

----------------------------------------------------------------------
Question 6:
-----------

In this question, "using foldr" means writing a definition
that invokes foldr in an essential way to perform all
the recursion required.  

(a) Define the list concatenation function (which is already in the Prelude) using a foldr:

> concat' :: [[a]] -> [a]
> concat' xs = foldr (++) [] xs
               
Also, write down a law, similar to those shown in class,
      that relates concat and ++

ANSWER:
concat [xs,ys] = xs ++ ys

(b) It is easy to write an arbitrary map as a foldr, for example like this:

    map f = foldr ((:).f) []       

   Give an argument based on types to show why
   it is _not_ possible to write an arbitrary foldr as a map.
   That is, explain why we cannot complete the following definition
   (for arbitrary c and n):	

    foldr c n = map ...


ANSWER:
foldr :: Foldable t => (a -> b -> b) -> b -> t a -> b
map :: (c -> d) -> [c] -> [d]

'map' takes in a list as its final argument and prduces a list as its result. If
we assume 'foldr' is equivalent and will also take in the same type of list as
its final argument and produce a the same type of list as its result its type
signature becomes:
      ie. b = [d], a = [c]
      foldr :: Foldable t => ([c] -> [d] -> [d]) -> [d] -> [c] -> [d]

We now see that the function and the types required by 'foldr' are fundamentally
different from the function and types of 'map', so it is not guaranteed that we
can write an equivalent expression.

(c) Define the tail function using a foldr. (This is a little challenging!)

> tail' :: [a] -> [a]
> tail' (x:xs) = foldr (:) [] xs

----------------------------------------------------------------------
Question 7 (Hutton):
--------------------

Do textbook Ch. 7 question 6.

> unfold                     :: (a -> Bool) -> (a -> b) -> (a -> a) -> a -> [b]
> unfold p h t x | p x       = []
>                | otherwise = h x : unfold p h t (t x)

Define chop8, map, iterate using unfold.

> chop8 :: [a] -> [[a]]
> chop8  = error "define me!"

> map' :: (a -> b) -> [a] -> [b]
> map' = error "define me!"

> iterate' :: (a -> a) -> a -> [a]
> iterate' = error "define me!"
