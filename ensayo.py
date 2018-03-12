import datetime
dt1 = datetime.datetime.strptime('12/11/1991', '%d/%m/%Y')
dt2 = datetime.datetime.strptime('14/11/1991', '%d/%m/%Y')
dt3 = datetime.datetime.strptime('16/11/1991', '%d/%m/%Y')

if dt1 <= dt2 <= dt3:
    print("works")
else:
    print("Paila")
