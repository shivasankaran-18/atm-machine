import mysql.connector as m
from random import *

mycon=m.connect(host='localhost',user='root',passwd='Lastbencher_07',database='standard_chartered_bank')
cur=mycon.cursor()

def pin():
    global sec_pin
    while True:
        if sec_pin in sepin:
            print('THE PIN ALREADY EXISTS.')
            sec_pin=int(input("PLEASE ENTER ANOTHER FOUR DIGIT SECURITY PIN FOR YOUR NEW ACCOUNT:" ))
        else:
            break

def withdraw(wamt):
    global bal  
    bal=data2[0][3]-wamt
    query3='update account_holder_details set balance_amount={} where acc_no={}'.format(bal,accountno)
    cur.execute(query3)
    mycon.commit()
   
    
def deposit(damt):
    global bal 
    bal=data2[0][3]+damt
    query4='update account_holder_details set balance_amount={} where acc_no={}'.format(bal,accountno)
    cur.execute(query4)
    mycon.commit()

def details():
    query5="select * from account_holder_details where acc_no={} and security_pin={}".format(accountno,securitypin)
    cur.execute(query5)
    data5=cur.fetchall()
    for i in data5:
        en=str(i[2])
        print("YOUR ACCOUNT NUMBER IS:",i[0])
        print("YOUR NAME IS:",i[1])
        print("YOUR SECURITY PIN IS:",en[0]+"XX"+en[3])
        print("YOUR CURRENT BALANCE IS:",i[3])
        print("YOUR  CITY:",i[4])

def edit():
    up=input('DO YOU WANT TO UPDATE YOUR NAME OR YOUR CITY OR BOTH?')
    if up in ['name','NAME']:
        new_name=input("ENTER YOUR NEW NAME:")
        query6="update account_holder_details set acc_holder_name='{}' where acc_no={}".format(new_name,accountno)
        cur.execute(query6)
        print('YOUR NAME HAS BEEN UPDATED SUCCESSFULLY')
        mycon.commit()
    elif up in ['city','CITY']:
        new_city=input('ENTER YOUR NEW LOCATION:')
        query7="update account_holder_details set city='{}' where acc_no={}".format(new_city,accountno)
        cur.execute(query7)
        print('YOUR CITY HAS BEEN UPDATED SUCCESSFULLY')
        mycon.commit()
    elif up in ['both','BOTH']:
        new_namee=input("ENTER YOUR NEW NAME:")
        query8="update account_holder_details set acc_holder_name='{}' where acc_no={}".format(new_namee,accountno)
        cur.execute(query8)
        new_cityy=input('ENTER YOUR NEW LOCATION:')
        query9="update account_holder_details set city='{}' where acc_no={}".format(new_cityy,accountno)
        cur.execute(query9)
        print('YOUR DETAILS HAS BEEN UPDATED SUCCESSFULLY')
        mycon.commit()

def delete():
    cho=input("ARE YOU SURE THAT YOU WANT TO DELETE YOUR ACCOUNT?")
    if cho=='no' or cho=='NO' or cho =='No':
        pass
    elif cho in ['YES','yes','Yes']:
        query11="delete from account_holder_details where acc_no={}".format(accountno)
        cur.execute(query11)
        mycon.commit()
        print("YOUR ACCOUNT HAS BEEN DELETED SUCCESSFULLY")
        
def beneficiary():
    query20='select * from account_holder_details where acc_no={}'.format(taccn)
    cur.execute(query20)
    data20=cur.fetchall()
    bal1=data20[0][3]+tramt
    query19='update account_holder_details set balance_amount={} where acc_no={}'.format(bal1,taccn)
    cur.execute(query19)
    mycon.commit()        



print('''======================
            WELCOME TO SRH BANK
======================''')

#screen 1
while True:
    print('''1.CREATE ACCOUNT
2.EXISTING USER
3.EXIT''') 
    choice=int(input('ENTER YOUR CHOICE:'))
    if choice==1:
        name=input("PLEASE ENTER  YOUR NAME:")
        city=input("PLEASE ENTER YOUR CITY:")
        balance=0
        acc_no=randint(100000,999999)
        print("YOUR NEW ACCOUNT NUMBER IS :",acc_no)
        sec_pin=int(input("PLEASE ENTER YOUR FOUR DIGIT SECURITY PIN FOR YOUR NEW ACCOUNT:" ))
        query='select  security_pin from account_holder_details '
        cur.execute(query)
        data=cur.fetchall()
        sepin=[]
        for i in data:
            a=i[0]
            sepin.append(a)
        pin()
        query1="insert into account_holder_details values({},'{}',{},{},'{}')".format(acc_no,name,sec_pin,balance,city)
        cur.execute(query1)
        print('YOUR ACCOUNT HAS BEEN SUCCESSFULLY CREATED')
        mycon.commit()

    elif choice==2:
        accountno=int(input('ENTER YOUR ACCOUNT NUMBER:'))
        query12="select * from account_holder_details where acc_no={} ".format(accountno)
        cur.execute(query12)
        data12=cur.fetchall()
        
        if data12==[]:
            print('ACCOUNT DOES NOT EXIST..PLEASE CREATE AN ACCOUNT')
            continue
        elif accountno==data12[0][0]:
            securitypin=int(input('ENTER YOUR SECURITY PIN:'))
            query2="select * from account_holder_details where acc_no={} and security_pin={}".format(accountno,securitypin)
       
            cur.execute(query2)
            data2=cur.fetchall()
            
            if data2==[]:
                print('INCORRECT SECURITY PIN')
                continue
                
            elif securitypin==data2[0][2]:
                #2 screen
                while True:
                    query2="select * from account_holder_details where acc_no={} and security_pin={}".format(accountno,securitypin)
       
                    cur.execute(query2)
                    data2=cur.fetchall()
                    bal=data2[0][3]
                    print('''
=========================
SELECT THE PREFERRED OPTIONS:
=========================
1.WITHDRAW AMOUNT
2.DEPOSIT AMOUNT
3.SHOW ACCOUNT DETAILS
4.EDIT ACCOUNT DETAILS
5.DELETE ACCOUNT
6.TRANSFER AMOUNT TO ANOTHER SRH BANK ACCOUNT
7.EXIT
''','CURRENT BALANCE:',str(bal)+".00")
                    
                    opt=int(input('ENTER THE CHOICE:'))
                    if opt==1:
                        withdraw_amt=int(input('PLEASE ENTER THE AMOUNT TO BE WITHDRAWN:'))
                        if withdraw_amt>bal:
                            print('INSUFFICIENT BALANCE')
                        else:
                            withdraw(withdraw_amt)
                            print('COLLECT YOUR CASH!!')
                            
                    elif opt==2:
                        deposit_amt=int(input('PLEASE ENTER THE AMOUNT TO BE DEPOSITED:'))
                        deposit(deposit_amt)
                        print('AMOUNT DEPOSITED SUCCESSFULLY')
                         
                    elif opt==3:
                        details()
                        
                    elif opt==4:
                        edit()

                    elif opt==5:
                        delete()
                        break

                    elif opt==6:
                        taccn=int(input('ENTER THE BENEFICIARY ACCOUNT NUMBER:'))
                        tramt=int(input('ENTER THE AMOUNT TO BE TRANSFERRED:'))
                        withdraw(tramt)
                        beneficiary()
                        print('YOUR TRANSACTION IS COMPLETED')

                    elif opt==7:
                        break
                
    elif choice==3:
        print('THANK YOU FOR YOUR TRANSACTION..!!!')
        break
                   
                    

    
