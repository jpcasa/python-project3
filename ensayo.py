import csv

with open("tasks.csv", "a") as csvfile:
    fieldnames = ["task_date", "task_title", "task_notes"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
