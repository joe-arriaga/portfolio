-- datatypes.hs
-- Definitions for Event abstract type and
-- Deadline, and Appointment concrete types

module Datatypes where
import Data.Text

data Event = Event {date  :: String,
              time  :: String,
              name  :: String,
              loc   :: String,
              recur :: String}
--data Deadline
--data Appointment

instance Show Event where
  show (Event date time name loc recur) 
    = "[" ++ show date ++ ","
      ++ show time ++ ","
      ++ show name ++ ","
      ++ show loc ++ ","
      ++ show recur ++ "]"

test1 = Event "Test Event #1" "5/22/2018" "12:00" "Mars" "Weekly"
     
