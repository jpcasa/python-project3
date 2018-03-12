import os
import datetime
import csv

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
        self.task_title = ""
        self.task_notes = ""
        self.fieldnames = ["task_date", "task_title", "task_notes"]
        self.search_results = []
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
        for key, value in options.items():
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

    # Shorcut to clear screen and check errorss
    def refresh(self):
        self.clear_screen()
        self.check_error()

    # Adds entry to tasks.csv
    def add_entry(self, task_date, task_title, task_notes):
        with open("tasks.csv", "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow({
                "task_date": task_date,
                "task_title": task_title,
                "task_notes": task_notes
            })

    # Search Entries by Date
    def search_entries_by_date(self, date):
        with open("tasks.csv") as csvfile:
            artreader = csv.DictReader(csvfile)
            rows = list(artreader)
            for row in rows:
                if row["task_date"] == date:
                    self.search_results.append(row)

    # Shows the search results
    def show_search_results(self):

        # Show the chosen result information
        print("Date: {}".format(self.search_results[0]["task_date"]))
        print("Title: {}".format(self.search_results[0]["task_title"]))
        print("Notes: {} \n".format(self.search_results[0]["task_notes"]))

        print("Result {} of {}".format(self.current_result + 1, len(self.search_results)))


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

                # Refresh Screen
                self.refresh()

                # If task date isn't set, asks for it
                if self.task_date == "":
                    # Task Date
                    self.task_date = self.choose_option("Date of the task\nPlease use DD/MM/YYYY")

                # Checks if valid date
                if(self.validate_date(self.task_date, "%d/%m/%Y")):

                    # Refresh Screen
                    self.refresh()

                    # If Task Title Not Set
                    if self.task_title == "":
                        # Asks for Task Title
                        self.task_title = self.choose_option("Title of the task")

                    # If text is valid
                    if(self.validate_text(self.task_title)):

                        # Enter Optional Notes
                        self.refresh()
                        self.task_notes = self.choose_option("Notes (Optional, you can leave this empty)")

                        # Adds the entry to the Tasks.csv file
                        self.add_entry(self.task_date, self.task_title, self.task_notes)
                        self.clear_screen()

                        # Press Enter to Return to Main Menu
                        self.choose_option("The entry has been added. Press Enter to return to main menu")
                        self.option = ""
                        self.task_date = ""
                        self.task_title = ""
                        self.task_notes = ""

            # Option B
            elif self.option == "b":

                # Refresh Screen
                self.clear_screen()

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
                    print("b")
                elif self.option_search == "c":
                    print("c")
                elif self.option_search == "d":
                    print("d")
                elif self.option_search == "e":
                    # Returns to Main Menu
                    self.option = ""
                    self.option_search = ""
                elif self.option_search == "f":
                    # Quits the program
                    self.quit()
                else:
                    self.error = "Please choose a valid option."
                    self.option_search = ""

                self.clear_screen()
                self.show_search_results()
                self.option_result = self.choose_option("[N]ext, [E]dit, [D]elete, [R]eturn to search menu")

                # Option C
            elif self.option == "c":
                    # Quits the program
                    self.quit()

            # No valid Option
            else:
                self.error = "Please choose a valid option."
