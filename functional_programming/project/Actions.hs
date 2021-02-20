module Actions where
import Datatypes
import Display
import Sorting
import System.IO
import Data.Time -- TODO: NEED THIS LIBRARY?
import Data.Time.LocalTime

-- Display the contents of the 'saveFile'
present saveFile = do
    events <- readData saveFile
    mapM_ display (eventMergeSort events)
    return ()

-- Take user input to create a new event, and add it to the 'saveFile'
addItem saveFile = 
  do
    putStr "date: "
    date <- getLine
    putStr "time: "
    time <- getLine
    putStr "name: "
    name <- getLine
    putStr "loc: "
    loc <- getLine
    putStr "recur: "
    recur <- getLine
    appendFile saveFile ((eventToString (Event date time name loc recur)) ++ "\n")

add_item events = 
  do
    putStr "date: "
    date <- getLine
    putStr "time: "
    time <- getLine
    putStr "name: "
    name <- getLine
    putStr "loc: "
    loc <- getLine
    putStr "recur: "
    recur <- getLine
    let events = (events ++ [(Event date time name loc recur)])
    return ()

pairToDateString (x,y) = show x ++ "/" ++ show y

{--
--compareDays :: [Int] -> [Int] -> [Int]
compareDays (e1,e2)
  | (e1 !! 1) == (e2 !! 1) = compareHours (e1,e2)
  | otherwise              = (e1 !! 1) < (e2 !! 1)

parseDate :: [Char] -> [Int]
parseDate x =
  map stringToInt parts
  where parts = splitOn "/" x

parseTime :: [Char] -> [Int]
parseTime x =
  map stringToInt parts
  where parts = splitOn ":" x

stringToInt x = read x :: Int
--}

getCurrentDate = fmap (toGregorian . localDay . zonedTimeToLocalTime) getZonedTime
                  


dateBefore :: Event -> (Int,Int) -> Bool
dateBefore event (b,c) = monthDayCompare (parseDate (date event)) (b,c)

monthDayCompare [m1,d1] (m2,d2)
    | m1 == m2 = d1 >= d2
    | otherwise = m1 > m2 
    
futureEvents (a,b,c) [] = []
futureEvents (a,b,c) (e:events) 
    | e `dateBefore` (b,c) = e:(futureEvents (a,b,c) events)
    | otherwise = futureEvents (a,b,c) events


-- Display only the contents of 'saveFile' that occur today or in the future
-- ie. Don't display old events
present_upcoming saveFile = do
    events <- readData saveFile
    currDate <- getCurrentDate
    mapM_ display (futureEvents currDate events)


