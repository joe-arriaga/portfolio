module Display where 
import Datatypes
import System.IO
import Data.List.Split (splitOn)

-- Constructs an Event from a list of its fields (and wraps it in a list)
makeEvent :: [String] -> [Event]
makeEvent (date:time:name:loc:recur:[]) = [Event date time name loc recur]
makeEvent _ = []

{-- Takes contents of file, reads it in line by line
    and returns a list of events --}
readData file = do
        contents <- readFile file
        let events = lines contents
        return $ concatMap makeEvent $ map parseData events

parseData = splitOn " , " 

example = "my , name , is , bob"
event1 = Event "5/27" "my event" "12:00" "Fun House" "Once"

-- Converts an Event to its String representation
eventToString :: Event -> String
eventToString e = ((id date e) ++ " , "
                  ++ (id time e) ++ " , "
                  ++ (id name e) ++ " , "
                  ++ (id loc e)  ++ " , "
                  ++ (id recur e))

-- Displays a formatted representation of an Event
display :: Event -> IO ()
display e = do
            putStr ((pad 9 (id date e))
                 ++ (pad 17 (id time e))
                 ++ (pad 54 (id name e))
                 ++ (pad 34 (id loc e))
                 ++ (id recur e) ++ "\n")

test1 = Event "Test Event #1" "5/22/2018" "12:00" "Mars" "Weekly"
sample1 = putStr "12345678"

-- Adds the appropriate number of spaces after 'text' so that the field becomes
-- 'width' characters wide. Used to create fixed-width columns
pad :: Int -> [Char] -> [Char]
pad width text = text ++ spaces
  where space = (width - (length text))
        spaces = concat (replicate space " ")
