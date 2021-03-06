import os
import datetime
import csv
import re
import operator

"""
    Class engine
    This class handles the main program in program()
"""
class Engine:

    def __init__(self):
        self.options = {
            "a": "Add New Entry",
            "b": "Search in Existing Entries",
            "c": "Quit Program"
        }
        self.options_search = {
            "a": "Exact Date",
            "b": "Range of Dates",
            "c": "Exact Search",
            "d": "Regex Pattern",
            "e": "Return to Menu",
            "f": "Quit Program",
        }
        self.running = True
        self.error = ""
        self.option = ""
        self.option_search = ""
        self.option_result = ""
        self.task_date = ""
        self.search_date = ""
        self.exact_search = ""
        self.regex_pattern = ""
        self.range_date_low = ""
        self.range_date_high = ""
        self.task_title = ""
        self.task_time = 0
        self.task_notes = ""
        self.fieldnames = ["task_id", "task_date", "task_title", "task_time", "task_notes"]
        self.search_results = []
        self.entries = []
        self.get_entries()
        self.current_result = 0


    # Clears the Screen
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Shows Welcome Message
    def welcome_message(self):
        print("The Work Log!\nWhat would you like to do?\n")

    # Returns Ready User Input for Options
    def choose_option(self, message = ""):
        return raw_input("{} -> ".format(message)).lower()

    # Show Menu with options
    def show_menu(self, options, title=""):
        if title!="":
            print(title)
        sorted_menu = sorted(options.items(), key=operator.itemgetter(0))
        for key, value in sorted_menu:
            print("{}) {}".format(key, value))
        print("\n")

    # Checks for error and displays error if exists
    def check_error(self):
        if self.error != "":
            print(self.error)

    # Quits the program
    def quit(self):
        self.clear_screen()
        self.running = False

    # Validates Date
    def validate_date(self, date_text, date_format):
        try:
            datetime.datetime.strptime(date_text, date_format)
            return True
        except ValueError:
            self.error = "Incorrect data format, should be DD/MM/YYYY"
            self.task_date = ""
            self.search_date = ""
            return False

    # Validate Title Text
    def validate_text(self, text):
        if(text!=""):
            return True
        else:
            self.error = "Please Enter a Valid Title"
            self.task_title = ""
            return False

    # Validates Time Input
    def validate_time(self, time):
        try:
            val = int(time)
            return True
        except ValueError:
            self.error = "Please Enter a Valid Time in Minutes"
            self.task_time = 0
            return False

    # Validates a Regex Pattern
    def validate_regex(self, regex_pattern):
        try:
            re.compile(regex_pattern)
            return True
        except re.error:
            return False

    # Shorcut to clear screen and check errorss
    def refresh(self):
        self.clear_screen()
        self.check_error()

    # Adds entry to tasks.csv
    def add_entry(self, task_date, task_title, task_time, task_notes):
        self.get_entries()
        id_add = self.get_last_id() + 1
        with open("tasks.csv", "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow({
                "task_id": id_add,
                "task_date": task_date,
                "task_title": task_title,
                "task_time": task_time,
                "task_notes": task_notes
            })

    # Gets all the entries from tasks.csv
    def get_entries(self):
        with open("tasks.csv") as csvfile:
            artreader = csv.DictReader(csvfile)
            self.entries = list(artreader)

    # Gets the last task_id from created tasks for event handling
    def get_last_id(self):
        if len(self.entries):
            return int(self.entries[-1]["task_id"])
        else:
            return -1

    # Search Entries by Date
    def search_entries_by_date(self, date):
        self.search_results = []
        for row in self.entries:
            if row["task_date"] == date:
                self.search_results.append(row)

    # Validates exact search
    def validate_exact_search(self, exact_search):
        self.search_results = []
        for row in self.entries:
            if exact_search in row["task_title"] or exact_search in row["task_notes"]:
                self.search_results.append(row)

    def search_results_with_date_range(self, low, high):
        self.search_results = []
        for row in self.entries:
            if datetime.datetime.strptime(low, '%d/%m/%Y') <= datetime.datetime.strptime(row["task_date"], '%d/%m/%Y') <= datetime.datetime.strptime(high, '%d/%m/%Y'):
                self.search_results.append(row)

    def search_entries_by_regex(self, regex_pattern):
        for row in self.entries:
            if re.match(regex_pattern, row["task_title"]) or re.match(regex_pattern, row["task_notes"]):
                self.search_results.append(row)

    # Shows the search results
    def show_search_results(self):

        self.clear_screen()
        if len(self.search_results):

            # Show the chosen result information
            print("Date: {}".format(self.search_results[self.current_result]["task_date"]))
            print("Title: {}".format(self.search_results[self.current_result]["task_title"]))
            print("Time: {} Minutes".format(self.search_results[self.current_result]["task_time"]))
            print("Notes: {} \n".format(self.search_results[self.current_result]["task_notes"]))
            print("Result {} of {}".format(self.current_result + 1, len(self.search_results)))

        else:
            self.error = "Oops... Looks like your search didn't have results."

    # Gets next result
    def get_next_result(self):
        next_result = self.current_result + 1
        if (next_result < len(self.search_results)):
            self.current_result = next_result
        else:
            self.current_result = 0
        self.show_search_results()

    # Deletes result
    def delete_result(self):
        results = []
        if len(self.entries) == 0:
            self.get_entries()
        for row in self.entries:
            if int(row["task_id"]) != self.current_result:
                results.append(row)
        self.entries = results
        self.update_csvfile()
        self.show_search_results()

    # Update csv file with records
    def update_csvfile(self):
        os.remove('tasks.csv')
        with open("tasks.csv", "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            count = 0
            for row in self.entries:
                writer.writerow({
                    "task_id": count,
                    "task_date": row["task_date"],
                    "task_title": row["task_title"],
                    "task_time": row["task_time"],
                    "task_notes": row["task_notes"]
                })
                count += 1

    # Get specific entry
    def get_entry(self):
        return self.search_results[self.current_result]

    # Gets first entry for tasks.csv
    def get_first_entry(self):
        return self.entries[0]["task_id"]

    # Edits an entry
    def edit_entry(self, task_id, task_date, task_title, task_time, task_notes):
        for row in self.entries:
            if row["task_id"] == task_id:
                row["task_date"] = task_date
                row["task_title"] = task_title
                row["task_time"] = task_time
                row["task_notes"] = task_notes
        self.search_results[self.current_result]["task_date"] = task_date
        self.search_results[self.current_result]["task_title"] = task_title
        self.search_results[self.current_result]["task_time"] = task_time
        self.search_results[self.current_result]["task_notes"] = task_notes
        self.update_csvfile()

    # Validates Information when creating or editing a task
    def validate_information(self, action = "add"):

        # Refresh Screen
        self.refresh()

        if action == "edit":
            entry = self.get_entry()
            print(entry)

        # If task date isn't set, asks for it
        if not self.task_date:
            # Task Date
            if action == "add":
                self.task_date = self.choose_option("Date of the task\nPlease use DD/MM/YYYY")
            else:
                task_date_edit = self.choose_option("Date of the task\nPlease use DD/MM/YYYY\nCurrent Date: "+entry["task_date"]+"\nHit Enter to skip.")
                if not task_date_edit:
                    self.task_date = entry["task_date"]
                else:
                    self.task_date = task_date_edit


        # Checks if valid date
        if(self.validate_date(self.task_date, "%d/%m/%Y")):

            # Refresh Screen
            self.refresh()

            # If Task Title Not Set
            if self.task_title == "":

                if action == "add":
                    # Asks for Task Title
                    self.task_title = self.choose_option("Title of the task")
                else:
                    task_title_edit = self.choose_option("Title of the task\nCurrent Title: "+entry["task_title"]+"\nHit Enter to skip.")
                    if not task_title_edit:
                        self.task_title = entry["task_title"]
                    else:
                        self.task_title = task_title_edit

            # If text is valid
            if(self.validate_text(self.task_title)):

                # Enter Optional Notes
                self.refresh()

                # If Task Time Not Set
                if self.task_time == 0:

                    if action == "add":
                        # Asks for Task Title
                        self.task_time = self.choose_option("Total Minutes spent on the task")
                    else:
                        task_time_edit = self.choose_option("Total Minutes spent on the task\nCurrent Time: "+entry["task_time"]+"\nHit Enter to skip.")
                        if not task_time_edit:
                            self.task_time = entry["task_time"]
                        else:
                            self.task_time = task_time_edit
                    # Asks for Task Time

                if(self.validate_time(self.task_time)):

                    self.refresh()

                    if action == "add":
                        self.task_notes = self.choose_option("Notes (Optional, you can leave this empty)")
                    else:
                        task_notes_edit = self.choose_option("Notes (Optional, you can leave this empty)\nCurrent Notes: "+entry["task_notes"]+"\nHit Enter to skip.")
                        if not task_notes_edit:
                            self.task_notes = entry["task_notes"]
                        else:
                            self.task_notes = task_notes_edit

                    self.clear_screen()

                    if action == "add":
                        # Adds the entry to the Tasks.csv file
                        self.add_entry(self.task_date, self.task_title, self.task_time, self.task_notes)
                        self.choose_option("The entry has been added. Press Enter to return to main menu")
                        self.option = ""
                    else:
                        self.edit_entry(entry["task_id"], self.task_date, self.task_title, self.task_time, self.task_notes)
                        self.choose_option("The entry has been edited. Press Enter to return to search results")

                    # Press Enter to Return to Main Menu
                    self.task_date = ""
                    self.task_title = ""
                    self.task_time = 0
                    self.task_notes = ""
                    self.error = ""

    # Main Program
    def program(self):

        # Program Main Loop
        while self.running:

            # Clear Screen
            self.clear_screen()

            if(self.option==""):
                # Welcome Message and First Menu
                self.welcome_message()
                self.show_menu(self.options)

                # If Error, then show the error
                self.check_error()

                # Choose Menu Options
                self.option = self.choose_option("Please Choose a, b, or c.")

            # Option A
            if self.option == "a":

                self.validate_information()

            # Option B
            elif self.option == "b":

                # Refresh Screen
                self.clear_screen()

                if len(self.entries):

                    # Show Second Menu
                    self.show_menu(self.options_search, "Search Entries\n")

                    # Checks if search option is set
                    if self.option_search == "":

                        # Search Option
                        self.check_error()
                        self.option_search = self.choose_option("Please Choose an option from the menu")

                    if self.option_search == "a":

                        # Check if search date is set
                        if self.search_date == "":

                            # Clears Screen and checks errors
                            self.refresh()
                            # Asks the user for the date he/she wants to search for
                            self.search_date = self.choose_option("Enter the date\nPlease use DD/MM/YYYY")

                        # Validate Search Date
                        if(self.validate_date(self.search_date, "%d/%m/%Y")):

                            # Search Entries by Exact Date
                            self.search_entries_by_date(self.search_date)

                    elif self.option_search == "b":

                        # Checks if search range low is set
                        if self.range_date_low == "":
                            # Clears Screen and checks errors
                            self.refresh()
                            self.range_date_low = self.choose_option("Enter the Date Low Range\nPlease use DD/MM/YYYY")

                        if(self.validate_date(self.range_date_low, "%d/%m/%Y")):
                            # Checks if search range low is set
                            if self.range_date_high == "":
                                # Clears Screen and checks errors
                                self.refresh()
                                self.range_date_high = self.choose_option("Enter the Date High Range\nPlease use DD/MM/YYYY")

                            if(self.validate_date(self.range_date_high, "%d/%m/%Y")):

                                self.search_results_with_date_range(self.range_date_low, self.range_date_high)

                    elif self.option_search == "c":

                        # Check if exact search is Set
                        if self.exact_search == "":

                            # Clears Screen and checks errors
                            self.refresh()
                            # Asks the user for the string he/she wants to search for
                            self.exact_search = self.choose_option("Enter the exact search you want to find")

                        # Validate Search String
                        if(self.validate_exact_search(self.exact_search)):

                            # Search Entries by Exact Date
                            self.search_entries_by_date(self.search_date)

                    elif self.option_search == "d":

                        # Check if regex pattern search is set
                        if self.regex_pattern == "":

                            # Clears Screen and checks errors
                            self.refresh()
                            # Asks the user for the Regex Pattern
                            self.regex_pattern = self.choose_option("Enter the Regex Pattern you want to find")

                        # Validate Regex
                        if(self.validate_regex(self.regex_pattern)):

                            # Search Entries by Exact Date
                            self.search_entries_by_regex(self.regex_pattern)


                    elif self.option_search == "e":
                        # Returns to Main Menu
                        self.option = ""
                        self.error = ""

                    elif self.option_search == "f":
                        # Quits the program
                        self.quit()
                        break

                    else:
                        self.error = "Please choose a valid option."
                        self.option_search = ""

                    # Shows the results results
                    self.clear_screen()
                    self.show_search_results()

                    if len(self.search_results):
                        self.check_error()
                        self.option_result = self.choose_option("[N]ext, [E]dit, [D]elete, [R]eturn to search menu")
                    else:
                        if self.option_search != "e":
                            self.check_error()
                            self.choose_option("Hit Enter to return to search menu")
                            self.option_search = ""

                        else:
                            self.option_search = ""


                    # Show Next Result
                    if self.option_result == "n":
                        self.get_next_result()

                    # Edit Entry
                    elif self.option_result == "e":

                        self.validate_information("edit")

                    # Delete Entry
                    elif self.option_result == "d":
                        self.delete_result()

                    # Return to search menu
                    elif self.option_result == "r":

                        self.option_search = ""
                        self.option_result = ""
                        self.search_results = []
                        self.error = ""

                    # Didn't choose a valid option
                    else:
                        self.error = "Please choose a valid option."
                        self.option_result = ""

                else:
                    print("Before searching, please add some tasks")
                    self.choose_option("Hit Enter to return to main menu")
                    self.option = ""

                # Option C
            elif self.option == "c":
                    # Quits the program
                    self.quit()
                    break

            # No valid Option
            else:
                self.error = "Please choose a valid option."
