import mysql.connector
from tabulate import tabulate
import random
import datetime

#connecting to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234", 
    database="computer_project"
)

cur = db.cursor()


#menu function
def menu():
    print("Select an Option to get going or type 'q' or 'quit' to quit.")
    print("--------------------------------------------------")
    print("1.Check trains. \n2.View Ticket. \n3.Book Train. \n4.Cancel Booking.")


#check avaialble trains and their status
def check_trains():

    cur.execute("SELECT * FROM trains;")
    result = cur.fetchall() #tuple of trains with information 
    
    #displaying the table
    header = ["TRAIN NAME", "DESTINATION", "TRAIN STATUS", "FARE ₹", "SEATS AVAILABLE"]
    print(tabulate(result, headers=header, tablefmt="simple_grid"))
    
    
#book a train
def book_train():

    #generate pnr number
    pnr = None
    cur.execute("SELECT pnr FROM bookings;")
    pnr_list = cur.fetchall()
    while(True):
        pnr = random.randint(10**9, (10**10)-1)
        if pnr in pnr_list:
            continue
        else:
            break

    username = input(str("Enter passenger name >> "))
    
    #for choice of trains
    cur.execute("SELECT train_name, destination, fare, seats FROM trains WHERE seats > 0;")
    train_choices = cur.fetchall()

    print("Enter the number for the train choice.")
    for i in range(len(train_choices)):
        print("\t","[",i+1,"]", train_choices[i][0])

    choice = None
    while(True):
        choice = int(input(" >> "))-1
        if choice > len(train_choices) or choice < 0:
            print("Please enter a valid train number.")
        else:
            break

    phoneno = None
    while(True):
        phoneno = int(input("Enter phone number >> "))
        if phoneno >= 999999999 and phoneno < 9999999999:
            break

    boarding_date = str(input("Enter boarding date in YYYY-MM-DD format [e.g. 2019-12-03] >> "))
    datetoday = datetime.datetime.now().strftime("%Y-%m-%d")
    timenow = datetime.datetime.now().strftime("%H:%M:%S")

    #inserting data into table
    booking_data = "INSERT INTO bookings (pnr, username, phoneno, train_name, destination, fare, booking_time, booking_date, boarding_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    booking_value = (pnr, username, phoneno, train_choices[choice][0], train_choices[choice][1], train_choices[choice][2], timenow, datetoday, boarding_date)
    cur.execute(booking_data, booking_value)

    #updating available seats in train
    cur.execute("UPDATE trains SET seats = seats-1 WHERE train_name=%s", (train_choices[choice][0],))
    print(f"\nCongratulations! Booking confirmed.\nYour PNR is {pnr}. You need this to view your ticket.")
    
    db.commit()


#View any booked ticket using pnr number
def view_ticket():
    userpnr = int(input("Enter PNR >> "))
    cur.execute("SELECT pnr FROM bookings;")
    pnr = cur.fetchall()

    if (userpnr,) in pnr:
        cur.execute("SELECT * FROM bookings WHERE pnr=%s;", (userpnr,))
        booking = cur.fetchall()
        header = ["PNR", "NAME", "PHONE NO.", "TRAIN NAME", "DESTINATION", "FARE-PAID ₹", "BOOKING TIME", "BOOKING DATE", "BOARDING DATE"]
        print(tabulate(booking, headers=header, tablefmt="simple_grid"))
    else:
        print("Booking with this PNR doesn't exist.")

    
#Cancel booked ticket using pnr number
def cancel_ticket():
    userpnr = int(input("Enter PNR >> "))
    cur.execute("SELECT pnr FROM bookings;")
    pnr = cur.fetchall()

    if (userpnr,) in pnr:
        print("Are you sure you want to cancel booking [y or n]?")
        while(True):
            confirm = str(input(">> "))
            if confirm == 'y':
                cur.execute("SELECT train_name FROM bookings WHERE pnr=%s;", (userpnr,))
                details = cur.fetchall()
                cur.execute("UPDATE trains SET seats = seats+1 WHERE train_name = %s;", details[0])
                cur.execute("DELETE FROM bookings WHERE pnr=%s;", (userpnr,))
                db.commit()
                print("Booking successfully cancelled.")
                break
            elif confirm == 'n':
                break
            else:
                print("Invalid input.")
     
    else:
        print("Booking with this PNR doesn't exist.")



#main loop to execute all the functions
quit = False

while(quit != True):
    menu()
    choice = input(">> ")

    if choice == "q" or choice == "quit":
        print("Thank you.")
        quit = True
        db.close()
    elif choice == '1':
        check_trains()
    elif choice == '2':
        view_ticket()
    elif choice == '3':
        book_train()
    elif choice == '4':
        cancel_ticket()
    else: 
        print("Invalid choice.")

    print("\n")