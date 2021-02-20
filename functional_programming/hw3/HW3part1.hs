{-  YOUR NAME: Joe Arriaga

----------------------------------------------------------------------
CS457/557 Functional Languages, Spring 2018                 Homework 3
----------------------------------------------------------------------

-}

module HW3 where
       
{- 
----------------------------------------------------------------------
For Credit Exercises:  Your solutions to the following questions are
due by email to cs457acc@pdx.edu at the start of class (2pm) on April 25.

Mailing instructions: Your mail should have the subject line "HW3".
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
Question 1:
-----------

Recall the definition of binary search trees from lecture,
reproduced here with a slightly more general type. 

-}

data Tree a = Leaf
            | Fork (Tree a) a (Tree a)
  deriving (Show,Eq)


testTreeInt = Fork 
  (Fork Leaf 2 Leaf) 
  3 
  (Fork 
      (Fork Leaf 4 Leaf)
      5
      (Fork Leaf 6 Leaf))

       
foldT                        :: t -> (t -> a -> t -> t) -> Tree a -> t
foldT leaf fork Leaf          = leaf
foldT leaf fork (Fork l n r)  = fork (foldT leaf fork l) n (foldT leaf fork r)

sumT    :: Num a => Tree a -> a
sumT    = foldT 0 (\l n r-> l + n + r)

heightT  :: Tree a -> Int
heightT = foldT 0 (\l _ r -> max l r + 1) 

{- 

Our intent is to maintain the _binary search tree_ (BST)
property on all our Trees, namely:
a given value appears at most once in the tree, and
for any node (Fork l n r),  all values in subtree l are < n
and all values in subtree r are > n. 

Note that the definition of Tree does not by itself
enforce the BST property, but any instance
of Tree built from a single Leaf by repeated use
of insertT will have the BST property.  The lookupT
function relies on the BST property holding.

-}


insertT :: Ord a => a -> Tree a -> Tree a       
insertT x Leaf = Fork Leaf x Leaf
insertT x t@(Fork l y r) | x < y = Fork (insertT x l) y r       
                         | x > y = Fork l y (insertT x r)
                         | otherwise = t

lookupT :: Ord a => a -> Tree a -> Bool
lookupT x Leaf = False
lookupT x (Fork l y r) | x < y = lookupT x l
                       | x > y = lookupT x r
                       | otherwise = True       

{- 
(a) Write a function fromListT that creates a search tree containing
the elements of a list.  Use the foldr function on lists.

-}

fromListT :: Ord a => [a] -> Tree a
fromListT []     = Leaf
fromListT (x:xs) = foldr (insertT) Leaf xs

{- 

(b) Write a function inorderT that returns a list of the values of the
tree in in-order.  (If the tree has the search tree property, the
resulting list will be sorted.)  Try to use the foldT function.

-}

inorderT :: Tree a -> [a]
inorderT Leaf         = []
inorderT (Fork l n r) = (inorderT l) ++ n:(inorderT r)

inorderT' :: Tree a -> [a]
inorderT' Leaf         = []
--inorderT' (Fork l n r) = foldT Leaf Fork (Fork l n r)
inorderT' t = foldT [] f t
                where f l n r = l ++ [n] ++ r

{-

(c) Show how to combine the functions from parts (a) and (b) to obtain
a sorting function on lists.

-}

treeSort :: Ord a => [a] -> [a]
treeSort xs = inorderT (fromListT xs)


{-

(d) Write a function mapT, analagous to map over lists, that applies a
specified function to each value in the tree, obtaining a new tree
with the same shape. Try to use the foldT function.

-}

mapT :: (a -> b) -> Tree a -> Tree b
mapT _ Leaf           = Leaf
mapT f (Fork l n r) = Fork (mapT f l) (f n) (mapT f r)

--mapT' Leaf = 
--mapT' f 

--TODO: foldT
{- 

(e) Write a function labelDepthsT that replaces each value v in the
tree with a pair (d,v), where d is the depth of the Fork (and the root
has depth 0).  For example, applying this function to the tree

-} 

ex1 = 
 Fork 
  (Fork Leaf 'a' Leaf) 
  'b' 
  (Fork 
      (Fork Leaf 'c' Leaf)
      'd'
      (Fork Leaf 'e' Leaf))

{-

should produce the tree

Fork 
  (Fork Leaf (1,'a') Leaf) 
  (0,'b') 
  (Fork 
      (Fork Leaf (2,'c') Leaf)
      (1,'d')
      (Fork Leaf (2,'e') Leaf))

Hint: Use a local auxiliary function that takes the current depth as
an accumulating parameter.

Extra credit challenge: Write this function using foldT! 

-}

