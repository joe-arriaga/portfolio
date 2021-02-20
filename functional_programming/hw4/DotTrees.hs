module DotTrees where

data BinTree a = Leaf a
               | BinTree a :^: BinTree a
                 deriving Show

example :: BinTree Int
example  = l :^: r
 where l = p :^: q
       r = s :^: t
       p = Leaf 1 :^: t
       q = s :^: Leaf 2
       s = Leaf 3 :^: Leaf 4
       t = Leaf 5 :^: Leaf 6

type Path      = [Int]
type NodeId  = String

showPath      :: Path -> NodeId
showPath p     = "\"" ++ show p ++ "\""

escQ :: String -> String
escQ = concatMap f
  where f '\"' = "\\\""
        f c    = [c] 


data LabTree l a = Tip a
                 | LFork l (LabTree l a) (LabTree l a)

data STree a     = Empty
                 | Split a (STree a) (STree a)

data RoseTree a  = Node a [RoseTree a]

data Expr        = Var String
                 | IntLit Int
                 | Plus Expr Expr
                 | Mult Expr Expr

class Tree t where
  subtrees :: t -> [t]

instance Tree (BinTree a) where
  subtrees (Leaf x)   = []
  subtrees (l :^: r)  = [l, r]

instance Tree (LabTree l a) where
  subtrees (Tip a)       = []
  subtrees (LFork s l r) = [l, r]

instance Tree (STree a) where
  subtrees Empty = []
  subtrees (Split s l r) = [l, r]

instance Tree (RoseTree a) where
  subtrees (Node x cs) = cs

instance Tree Expr where
  subtrees (Var s)    = []
  subtrees (IntLit n) = []
  subtrees (Plus l r) = [l, r]
  subtrees (Mult l r) = [l, r]

depth  :: Tree t => t -> Int
depth   = (1+) . foldl max 0 . map depth . subtrees

size   :: Tree t => t -> Int
size    = (1+) . sum . map size . subtrees

paths               :: Tree t => t -> [[t]]
paths t | null br    = [ [t] ]
        | otherwise  = [ t:p | b <- br, p <- paths b ]
          where br = subtrees t

dfs    :: Tree t => t -> [t]
dfs t   = t : concat (map dfs (subtrees t))

class Tree t => LabeledTree t where
   label :: t -> String

instance Show a => LabeledTree (BinTree a) where
  label (Leaf x)   = show x
  label (l :^: r)  = ""

instance (Show l,Show a) => LabeledTree (LabTree l a) where
  label (Tip a)       = show a
  label (LFork s l r) = show s

instance Show a => LabeledTree (STree a) where
  label Empty         = ""
  label (Split s l r) = show s

instance Show a => LabeledTree (RoseTree a) where
  label (Node x cs) = show x

instance LabeledTree Expr where
  label (Var s)    = s
  label (IntLit n) = show n
  label (Plus l r) = "+"
  label (Mult l r) = "*"

toDot :: LabeledTree t => String -> t -> IO ()
toDot s t = writeFile (s ++ ".dot")
           ("digraph tree {\n"
            ++ semi (nodeTree [] t) ++ "}\n")
 where semi = foldr (\l ls -> l ++ ";\n" ++ ls) ""

nodeTree    :: LabeledTree t => Path -> t -> [String]
nodeTree p t
  = [ showPath p ++ " [label=\"" ++ escQ(label t) ++ "\"]" ]
  ++ concat (zipWith (edgeTree p) [1..] (subtrees t))

edgeTree      :: LabeledTree t => Path -> Int -> t -> [String]
edgeTree p n c = [ showPath p ++ " -> " ++ showPath p' ]
               ++ nodeTree p' c
                 where p' = n : p

  