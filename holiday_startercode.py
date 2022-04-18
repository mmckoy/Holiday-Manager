import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from datetime import datetime


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday: #class Age(object): takes in the name and date
      
    def __init__(self,name, date):
        self.name = name #int
        self.date = date #str      
    
    def __str__ (self):
        return f"{self.name} {self.date}" #f'string is formating, {variable inside}
#add from dataclasses import dataclass, field on top
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
       self.innerHolidays = []
   
    def addHoliday(self, holidayObj): # self is added to all dataclass it references class
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        assert isinstance(holidayObj, Holiday) # assert isinstance() to check if obj is instance of class, true/false
        self.innerHolidays.append(holidayObj) #append()adds a single item to the existing list
        print("successfully added holiday")

    def findHoliday(self, HolidayName, Date,):
        # Find Holiday in innerHolidays
        # Return Holiday
        try: #try the code
            holiday = next(filter(lambda hd: hd.name == HolidayName and hd.date == Date, self.innerHolidays)) #lambda shortens long functions without a name, filter list by name and date in holidays--> returns a generator obj, 
        except StopIteration:# if it fails with no match, then return (none=fail or holiday=success)
            return None
        return holiday #== is boolean



    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        #holiday = Holiday(HolidayName, Date)
        holiday = self.findHoliday(HolidayName, Date) #definding holiday
        if holiday:
            self.innerHolidays.remove(holiday) #Removing Values from Lists with remove()
            print("holiday is removed")
        else:
            print("holiday does not exist") 

    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        with open(filelocation)as f: #reading file
            self.innerHolidays = [Holiday(h["name"], datetime.fromisoformat(h["date"])) for h in json.load(f)] # convert DateTime value into ISO format, A nested list is a list of lists[([])]


    def save_to_json(self,filelocation):
        # Write out json file to selected file.
        with open(filelocation,"w")as f: #w for write
            json.dump([{"name": h.name, "date": h.date.strftime("%Y-%m-%d")} for h in self.innerHolidays] #json.dumps(nested list), convert date and time objects to their string representation
,f)
        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions. 
        url= "https://www.timeanddate.com/holidays/us/{year}"
        current_year = 2022
        for year in range(current_year-2, current_year+3):   
            html = requests.get(url.format(year = year)).text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find("table", id="holidays-table")
            for row in table.tbody.find_all('tr'):
                columns = row.find_all(["td", "th"])
                if not columns:
                    continue
                date = columns[0].text.strip()
                name = columns[2].text.strip()
                #print(date)
                date = datetime.strptime(str(year) + " " + date, "%Y %b %d")
                #print(date)
                #date= date.strftime("%Y-%m-%d")
                #print(date)
                holiday = Holiday(name, date)
                if holiday not in self.innerHolidays:
                    self.innerHolidays.append(holiday)


    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)

    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        return filter(lambda hd: hd.date.year == year and hd.date.isocalendar().week == week_number, self.innerHolidays) #lambda shortens long functions without a name, filter list by name and date in holidays--> returns a generator obj, 

    def displayHolidaysInWeek(self, holidayList, see_weather=False):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        for holiday in holidayList:
            if see_weather:
                print(holiday, "-", self.getWeather(holiday.date.isocalendar().week))
            else:
                print(holiday)

    def getWeather(self, weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        url = "http://history.openweathermap.org/data/2.5/history/city"

        querystring = {"lat":"37.774929","lon":"-122.419418","type":"hour", "start":"1369728000"
, "end": "1369789200", "appid": "209678d41dbbee2048ebd5d17ffe70bc"} #copied from site, changed dt, time

        headers = {
            #"X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            #"X-RapidAPI-Key": "2cb492fcb3mshc7b7ed453b2dec8p1ffc7djsn03533e30a16f"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response

    def viewCurrentWeek(self): #self=class/obj
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        dt = datetime.now() # means you are assigning current day time
        year =dt.date.year
        week = dt.isocalender().week
        holidays = self.filter_holidays_by_week(year,week)
        self.displayHolidaysInWeek(holidays)
        while True:
            inp = input("Would you like to see the weather?")
            if inp == 'yes':
                weather = self.getWeather(week) #apart of obj, API
                print(weather)
                break
            elif inp == 'no':
                break
            print(" Valid options is yes or no.")





def main():
    #hl = HolidayList()
    #hl. getWeather()
    #hl.scrapeHolidays()
    #hl.save_to_json("holiday.json")
    #print(hl.innerHolidays)

    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object 
    hl = HolidayList()
    # 2. Load JSON file via HolidayList read_json function
    hl.read_json("holiday.json")
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    hl.scrapeHolidays()
    print(f"""
Holiday Management
===================
There are {hl.numHolidays()} holidays stored in the system.
""")
    # 3. Create while loop for user to keep adding or working with the Calender
    while True:
    # 4. Display User Menu (Print the menu)
        print("""Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit""")
    # 5. Take user input for their action based on Menu and check the user input for errors
        inp = input("Enter Number")
        if inp == "1":
            print("Add a Holiday\n================")
            while True:
                name = input("Holiday: ")
                date = input("Date: ")
                try:
                    date = datetime.fromisoformat(date) 
                except ValueError:
                    print("Date not valid")
                else:
                    hl.addHoliday(Holiday(name, date))
                    print("Success:")
                    print(f"{name} ({date}) has been added to the holiday list")
                    break
        elif inp == '2':
            print("Remove a Holiday\n================")
            while True:
                name = input("Holiday: ")
                date = input("Date: ")
                try:
                    date = datetime.fromisoformat(date) 
                except ValueError:
                    print("Date not valid")
                else:
                    hl.removeHoliday(name, date)
                    print("Success:")
                    print(f"{name} ({date}) has been removed from the holiday list")
                    break
        elif inp == "3":
            print("Saving Holiday List\n================")
            while True:
                save = input("Are you sure you want to save your changes? [y/n]: ")
                if save == 'y':
                    hl.save_to_json("holiday.json")
                    print("Success:")
                    print("Your changes have been saved, choose n to exit")
                else:
                    print("Canceled:")
                    print("Holiday list file saved and canceled")
                    break
        elif inp == "4":
            hl.displayHolidaysInWeek
            while True:
                year = input("Which year?:")
                week = input("Which week?") #convert to int
                see_weather = input("Would you like to see this weeks weather? [y/n]: ")
                try:
                    year = int(year)
                    week = int(week) 
                except ValueError:
                    print("Week is not a number")
                else:
                    hl.displayHolidaysInWeek(hl.filter_holidays_by_week(year, week), see_weather)  
                    break
        elif inp == "5":
            with open("holiday.json") as f:
                if json.load(f) == hl.innerHolidays:
                    lost = "Your changes will be lost"
                else:
                    lost = ""
            exit_ = input("Are you sure you want to exit? [y/n]: " + lost)
            if exit_ == 'y':
                print("Goodbye!")
                break
        else:
            print("Enter a number between 1 and 5")

    # 6. Run appropriate method from the HolidayList object depending on what the user input is


    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





