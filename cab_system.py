import datetime
import random
from tabulate import tabulate
from fpdf import FPDF
import mail
import smtplib
import sys
import re


print("    Welcome To Uber Service    ".center(100,'⦾'),"\n")

#Available Routes

routes={'SWARGATE-KOTHRUD':20,'SWARGATE-HADAPSAR':15,'SWARGATE-VIMANNAGAR':25,
        'KOTHRUD-SWARGATE':20,'HADAPSAR-SWARGATE':15,'VIMANNAGAR-SWARGATE':25}
vehicle={'Sr.No':[1,2,3,4],'Car Type':['AUTO','MINI','SEDAN','SUV'],'Fare':[15,20,25,30]}
fare={'AUTO':15,'MINI':20,'SEDAN':25,'SUV':30}

#Printing Vehicle Types

print("   Vehicle Types   ".center(100,'⦾'))
print('\n\t\tSr.No\t\t\t\tCar Type\t\t\tFare')
for a in range(len(vehicle['Sr.No'])):
    for i,j in vehicle.items():
        print(f'\t\t{j[a]}\t\t',end='')
    print()


#Printing Available Routes    
print('\n',"    Available Routes    ".center(100,'⦾'),'\n')
list_routes=routes.keys()
for i in list_routes:
    print('\t➤ ',i)

print('\n',"    Book Your Ride    ".center(100,'⦾'),'\n')

#Get Picking Point and Droping Point
pick_up=input("\n\t◙ Pick Up Location : ")
pick_up=pick_up.upper()
drop=input("\n\t◙ Drop Location : ")
drop=drop.upper()
car=input("\n\t◙ Vehicle Type : ")
car=car.upper()
route_to_find=pick_up+'-'+drop
fare_to_find=car

print('\n',"    Ride Details    ".center(100,'⦾'),'\n')
#Find Routes and distance

if route_to_find in routes.keys():
    print(f'\n\t① Distance Between {pick_up} And {drop}= {routes[route_to_find] } KM')
else:
    sys.exit(f"\n\t① Enterd Routes {pick_up}-{drop} is not in available our route list" )

#Calculate Base Fare

if fare_to_find in fare.keys():
        print(f'\n\t② Fare For {car} = {fare[fare_to_find] } Rs/KM')
        base_fare=fare[fare_to_find]*routes[route_to_find]
        print(f'\n②\t Fare For This Ride {base_fare} ₹ (Exculding Taxex)')
else:
    sys.exit(f"\n\t② {car} Type Vehicle Is Not Available " )
    

#Confirmation

print('\n',"    Confirmation    ".center(100,'⦾'),'\n')
ride=input('\n\t● Do You Want To Book Ride? [Yes/No] : ')
ride=ride.upper()

def checkmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        pass
    else:
        sys.exit("\n\t★ Invalid Email Address")

def checkmobile(mobile):
    regex=r'[6-9][0-9]{9}'
    if(re.fullmatch(regex, mobile)):
        pass
    else:
        sys.exit("\n\t★ Invalid Mobile Number")

        




if ride=='YES':
    name=input('\n\t■ Enter Your Name :')
    mobile=input("\n\t■ Enter Your Contact Number : ")
    checkmobile(mobile)
    email=input("\n\t■ Enter Your Email ID : ")
    checkmail(email)
    print("\n\t★ Thanks For Booking Ride With Us")
    print("\n\t★ Driver Will Come Soon To Your Pick-Up Point")
elif ride=='NO':
    print("\n\t★ Thanks For Visiting Our Site")
else:
    print("\n\t★ Wrong Option Selected")
#Ride Number

ride_no=random.randint(0,100000)

#Ride Time
now = datetime.datetime.now()
date=now.strftime("%d-%m-%Y %H:%M:%S")


#Total Fare Including Tax
gst=base_fare/100*9
total_fare=base_fare+gst+gst

#Bill Print
bill=input('\n\t● Do You Want To Billing Invoice? [Yes/No] : ')
bill=bill.upper()

#Bill Table 
if bill=='YES':
    print('\n',"    Your Last Ride Bill    ".center(100,'⦾'),"\n")
    print(tabulate([['Date And Time',date],['Ride Number',ride_no],['Passanger Name',name],
       ['Passanger Mobile-No',mobile],['Passanger Email-ID',email],
       ['Pick-Up Point',pick_up.upper()],['Droping Point',drop.upper()],
       ['Base Fare',base_fare],['CGST 9%',gst],
       ['SGST 9%',gst],['Total Fare',total_fare]],tablefmt="grid"))
    print("\n\t★ Thanks For Riding With Us")
else:
    print("\n\t★ Thanks For Riding With Us")


# Bill PDF
def bill_pdf():
    pdf = FPDF()
    pdf.set_font_size(16)
    pdf.add_page()
    pdf.write_html(f"""
        <h1 align="center">Billing Invoice</h1>
        <p align="right">Date Of Ride</p>
        <p align="right">{date}</p>
        <p align="right">Ride No :{ride_no}</p>
        <table width="100%" border="1">
            <tr>
                <th width="50%">Passanger Name</th>
                <th width="50%">{name}</th>
            </tr>
            <tr>
                <th width="50%">Passanger Mobile No</th>
                <th width="50%">{mobile}</th>
            </tr>
            <tr>
                <th width="50%">Passanger E-Mail ID</th>
                <th width="50%">{email}</th>
            </tr>
            <tr>
                <th width="50%">Pick-Up Point</th>
                <th width="50%">{pick_up}</th>
            </tr>
            <tr>
                <th width="50%">Droping Point</th>
                <th width="50%">{drop}</th>
            </tr>
            <tr>
                <th width="50%">Vehicle Type</th>
                <th width="50%">{car}</th>
            </tr>
            <tr>
                <th width="50%">Base Fare</th>
                <th width="50%">{base_fare} Rs</th>
            </tr>
            <tr>
                <th width="50%">CGST 9%</th>
                <th width="50%">{gst} Rs</th>
            </tr>
            <tr>
                <th width="50%">SGST 9%</th>
                <th width="50%">{gst} Rs</th>
            </tr>
            <tr>
                <th width="50%">Total Fare</th>
                <th width="50%">{total_fare} Rs</th>
            </tr>
        </table>"""
    
    )
    pdf.output(f'{ride_no}.pdf')


bill_pdf()



server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

server.login(mail.email,mail.password)
#filename = f"{ride_no}.pdf"
#attachment = open(f"E:\uber_project\{ride_no}.pdf", "r",encoding='UTF-8')

SUBJECT=f'Ride Bill{ride_no}'
body=f'Hii{name}'
msg=f"Hii {name}\nRide Bill {ride_no}\nDate {date}\nPassanger Name : {name}\nMobile No : {mobile}\nE-Mail : {email}\
    \nPick-Up Point : {pick_up}\nDroping Point :{drop}\nVehicle Type : {car}\nBase Fare : {base_fare}Rs\
    \nCGST 9% : {gst} Rs\nSGST 9% : {gst} Rs\nTotal Fare : {total_fare} Rs\nThanks For Riding With Us"
server.sendmail('yashrajb007@gmail.com',email,msg)
# server.sendmail(sender_email, receiver_email, message)
print('Bill Sent Successfully !!')
#





