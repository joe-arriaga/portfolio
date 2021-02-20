module Sorting where
import Datatypes
import Display
import Data.List
import Data.List.Split (splitOn)
-------------------------- TEST OBJECTS ---------------------------------
testDates = ["5/23","4/21","4/16","5/5","6/31","7/27","7/4"]
date1 = "5/5"
date2 = "5/31"
date3 = "5/3"
date4 = "1/21"
date5 = "12/1"


testSort = do 
  events <- readData "events.txt"
  let sorted = eventMergeSort events
  print sorted

------------------------ END TEST OBJECTS -------------------------------
--date , time  , name                         , loc               , recur
testEvent1 = Event "5/23" "12:00" "Pickup my cap and gown order" "University Market" "Once"
testEvent2 = Event "5/24" "14:00" "Meet with Barbara about electives" "FAB-120" "Once"
testEvent3 = Event "6/2" "8:00-9:15" "Dentist appointment" "123 Main Street" "Once"
testEvent4 = Event "6/6" "12:00" "yo" "here" "Once"


eventMergeSort lst
  | length(lst) < 2 = lst
  | otherwise       = eventMerge (eventMergeSort (firstHalf lst)) (eventMergeSort (secondHalf lst))
  where firstHalf lst  = take (length(lst) `div` 2) lst
        secondHalf lst = drop (length(lst) `div` 2) lst

eventMerge []     []     = []
eventMerge xs     []     = xs
eventMerge []     ys     = ys
eventMerge (x:xs) (y:ys)
  | (x `eventBefore` y) = x:(eventMerge xs (y:ys))
  | otherwise      = y:(eventMerge (x:xs) ys)

eventBefore e1 e2 = compareEvents e1 e2

compareEvents e1 e2 = compareMonths (parseDateAndTime e1, parseDateAndTime e2)

compareMonths (e1,e2)
  | (e1 !! 0) == (e2 !! 0) = compareDays (e1,e2)
  | otherwise              = (e1 !! 0) < (e2 !! 0)  -- Does e1 come before e2 (T/F)?

--compareDays :: [Int] -> [Int] -> [Int]
compareDays (e1,e2)
  | (e1 !! 1) == (e2 !! 1) = compareHours (e1,e2)
  | otherwise              = (e1 !! 1) < (e2 !! 1)

compareHours (e1,e2)
  | (e1 !! 2) == (e2 !! 2)  = compareMinutes (e1,e2)
  | otherwise               = (e1 !! 2) < (e2 !! 2)

--compareMinutes :: [Int] -> [Int] -> [Int]
compareMinutes (e1,e2) = (e1 !! 3) <= (e2 !! 3)

parseDateAndTime :: Event -> [Int]
parseDateAndTime (Event d t n l r) = (parseDate d) ++ (parseTime t)

parseDate :: [Char] -> [Int]
parseDate x =
  map stringToInt parts
  where parts = splitOn "/" x

parseTime :: [Char] -> [Int]
parseTime x =
  map stringToInt parts
  where parts = splitOn ":" x

stringToInt x = read x :: Int

