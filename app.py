from os import system
from time import sleep
import sys
from pymongo import MongoClient as MC
import certifi
from validate_email_address import validate_email 
import re


#connecting database

client = MC("mongodb+srv://sureshkumarm:OxQdM5AdpkpfZXae@cluster0.b4bhdnb.mongodb.net/?retryWrites=true&w=majority", tlsCAFile= certifi.where())

db = client['flight-booking']

userdb = db['userdata']
flightdb = db['flight']
bookdb = db['booking']

system('cls')

def home():
    '''
    function for home page.
    '''
    print("Welcome to Flight Booking System!\n\nUser options:\n1. User\n2. Admin\n")
    print("Enter your choice: ")
    userType = get_input('1', '2')        
    choice = 'User' if userType == '1' else 'Admin'
    redirect(choice)
    
    if userType=='1':
        user()
    else:
        admin()
        
        
def user():
    """Fuction for user login"""
    system('cls')
    print("Welcome to user Dashboard!\n")
    print("1. Login.\n2. Sign Up.\n\nEnter your choice: ")
    choice = int(get_input('1', '2'))
    if choice == 1:
        redirect('Login')
        user_login()
    else:        
        redirect('Sign Up')
        user_reg()
    
    
def admin():
    """Fuction for Admin login"""
    system('cls')
    print("Welcome to Admin Dashboard!\n")
    print("1. Login.\n\nEnter your choice: ")
    choice = int(get_input('1', '6'))
    admin_login()
    
        

def user_dashboard():
    '''User dashboard'''
    system('cls')
    print(f"Welcome {activeUser.get('name')}!\n\n1. Check flight availability and book.\n2. My bookings.\n3. Logout.")
    print("\nEnter your choice: ")
    choice = int(get_input('1', '3'))
    if choice == 1:
        redirect('flight availablility')
        flight_availability()
    elif choice == 2:
        redirect('My bookings')
        myBookings()
    else:
        logout()
    

def flight_availability():
    system('cls')
    print("Flight Availability.\n\nEnter the date of journey (in 24hr format): ")
    date = input()
    data = list(flightdb.find({'date': {'$gte' : date}}))
    if len(data)>0:
        system('cls')
        print(f"Available flights on {date}.\n\n")
        print("Flight Number\tSource\tDestination\tTime\n")
        for i in data:
            print(f"{i['flight_no']}\t{i['src']}\t{i['dest']}\t{i['dep_time']}")
        print("\n1. Book ticket now!\n2. Back to home.\n\nEnter your choice: ")
        choice = int(get_input('1', '2'))
        if choice == 1:
            clearLine(2)
            sleep(1)
            book_flight()
        else:
            for i in range(3,0,-1):
                print(f"\nRedirecting to Dashboard in {i}sec")
                sleep(1)
                clearLine(2)
            user_dashboard()
            
    else:
        print("\nNo flight is available!!!")
        print("\n1. Try again\n2. Back Home.\n\nEnter your choice: ")
        choice = int(get_input('1', '2'))
        if choice == 1:
            for i in range(3,0,-1):
                print(f"\nTrying again in {i}sec")
                sleep(1)
                clearLine(2)
            flight_availability()
        else:
            for i in range(3,0,-1):
                print(f"\nRedirecting to Dashboard in {i}sec")
                sleep(1)
                clearLine(2)
            user_dashboard()
    
    
def book_flight():
    print("\nTo book the flight ticket!\n\nEnter flight number: ")
    f_no = input()
    print("\nNumber of tickets: ")
    count = int(input())
    print(f"\nYou have selected {count} in flight number: {f_no}\n")
    print("1. Confirm\n2.Back to home")
    choice = int(get_input('1', '2'))
    if choice==1:
        data = flightdb.find_one({'flight_no': f_no})
        flightdb.update_one({'flight_no':f_no}, {'$set' : {
            'seats_available' : data['seats_available'] - count
        }})
        bookdb.insert_one({'email' : activeUser['email'],
                           'f_no': f_no,
                           'src': data['src'],
                           'dest': data['dest'],
                           't_count': count})    
        for i in range(3,0,-1):
            print(f"\nTicket booking successfull!!! Redirecting to Dashboard in {i}sec")
            sleep(1)
            clearLine(2)
        user_dashboard()
    else:
        for i in range(3,0,-1):
            print(f"\nRedirecting to Dashboard in {i}sec")
            sleep(1)
            clearLine(2)
        user_dashboard()
        