labelDepthsT :: Tree a -> Tree (Int,a)
labelDepthsT (Fork Leaf n Leaf)        = Fork Leaf (0,n) Leaf
labelDepthsT (Fork l n r) = trackDepthsT (Fork l n r)
{- 
-- Pass current depth
trackDepthsT :: Tree a -> Tree (Int,a)
trackDepthsT (Fork Leaf n Leaf)        = Fork Leaf (-99,n) Leaf
trackDepthsT (Fork l n r) = Fork (calcDepthsT 0 l) (0,n) (calcDepthsT 0 r)

calcDepthsT :: Int -> Tree a -> Tree (Int, a)
calcDepthsT acc (Fork Leaf n Leaf)        = Fork Leaf (acc+1,n) Leaf
calcDepthsT acc (Fork l n r) = Fork (calcDepthsT (acc+1) l) (acc+1,n) (calcDepthsT (acc+1) r)
-}

-- Pass depth of next lowest level
trackDepthsT :: Tree a -> Tree (Int,a)
trackDepthsT (Fork Leaf n Leaf) = Fork Leaf (-99,n) Leaf
trackDepthsT (Fork l n r)       = Fork (calcDepthsT 1 l) (0,n) (calcDepthsT 1 r)

calcDepthsT :: Int -> Tree a -> Tree (Int, a)
calcDepthsT acc (Fork Leaf n Leaf) = Fork Leaf (acc,n) Leaf
calcDepthsT acc (Fork l n r)       = Fork (calcDepthsT (acc+1) l) (acc,n) (calcDepthsT (acc+1) r)

--EC
--labelDepthsT (Fork l n r) = foldT 0 trackDepthT (Fork l n r)

{-

Once you've defined mapT and labelDepthsT, the following function
should work; it is useful for displaying trees in a "sideways" manner
in ghci, if you apply the putStr library function on the resulting
String.

-}

showT :: Show a => Tree a -> String
showT  = unlines
          .  inorderT
          .  mapT indent
          .  labelDepthsT  
  where indent (d,x) = replicate (2*d) ' ' ++ (show x)


{-   

(f) Write a function deleteT that deletes a value from a Tree,
while preserving the BST property.

-}

deleteT :: Ord a => a -> Tree a -> Tree a
deleteT = error "fill in here"

{- 

Probably the easiest way to do this is to write an auxiliary function

splitOutMaxT :: Ord a => Tree a -> (Tree a,a)

that finds the maximum (i.e. rightmost) value of a (non-empty) BST and
returns it, paired with the remainder of the tree without the
rightmost value.

For example, applying splitOutMaxT to the example tree
ex1 given above should return

(Fork 
  (Fork Leaf 'a' Leaf) 
  'b' 
  (Fork 
      (Fork Leaf 'c' Leaf)
      'd'
      Leaf),
 'e')

Note: we could just as well define the dual function
splitOutMinT, but we don't need both.

-} 

splitOutMaxT :: Ord a => Tree a -> (Tree a,a)
splitOutMaxT = error "fill in here"

{-
----------------------------------------------------------------------
Question 2 (Thompson):
---------------------

Consider the problem of finding the _edit distance_ between
two strings. Given two strings and a fixed set of editing operations,
we ask what is the cheapest sequence of operations that converts
one string to the other.

For this problem, we'll suppose that we have these operations:

- change one character to another
- copy a character without changing it
- delete a character
- insert a character
- kill all characters to the end of the string

and we'll suppose that all operations have the same cost (1)
except copy, which is free.

Then, for example, we can get from the string "fish" to the string "chips"
by the following sequence of operations

"fish" 
 ^ [insert 'c']
"cfish"
  ^ [change 'f' to 'h']
"chish"
   ^ [copy 'i']
"chish"
    ^ [insert 'p']
"chipsh"
     ^ [copy 's']
"chipsh"
      ^ [delete 'h']
"chips"

with total cost 4, and this cost is in fact optimal.

To model this problem in Haskell, we start by
defining an algebraic data type for edit operations:

-}

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

--transform :: String -> String -> [Edit] 
--transform x:xs y:ys = 

{- If x is in the word, insert before it
-}

{- Note that this problem is normally solved using dynamic programming, 
We're not asking for a dynamic programming solution here --- exponential
running time is OK.  But you are welcome to investigate how to code 
up dynamic programming in Haskell if you're interested! Hint: it's all
about laziness! -}

