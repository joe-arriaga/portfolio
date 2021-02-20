import Display
import Datatypes
import Actions
import System.IO
import Data.Char

testEvents = do 
  events <- readData "events.txt"
  print events

saveFile = "events.txt"

main =
  do
       putStrLn "\nTo execute a command enter the keyword given in square brackets. \nFor example, to display the calendar, type 'display all'"
       putStrLn "*****************************"
       putStrLn "* Menu:                     *"
       putStrLn "* [Display All] Events      *"
       putStrLn "* [Display Upcoming] Events *"
       putStrLn "* [Add] Event               *"
       putStrLn "* [Quit]                    *"
       putStrLn "*****************************"
       putStrLn "Type in your command: "
       command <- getLine >>= return . map toUpper


       if command == "DISPLAY ALL" then 
         do
            present saveFile
            main
       else if command == "DISPLAY UPCOMING" then
         do
            date <- present_upcoming saveFile
            --putStrLn "\nToday's Date:"
            --print ((\(x,y,z) -> (y,z)) date) 
            main
       else if command == "ADD" then
         do
            addItem "events.txt"
            main
       else if command == "QUIT" then
            putStrLn "\nGoodbye.\n"
       else
         do
              putStrLn "Please enter in a valid command!"
              main