def myBookings():
    system('cls')
    print(f"\nHello {activeUser['name']}! Here is you bookings.\n\n")
    print("Flight Number\tSource\tDestination\tTicket Count\n")
    data = list(bookdb.find({'email':activeUser['email']}))
    for i in data:
        print(f"{i['f_no']}\t{i['src']}\t{i['dest']}\t{i['t_count']}")
        sleep(1)
    print("\nPress 1 to exit!")
    n = input()
    if n == '1':
        for i in range(3,0,-1):
            print(f"\nRedirecting to Dashboard in {i}sec")
            sleep(1)
            clearLine(2)
        user_dashboard()
        
        
def logout():
    system('cls')
    for i in range(3,0,-1):
        print(f"\nLogout successfull!!! Redirecting to Home in {i}sec")
        sleep(1)
        clearLine(2)
    home()    
    
    
def admin_dashboard():
    '''admin dashboard'''
    system('cls')
    print(f"Welcome back Admin!\n\n1. Add Flight.\n2. Remove Flight.\n3. Flight Bookings.\n4. Logout.")
    print("\nEnter your choice: ")
    choice = int(get_input('1', '4'))
    if choice == 1:
        add_flight()
    elif choice == 2:
        remove_flight()
    elif choice == 3:
        bookings()
    else:
        logout()
        
    
def add_flight():
    system('cls')
    data = {}
    print("Add a flight!\n\n")
    print('Enter flight number: ')
    data['flight_no'] = input()
    print('Enter the source: ')
    data['src'] = input()
    print('Enter the destination: ')
    data['dest'] = input()
    print("Enter flight's date: ")
    data['date'] = input()
    print("Enter flight's time (in 24hr format): ")
    data['dep_time'] = input()
    print('Enter the travel duration (in hrs): ')
    data['duration'] = input()
    print('Enter the seating capacity: ')
    data['capacity'] = int(input())
    data['seats_available'] = data['capacity']
    
    system('cls')
    
    print(f"\n\nYou have entered!!!\n\n" 
            f"Flight Number: {data['flight_no']}\n" 
            f"Source: {data['src']}\n" 
            f"Destination: {data['dest']}\n" 
            f"Date: {data['date']}\n" 
            f"Time: {data['dep_time']}\n" 
            f"Duration: {data['duration']}\n" 
            f"Capacity: {data['capacity']}\n" 
            f"Seats Available: {data['seats_available']}\n")
    
    print(" 21. Confirm to Add.\n2. Cancel and Try again.\n3. Home\n\nEnter your choice: ")
    
    choice = int(get_input('1', '3'))
    if choice == 1:
        flightdb.insert_one(data)
        for i in range(3,0,-1):
            print(f"\nFlight added successfully!!! Redirecting to Dashboard in {i}sec")
            sleep(1)
            clearLine(2)
        admin_dashboard()
    elif choice == 2:
        sleep(1)
        add_flight()
    else:
        for i in range(3,0,-1):
            print(f"\nRedirecting to Dashboard in {i}sec")
            sleep(1)
            clearLine(2)
        admin_dashboard()
    
    
def remove_flight():
    system('cls')
    print("Remove a flight!!!\n\nEnter the Flight you want to remove: ")
    f_no = input()
    data = flightdb.find_one({'flight_no': f_no})
    if data:
        print(f"\n\nYou have selected!!!\n\n" 
            f"Flight Number: {data['flight_no']}\n" 
            f"Source: {data['src']}\n" 
            f"Destination: {data['dest']}\n" 
            f"Date: {data['date']}\n" 
            f"Time: {data['dep_time']}\n" 
            f"Duration: {data['duration']}\n" 
            f"Capacity: {data['capacity']}\n" 
            f"Seats Available: {data['seats_available']}\n")
        print("\n1. Remove\n2. Back Home.\n\n Enter your choice: ")
        choice = int(get_input('1', '2'))
        if choice == 1:
            flightdb.delete_one({'flight_no' : f_no})
            for i in range(3,0,-1):
                print(f"\nFlight number {f_no} is removed Successfully! Redirecting to dashboard in {i}sec")
                sleep(1)
                clearLine(2)
            admin_dashboard()
        else:
            for i in range(3,0,-1):
                print(f"\nRedirecting to Dashboard in {i}sec")
                sleep(1)
                clearLine(2)
            admin_dashboard()
    else:
        print("\nFlight not Found! Invalid Flight number.")
        print("\n1. Try again\n \
                 2. Back Home.\n\n Enter your choice: ")
        choice = int(get_input('1', '2'))
        if choice == 1:
            for i in range(3,0,-1):
                print(f"\nTrying again in {i}sec")
                sleep(1)
                clearLine(2)
            remove_flight()
        else:
            for i in range(3,0,-1):
                print(f"\nRedirecting to Dashboard in {i}sec")
                sleep(1)
                clearLine(2)
            admin_dashboard()
    
    
