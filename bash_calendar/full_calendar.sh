#!/bin/bash
### full_calendar.sh
### Joe Arriaga
### Updated September 26, 2018

# NOTE: This program is still pretty buggy. If a certain combination of format
#       and date range doesn't work, just try a different combination. you can
#       also try one of the previous versions. \_(*_*)_/ Sorry, good luck.

#***** COMPLETED ******
#******* PLAN *********
#x 1) Take date range from command line
#x 2) Find beginning date (most recent Sunday)
#x	- Set beginning date as zero-date
#x 3) Increment from zero-date to fill all places in calendar
#x 4) Move to next month
#x	- Reset zero-date to first Sunday of next month???
#x	- Or could just continue to increment
#x 5) Output to file
#	- if 1st of month is Fri or Sat, start on next Sunday
#		- otherwise start on previous Sunday
#deprecated:	- replace dummy characters in template with appropriate dates
# 6) Print to printer???

#TODO: Decide which week should start a month; see Dec. 2018
#TODO: Condensed week formats (3,5) don't work




#### Debugging utility function
pause ()
{
	read -p "Continue? " response
	if [ $response == "y" ]; then : #do nothing
	else exit
	fi
}

#### Usage
selectFormat()
{
	#echo "Enter the starting month and optional year, then the ending month and optional year"
	#echo
	#echo "USAGE:    ./calendar.sh [-m|-w|-W] Mon [YY] Mon [YY] "
	#echo "USAGE:    ./calendar.sh Mon [YY] Mon [YY] "
	#echo
  echo "Please select a format:"
  echo " 1 - Month only"
  echo " 2 - Expanded Week only (1 week per page)"
  echo " 3 - Condensed Week only (2 weeks per page)"
  echo " 4 - Month and Expanded Week"
  echo " 5 - Month and Condensed Week"
  read format_selection
	echo
	echo "To print enter:"
	#echo 'lpr -o orientation-requested=4 -P $printer cal_output.txt'
	echo 'lpr -o landscape -o sides=one-sided -P $printer cal_output.txt'
    echo
}

