# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 19:44:24 2019

J.A.R.V.I.S Says Hello

@author: Sayan
"""

from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import pymysql

# Add your own database name and password here to reflect in the code
mypass = "1234"
mydatabase="rcpl_db"

con = pymysql.connect(host="localhost",user="root",password=mypass,database=mydatabase)
cur = con.cursor()

# Enter Table Names here
issueTable = "issuedetail" #Issue Table
bookTable = "books" #Book Table
stuTable = "studetail" #Student Table
empTable = "empdetail" #Employee Table
    
allRoll = [] #List To store all Roll Numbers
allEmpId = [] #List To store all Employee IDs
allBid = [] #List To store all Book IDs

def issue():
    
    global issueBtn,labelFrame,lb1,en1,en2,en3,quitBtn,root,Canvas1,status
    
    bid = en1.get()
    issueto = en2.get()
    issueby = en3.get()
    
    issueBtn.destroy()
    quitBtn.destroy()
    labelFrame.destroy()
    lb1.destroy()
    en1.destroy()
    en2.destroy()
    en3.destroy()
    
    
    extractBid = "select bid from "+bookTable
    try:
        cur.execute(extractBid)
        con.commit()
        for i in cur:
            allBid.append(i[0])
        
        if bid in allBid:
            checkAvail = "select status from "+bookTable+" where bid = '"+bid+"'"
            cur.execute(checkAvail)
            con.commit()
            for i in cur:
                check = i[0]
                
            if check == 'avail':
                status = True
            else:
                status = False
        else:
            messagebox.showinfo("Error","Book ID not present")
    except:
        messagebox.showinfo("Error","Can't fetch Book IDs")
    
    extractRollno = "select rollno from "+stuTable
    try:
        cur.execute(extractRollno)
        con.commit()
        for i in cur:
            allRoll.append(i[0])
        
        if issueto in allRoll:
            pass
        else:
            messagebox.showinfo("Error","Roll No not present")
    except:
        messagebox.showinfo("Error","Can't fetch Roll No")
        
    extractEmpID = "select empid from "+empTable
    try:
        cur.execute(extractEmpID)
        con.commit()
        for i in cur:
            allEmpId.append(i[0])
        
        if issueby in allEmpId:
            pass
        else:
            messagebox.showinfo("Error","Emp ID not present")
    except:
        messagebox.showinfo("Error","Can't fetch Emp IDs")
    
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.5)
    
    y = 0.25
    
    Label(labelFrame, text="%-20s%-30s%-30s"%('BID','Issued To','Issued By'),bg='black',fg='white').place(relx=0.27,rely=0.1)
    Label(labelFrame, text="---------------------------------------------------------",bg='black',fg='white').place(relx=0.2,rely=0.2)
    
    issueSql = "insert into "+issueTable+" values ('"+bid+"','"+issueto+"','"+issueby+"')"
    show = "select * from "+issueTable
    
    updateStatus = "update "+bookTable+" set status = 'issued' where bid = '"+bid+"'"
    try:
        if bid in allBid and issueto in allRoll and issueby in allEmpId and status == True:
            cur.execute(issueSql)
            con.commit()
            cur.execute(updateStatus)
            con.commit()
        else:
            allBid.clear()
            allEmpId.clear()
            allRoll.clear()
            return
        con.commit()
        cur.execute(show)
        con.commit()
        for i in cur:
            Label(labelFrame, text="%-20s%-30s%-30s"%(i[0],i[1],i[2]),bg='black',fg='white').place(relx=0.27,rely=y)
            y += 0.1
            print(i)
    except:
        messagebox.showinfo("Search Error","The value entered is wrong, Try again")
    
    print(bid)
    print(issueto)
    print(issueby)
    
    allBid.clear()
    allEmpId.clear()
    allRoll.clear()
    
    backBtn = Button(root,text="< Back",bg='#455A64', fg='white', command=issueBook)
    backBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)

    
def issueBook(): 
    
    global en1,en2,en3,issueBtn,lb1,labelFrame,quitBtn,Canvas1,root,status
    
    root = Tk()
    root.title("Library")
    root.minsize(width=400,height=400)
    root.geometry("600x500")
    
    
    same=True
    n=0.3
    
    # Adding a background image
    background_image =Image.open("library.jpg")
    [imageSizeWidth, imageSizeHeight] = background_image.size
    
    newImageSizeWidth = int(imageSizeWidth*n)
    if same:
        newImageSizeHeight = int(imageSizeHeight*n) 
    else:
        newImageSizeHeight = int(imageSizeHeight/n)

    
    Canvas1 = Canvas(root)
    
    Canvas1.config(bg="#706fd3",width = newImageSizeWidth, height = newImageSizeHeight)
    Canvas1.pack(expand=True,fill=BOTH)
    
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.3)
        
    headingFrame1 = Frame(root,bg="#333945",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
        
    headingFrame2 = Frame(headingFrame1,bg="#EAF0F1")
    headingFrame2.place(relx=0.01,rely=0.05,relwidth=0.98,relheight=0.9)
        
    headingLabel = Label(headingFrame2, text="ISSUE BOOK", fg='black')
    headingLabel.place(relx=0.25,rely=0.15, relwidth=0.5, relheight=0.5)   
        
    # Book ID
    lb1 = Label(labelFrame,text="Book ID : ", bg='black', fg='white')
    lb1.place(relx=0.05,rely=0.2)
        
    en1 = Entry(labelFrame)
    en1.place(relx=0.3,rely=0.2, relwidth=0.62)
    
    # Issued To Roll Number 
    lb2 = Label(labelFrame,text="Issued To(rollno) : ", bg='black', fg='white')
    lb2.place(relx=0.05,rely=0.4)
        
    en2 = Entry(labelFrame)
    en2.place(relx=0.3,rely=0.4, relwidth=0.62)
    
    # Issued By Employee Number
    lb3 = Label(labelFrame,text="Issued By(empid) : ", bg='black', fg='white')
    lb3.place(relx=0.05,rely=0.6)
        
    en3 = Entry(labelFrame)
    en3.place(relx=0.3,rely=0.6, relwidth=0.62)
    
    #Issue Button
    issueBtn = Button(root,text="Issue",bg='#d1ccc0', fg='black',command=issue)
    issueBtn.place(relx=0.28,rely=0.75, relwidth=0.18,relheight=0.08)
    
    quitBtn = Button(root,text="Quit",bg='#aaa69d', fg='black', command=root.quit)
    quitBtn.place(relx=0.53,rely=0.75, relwidth=0.18,relheight=0.08)
    
    root.mainloop()