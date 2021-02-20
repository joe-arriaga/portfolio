{-  YOUR NAME: [Fill in here! ]

----------------------------------------------------------------------
CS457/557 Functional Languages, Spring 2018                 Homework 6
----------------------------------------------------------------------

-}

module HW6 where
import Data.Vector((!), generate)
              
{- 
----------------------------------------------------------------------
For Credit Exercises:  Your solutions to the following questions are
due by email to cs457acc@pdx.edu at the start of class (2pm) on May 30.

Mailing instructions: Your mail should have the subject line "HW6".
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
----------

Suppose you are given the following definitions

[] ++ ys = ys                        (++1)
(x:xs) ++ ys = x:(xs ++ ys)          (++2)
map f [] = []                        (map1)
map f (x:xs) = (f x):(map f xs)      (map2)

(a) Prove that for any finite lists xs,ys, and zs,

(xs ++ ys) ++ zs = xs ++ (ys ++ zs)  (++assoc)

ANSWER:

Base Case:
([] ++ ys) ++ zs  LHS
ys ++ zs          ++1 ->
(ys ++ zs)        Regrouping with parentheses
[] ++ (ys ++ zs)  ++1 <-
                  RHS

Inductive Hypothesis:
t ++ (ys ++ zs) = (t ++ ys) ++ zs


WTS: h:t ++ (ys ++ zs) = (h:t ++ ys) ++ zs

(h:t ++ ys) ++ zs       RHS
h:( t ++ ys) ++ zs      ++2 ->
h:( (t ++ ys) ++ zs)    Regrouping with parentheses
h:( t ++ (ys ++ zs))    IH <-
h:t ++ (ys ++ zs)       Regrouping with parentheses
                        LHS

(b) Prove that for any finite lists xs and ys and function f, that

map f (xs ++ ys) = map f xs ++ map f ys

[] ++ ys = ys                        (++1)
(x:xs) ++ ys = x:(xs ++ ys)          (++2)
map f [] = []                        (map1)
map f (x:xs) = (f x):(map f xs)      (map2)

ANSWER:

Base Case:
map f ([] ++ ys)      LHS
map f ys              Def. of []
[] ++ map f ys        Def. of []
map f [] ++ map f ys  map1 <-
                      RHS


Inductive Hypothesis:
map f (t ++ ys) = map f t ++ map f ys


WTS: map f (h:t ++ ys) = map f h:t ++ map f ys

map f (h:t ++ ys)           LHS
map f h:(t ++ ys)           ++2 ->
(f h):(map (t ++ ys))       map2 ->
(f h):(map f t ++ map f ys) IH ->
(f h):(map f t) ++ map f ys Regrouping with parentheses
map f (h:t) ++ map f ys     map2 <-
                            RHS


Question 2
----------

Lists are declared as an instance of Monad in the Prelude.

(a) By experimentation, figure out the 
definitions of return and >>= that the Prelude
uses for lists, and fill them in here:

instance Monad [] where
  return x = [x]
  m >>= k  = [k]


(b) The list monad is useful for describing non-deterministic
computations: a value of type [a] can be thought of as
representing a set of possible values of type a. 
(Consistent with that, the empty list [] can be thought of as 
representing an empty set of values.)

Modify and extend the original interpreter from lecture10e.hs to 
include a non-deterministic choice operator

Amb e1 e2

which yields the value of either e1 or e2.
Modify the definition of eval to use the list monad
rather than the Exn monad, i.e. it should have type

eval :: Exp -> [Int]

This eval function should return a list (possibly empty) 
of ALL possible values of the overall expression. 

Cases that originally produced an Error exception should now
instead produce an empty list.

For example,

example1 = eval (Plus (Amb (Const 1) (Const 2)) (Amb (Const 10) (Const 20)))

should return the list

[11,21,12,22]

Also, the example

example2 = eval (Amb (Div (Const 1) (Const 0)) (Const 42))

should return the list 

[42]
-}
--ANSWER:

data Exp =
           Plus Exp Exp
         | Minus Exp Exp
         | Times Exp Exp
         | Div Exp Exp
         | Const Int
         | Amb Exp Exp