def bookings():
    ''''''
    system('cls')
    print(f"\nHello Admin! Here is the bookings.\n\n")
    print("Flight Number\tSource\tDestination\tTicket Count\n")
    data = list(bookdb.find())
    for i in data:
        print(f"{i['f_no']}\t{i['src']}\t{i['dest']}\t{i['t_count']}")
        sleep(1)
    print("\nPress 1 to exit!")
    n = input()
    if n == '1':
        for i in range(3,0,-1):
            print(f"\nRedirecting to Dashboard in {i}sec")
            sleep(1)
            clearLine(2)
        admin_dashboard()
    

def user_login():
    '''function for user login'''
    global activeUser
    system('cls')
    print("Welcome back user!\n")
    email = get_email()
    print("\nEnter the password: ")
    password  = input()
    userData = userdb.find_one({'email':email})
    if userData:
        if password == userData['password']:
            for i in range(3,0,-1):
                print(f"\nLogin successfull!!! Redirecting to Dashboard in {i}sec")
                sleep(1)
                clearLine(2)
            activeUser = userData
            user_dashboard()
        else:
            print("\nIncorrect password! Try again.")
            sleep(1)
            user_login()
    else:
        for i in range(3,0,-1):
                print(f"\nUser not found!!! Redirecting to Sign Up in {i}sec")
                sleep(1)
                clearLine(2)
        
    

    
def user_reg():
    '''funtion for user registration'''
    user = {}
    system('cls')
    print("New user registration\n\nEnter your name: ")
    user['name'] = input()
    user['email'] = get_email()
    while True:
        print("\nEnter your password: ")
        password = input()
        if validate_password(password):
            user['password'] = password
            break
        else:
            print("\nPassword should contain atleast one\n*Uppercase\n*Lowercase\n*Number\n*Special character\n*Min length 8")
            sleep(2)
            clearLine(10)
    try: 
        if userdb.find_one({'email': user['email']}):
            for i in range(3,0,-1):
                print(f"\nUser already exist!!! Redirecting to login in {i}sec")
                sleep(1)
                clearLine(2)
            user_login()
        else:
            userdb.insert_one(user)
            sleep(1)
            for i in range(3,0,-1):
                print(f"\nAccount successfully created!!! Redirecting to login in {i}sec")
                sleep(1)
                clearLine(2)
            user_login()
        
    except Exception as e:
        print(e)
    
    
def admin_login():
    ''''''
    system('cls')
    print("Welcome back Admin!\n")
    email = get_email()
    print("\nEnter the password: ")
    password  = input()
    if email == 'admin123@gmail.com' and password == 'Admin@123':
        for i in range(3,0,-1):
            print(f"\nLogin successfull!!! Redirecting to Dashboard in {i}sec")
            sleep(1)
            clearLine(2)
    else:
        print("\nIncorrect credentials. Try Again!")
        sleep(1)
        admin_login()
    admin_dashboard()
        

def clearLine(n):
    for i in range(n):
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear the line
        
        
def get_input(start, end):
    choice = ''
    while True :
        try:
            choice = input()
        except:
            print("\nInvalid choice!")
            sleep(1)          
            clearLine(4)
            print(f"Enter a valid choice ({start} - {end}): ")
        if choice.isdigit() and (choice>= start and choice<=end):
            break
        else:
            print("\nInvalid choice!")
            sleep(1)
            clearLine(4)
            print(f"Enter a valid choice ({start} - {end}): ")
    return choice


def redirect(to):
    for i in range(3,0,-1):
        print(f'\nYou have selected {to} option. Redirecting in {i}sec.')
        sleep(1)
        clearLine(2)
        

def validate_password(password):
    if len(password)>=8 and bool(re.search(r'[a-z]', password)) and \
        bool(re.search(r'[A-Z]', password)) and bool(re.search(r'[0-9]', password)) \
        and bool(re.search(r'[^\w\s]', password)):
        return True
    return False

def get_email():
    email = ''
    while True:
        print("\nEnter your email: ")
        email = input()
        if validate_email(email):
            return email
        else:
            print("\nInvalid email!")
            sleep(1)
            clearLine(5)
            
            
if __name__ == '__main__':
    home()