#### Initialize workspace
initializer()
{
	if [ -e cal_output.txt ]; then
		rm cal_output.txt
	fi

#echo "# of arguments = $#"
  #### Check number of arguments
	if [[ $# -ne 2 && $# -ne 4 ]]; then # insufficient arguments provided
		echo
		echo "ERROR: invalid number of arguments"
    echo "Enter the starting month and optional year, then the ending month and optional year"
    echo
    echo "USAGE:    ./calendar.sh MMM [YY] MMM [YY] "
    echo
		exit 1
	fi
	
}

#### Process date parameters from command line
#### Requires that command line arguments be passed when this function in called
# For a better way to handle command line options and arguments see:
# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash
#shift #translates all arguements down one place --> and 'deletes' input args
getArgs()
{
#echo
#echo "Inside getArgs() before shift:"
#echo "# of arguments = $#"
#echo "\$0 = ${0}"
#echo "\$1 = ${1}"
#echo "\$2 = ${2}"
#echo "\$3 = ${3}"
#echo "\$4 = ${4}"
#echo "\$5 = ${5}"

  print_months=true
  print_weeks_expanded=false
  print_weeks_condensed=false
  
  if [ "$format_selection" == 1 ]; then
    : # no change to variables needed
  elif [ "$format_selection" == 2 ]; then
    print_months=false
    print_weeks_expanded=true
  elif [ "$format_selection" == 3 ]; then
    print_months=false
    print_weeks_condensed=true
  elif [ "$format_selection" == 4 ]; then
    # print_months = true
    print_weeks_expanded=true
  elif [ "$format_selection" == 5 ]; then
    # print_months = true
    print_weeks_condensed=true
  else
    echo "ERROR in getArgs() - invalid format specified, please enter a number in the range 1-5 when selecting the format"
    exit
  fi

	############## Process arguments #################
  ### Fill in the year if those arguments have been omitted
#  args=$#
#echo
#echo "Inside getArgs() after shift:"
#echo "# of arguments = $#"
#echo "\$0 = ${0}"
#echo "\$1 = ${1}"
#echo "\$2 = ${2}"
#echo "\$3 = ${3}"
#echo "\$4 = ${4}"
#echo "\$5 = ${5}"
#echo "first = $1"

	# Check if any arguments are provided
  #if (( $# == 0 )) # no arguments provided

	### Only months provided
  if [ $# == 2 ]; then
    start_month=$1
    start_year=$(date +%y)
    end_month=$2
    ### if end_month is before start_month, increment year
    #if (( $(date --date="$1 1 $start_year" +m) > $(date --date="$2 1 $start_year" +m) )); then
    if [ $(date --date="$start_month 1 $start_year" +%m) -gt $(date --date="$end_month 1 $start_year" +%m) ]; then
      end_year=$(echo "$start_year + 1" | bc)
    else
      end_year=$start_year
    fi
	
	### Months and years provided
	elif [ $# == 4 ]; then
    start_month=$1
    start_year=$2
    end_month=$3
    end_year=$4
	
  ### nonstandard usage, exit script
  else
		echo
		echo "ERROR: invalid number of arguments"
		echo "Please conform to one of the standard usages"
		exit 1
	fi
}

#### Transform command-line arguments to usable forms
transformArgs ()
{
		start_month_num=$(date --date="$start_month 1" +%m)
		start_day_str=$(date --date="$start_month 1" +%a)
		start_year_num=$start_year
		start_date=$(date --date="$start_month_num/1/$start_year_num")

		end_month_num=$(date --date="$end_month 1 + 1 month - 1 day" +%m)
		end_day_str=$(date --date="$end_month 1 + 1 month - 1 day" +%a)
		end_year_num=$end_year
		end_date=$(date --date="$end_month_num/1/$end_year_num + 1 month - 1 day")
}

#### Debugging utility routine
#### Sanity check for variable values
checkVariables ()
{
	echo
	echo "=========== Variable Values ==========="
	echo "______ getArgs ()_______"
	echo "start_month = $start_month"
	echo "start_year = $start_year"
	echo "end_month = $end_month"
	echo "end_year = $end_year"
	echo 
	echo "______ transformArgs ()_____"
	echo "start_month_num = $start_month_num"
	echo "start_day_str = $start_day_str"
	echo "start_year_num = $start_year_num"
	echo "start_date = $start_date"
	echo
	echo "end_month_num = $end_month_num"
	echo "end_day_str = $end_day_str"
	echo "end_year_num = $end_year_num"
	echo "end_date = $end_date"
	echo
	echo "______ setStartDate ()______"
	echo "cal_start_date = $cal_start_date"
	echo
	echo "______ setEndDate ()______"
	echo "cal_end_date = $cal_end_date"
	echo "======================================="
}

#### Set the starting day for the calendar
#### ie. The first Sunday from the start of the month
#### Get starting date of previous Sunday
#### Takes an integer argument specifying the month to start in
setStartDate ()
{
	#temp=$start_date
	if [ $# -eq 1 ]; then
		temp=$(date --date="$1/1/$iteration_year")
	else
		echo "ERROR: function setStartDate() provided invalid argument"
	fi

	### while day != Sunday
	while [ $(date --date="$temp" +%u) -ne 7 ]; do
		#echo $(date --date="$temp" +%u)
		temp=$(date --date="$temp - 1 day")
	done
	
	cal_start_date=$(date --date="$temp" +%F)
	#cal_start_date=$(date --date="$start_month_num/1/$start_year_num - $offset days")
}

#### Set the ending day for the calendar
#### ie. The last Saturday from the end of the month
#### Get ending date of last Saturday
#### Takes an integer argument specifying the month to start in
setEndDate ()
{
	#temp=$end_date
	if [ $# -e 1 ]; then
		#temp=$start_date
		temp=$(date --date="$1/1/$iteration_year + 1 month - 1 day")
	else
		echo "ERROR: function setEndDate() provided invalid argument"
	fi
	### while day != Sunday
	while [ $(date --date="$temp" +%u) -ne 6 ]; do
		temp=$(date --date="$temp + 1 day")
	done
	
	cal_end_date=$(date --date="$temp" +%F)
	#cal_end_date=$(date --date="$end_month_num/1/$end_year_num - $offset days")
}

#### Constructs the file to be printed, substituting the correct dates
#### Takes an integer argument for the month to construct
constructMonth ()
{
	setStartDate $1
	#temp_date=$(date --date="$cal_start_date" - 1 day)
	temp_date=$cal_start_date

	#temp_day=$(date --date="$cal_start_date" +%d)
	#temp_month=$(date --date="$cal_start_date" +%m)
	#temp_year=$(date --date="$cal_start_date" +%Y)
	#temp_date=$(date --date="$1/1/18")

#echo "argument = $1"
#echo "temp_date = $temp_date"
#echo

	#### Calendar Heading
	echo -n "|                                                                                     " >> cal_output.txt
	echo -n "$(date --date="$1/1/$iteration_year" "+%_8B  %Y")" >> cal_output.txt
	#echo "           |" >> cal_output.txt
	echo "     |" >> cal_output.txt
	echo "==========================================================================================================" >> cal_output.txt
	echo "|    Sunday    |    Monday    |    Tuesday   |   Wednesday  |   Thursday   |    Friday    |   Saturday   |" >> cal_output.txt
	echo "==========================================================================================================" >> cal_output.txt

	#### Calendar weeks
	for week in $(seq 1 5); do #prints each week
		#### Calendar date boxes
		echo -n "|" >> cal_output.txt #begins each line
		for day in $(seq 1 7); do #prints the first line of a week
			if [ $(date --date="$temp_date" +%m) -ne $1 ]; then #determines if date is part of this month or another month
				echo -n "        $(date --date="$temp_date" "+%b %e")|" >> cal_output.txt	#if part of another month, prepend month abbreviation
			else	
				echo -n "            $(date --date="$temp_date" +%e)|" >> cal_output.txt #otherwise, just print date
			fi
			#### increment $temp_date
			check_date=$temp_date
			temp_date=$(date --date="$temp_date + 1 day")
			### adding one day in $(date) command can be buggy, need to check result
			### to make sure day incremented correctly
			if [ $(date --date="$temp_date" +%d) -eq $(date --date="$check_date" +%d) ]; then
				temp_date=$(date --date="$temp_date + 1 day")
			fi
#echo "temp_date = $temp_date"
		done #end first line of week
		echo "" >> cal_output.txt #move to next line
		
		for day in $(seq 1 7); do #prints the other 7 lines of a week
			echo "|              |              |              |              |              |              |              |" >> cal_output.txt
		done
		echo "==========================================================================================================" >> cal_output.txt
	done #end week
}
			#### increment $temp_date
			check_date=$temp_date
			temp_date=$(date --date="$temp_date + 1 day")
			### adding one day in $(date) command can be buggy, need to check result
			### to make sure day incremented correctly
			if [ $(date --date="$temp_date" +%d) -eq $(date --date="$check_date" +%d) ]; then
				temp_date=$(date --date="$temp_date + 1 day")
			fi


constructWeeks ()
{
	week_start=$(date --date="$iteration_date")
	week_stop_month=$(( ($iteration_month % 12) + 1 ))
  condensed_count=0

  if [ "$1" == "none" ]; then #don't print weeks
    exit 0 #a format without weeks was selected
  elif [ "$1" == "expanded" ]; then #print expanded weeks, 1 week per page
    ### output all weeks that start (with Monday) before next month
    while [ $(date --date="$week_start" +%m) -ne $week_stop_month ]; do
    #for i in $(seq 1 5); do
      ### Set start date to first Monday after 1st of month
      while [ $(date --date="$week_start" +%u) -ne 1 ]; do
        week_start=$(date --date="$week_start + 1 day")
      done
      week_start_day=$(date --date="$week_start" +%-d)
      current_month=$(date --date="$week_start" +%m)
      current_year=$(date --date="$week_start" +%Y)

      mon=$(date --date="$week_start" +%-m/%-d)
      tue=$(date --date="$mon + 1 day" +%-m/%-d)
      wed=$(date --date="$mon + 2 day" +%-m/%-d)
      thu=$(date --date="$mon + 3 day" +%-m/%-d)
      fri=$(date --date="$mon + 4 day" +%-m/%-d)
      sat=$(date --date="$mon + 5 day" +%-m/%-d)
      sun=$(date --date="$mon + 6 day" +%-m/%-d)
      ### increment week_start
      week_start=$(date --date="$week_start + 1 week")

      awk -v mon="$mon" -v tue="$tue" -v wed="$wed" -v thu="$thu" -v fri="$fri" -v sat="$sat" -v sun="$sun" '{
        #format1 = ||  day  num ||   day  num  ||
        format1 = "%2s %25s %6s %18s %26s %6s %17s\n"
        
        #format2 = ||  Wed  num  ||  Sat  num  |  Sun  num  ||
        format2 = "%2s %25s %6s %18s %14s %6s %3s %12s %6s %5s\n"

        filename = "cal_output.txt"

        if ($2 == "Monday")
        {
          printf format1, "||", "Monday", mon, "||", "Thursday", thu, "||" >> filename
        }
        else if ($2 == "Tuesday")
        {
          printf format1, "||", "Tuesday", tue, "||", "Friday", fri, "||" >> filename
        }
        else if ($2 == "Wednesday")
        {
          printf format2, "||", "Wednesday", wed, "||", "Saturday", sat, "|", "Sunday", sun, "||" >> filename
        }
        else
          print $0 >> filename
      }' expanded_week.txtt
    done
  elif [ "$1" == "condensed" ]; then #print condensed weeks, 2 weeks per page
    ### Set start date to first Monday before 1st of month
    while [ $(date --date="$week_start" +%a) != "Mon" ]; do
      week_start=$(date --date="$week_start - 1 day")
    done
    while [ "$condensed_count" -le 2 ]; do
      m1=$(date --date="$week_start" +%-m/%-d)
      s1=$(date --date="$m1 + 6 day" +%-m/%-d)
      m2=$(date --date="$m1 + 7 day" +%-m/%-d)
      s2=$(date --date="$m1 + 13 day" +%-m/%-d)

#echo "m1 = $m1"
#echo "con_count = $condensed_count"
#if [ "$condensed_count" -le 2 ]; then 
#  echo "con <= 2"
#fi

      ### increment week_start
      week_start=$(date --date="$week_start + 2 week")
      condensed_count+=1

      awk -v mon1="$m1" -v sun1="$s1" -v mon2="$m2" -v sun2="$s2" '{
        #header = ||  mon1 -   sun1 ||  mon2 -   sun2 ||
        header = "%2s %23s %1s %5s  %18s %23s %1s %5s  %18s\n"
        filename = "cal_output.txt"

        if ($2 == "XX/XX")
        {
          printf header, "||", mon1, "-", sun1, "||", mon2, "-", sun2, "||" >> filename
        }
        else
          print $0 >> filename
      }' condensed_week.txtt
    done
  else
    echo "ERROR inside constructWeeks() - format could not be matched"
    exit
  fi
}

#### calls constructMonth() and constructWeeks() functions to create the requested calendar
constructionManager ()
{
	iteration_year=$start_year
	iteration_month=$start_month_num
	iteration_date=$(date --date="$iteration_month/1/$iteration_year") # first of the current month

	#while [ $(date --date="$iteration_date" +%m) -le $end_month_num ]; do
	while [ $(date --date="$iteration_date" +%s) -le $(date --date="$end_date" +%s) ]; do

		if [ "$print_months" == true ]; then
			constructMonth $iteration_month
		fi

		#if [ "$print_weeks" == true ]; then
    #if [ "$print_weeks_expanded" == true ]; then
    #  echo ex = false
    #fi
    #if [ "$print_weeks_condesed" == true ]; then
    #if [ "$print_weeks_expanded" == true ] || [ "$print_weeks_condesed" == true ]; then
    #if [[ "$print_weeks_expanded" == true || "$print_weeks_condesed" == true ]]; then
    
    if [[ "$print_weeks_expanded" == false && "$print_weeks_condensed" == false ]]; then
      week_format="none"
    elif [ "$print_weeks_expanded" == true ]; then
      week_format="expanded"
    elif [ "$print_weeks_condensed" == true ]; then
      week_format="condensed"
    else 
      echo "ERROR: constructionManager() could not call constructWeeks() - week format not specified"
      exit
    fi
    constructWeeks $week_format
    #fi

		#### Increment $iteration_date to next month
		if [ $iteration_month -eq 12 ]; then
			iteration_month=1
			iteration_year=$(( $iteration_year + 1 ))
		else
			iteration_month=$(( $iteration_month + 1 ))
		fi
		iteration_date=$(date --date="$iteration_month/1/$iteration_year")
	done
}


#### MAIN
initializer $1 $2 $3 $4
selectFormat
getArgs $1 $2 $3 $4
transformArgs
constructionManager

#checkVariables