eval :: Exp -> [Int]
eval (Plus e1 e2)  =
     do v1 <- eval e1
        v2 <- eval e2
        return (v1+v2)
eval (Minus e1 e2) = 
     do v1 <- eval e1
        v2 <- eval e2
        return (v1-v2)
eval (Times e1 e2) = 
     do v1 <- eval e1
        v2 <- eval e2
        return (v1*v2)
eval (Div e1 e2)   =
     do v1 <- eval e1
        v2 <- eval e2
        if v2 == 0 then
          []
        else
          return (v1 `div` v2)
eval (Const i)     =  return i

eval (Amb e1 e2) = 
     do v1 <- eval e1
        v2 <- eval e2
        if ((length [v1]) == 0) then
          return v2
        else if ((length [v2]) == 0) then
          return v1
        else
          [v1, v2]

example1 = eval (Plus (Amb (Const 1) (Const 2)) (Amb (Const 10) (Const 20)))
example2 = eval (Amb (Div (Const 1) (Const 0)) (Const 42))
example3 = eval (Amb (Const 1) (Const 42))
example4 = eval (Div (Const 1) (Const 0))
{---------------------------------------------------------------------

Question 3
----------

Recall the edit distance problem from Question 2 of Homework 3.
(Note that a sample solution to that homework is available on the web site.)

Write a new version of the transform function that uses lazy memoization
to solve this problem in polynomial time rather
than the exponential time required by the sample solution.

Hints: 

Follow the basic idea shown on slide 16 of the lecture on Laziness, 
which uses the Vector library.

You will need to find a numbering scheme to identify the sub-problems to 
solve: a simple one is to use the two indices of the positions being examined
in each list. 

To build a two-dimensional memo table, you can use a vector of vectors.

-}

-- ANSWER:
data Edit = Change Char
          | Copy
          | Delete
          | Insert Char
          | Kill
          deriving (Eq, Show)

testEdits = [Insert 'c', Change 'h', Copy, Insert 'p', Copy, Delete, Kill, Change 'l']
     

{- Write a function to compute the cost of a list of edits. -}

cost :: [Edit] -> Int   
cost []          = 0
cost (Copy:xs)   = cost xs
cost (_:xs)      = (cost xs) + 1

{- Write a function to chose the cheapest edit sequence from a collection
of such sequences. -}

best :: [[Edit]] -> [Edit]
best (x:xs) = least x (cost x) xs
              where least item minCost []     = item
                    least item minCost (x:xs) = if (cost x) < minCost then least x (cost x) xs
                                                                        else least item minCost xs
--best [xs] = xs | (cost xs) == least
--  where least = minimum (map cost [xs])
        
{- Finally, write a function transform that finds a cheapest 
edit sequence for two given strings. Hint: use recursion;
pattern match on both strings to determine which edits are 
possible, and use `best` to choose among the possibilities. -}

{-
transform :: String -> String -> [Edit] 
transform []   []   = []
transform []   ys   = map Insert ys
transform xs   []   = [Kill]
transform (x:xs) (y:ys) | x == y    = Copy : transform (length xs) (length ys)
                        | otherwise = best [Delete   : table ! ((length xs)+1) ! (length (y:ys)),
                                            Insert y : table ! (length (x:xs)) ! ((length ys)+1),
                                            Change y : table !  (length xs)    ! (length ys)]
-}
answer xs ys = table ! 0 ! 0
  where table = generate ((length xs)+1) (\n ->
                generate ((length ys)+1) (\m ->
                trans n m))
                  where trans n m | n == length xs && m == length ys = []
                                  | n == length xs                   = map Insert ys
                                  | m == length ys                   = [Kill]
                                  | xs !! n == ys !! m               = Copy : table ! (n+1) ! (m+1)
                                  | otherwise = best [Delete : table ! (n+1) ! m,
                                                      Insert (ys !! m) : table ! n ! (m+1),
                                                      Change (ys !! m) : table ! (n+1) ! (m+1)]

