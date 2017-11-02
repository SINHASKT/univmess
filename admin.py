import Tkinter
import univmess
import tkMessageBox
import numpy as np
import cv2
import os
def admin():
    root11.destroy()
    global root2
    root2=Tkinter.Tk()
    root2.geometry('200x110+0+0')
    root2.title("Login")
    lbl_login=Tkinter.Label(root2,font=('times', 13),text="Enter Password",bg="sky blue")
    lbl_login.pack(fill="both",expand=1)
    global txt_pass
    txt_pass=Tkinter.Entry(root2,font=('times', 13, 'bold'),fg="blue",show="*")
    txt_pass.pack(fill="both",expand=1)
    btn_login=Tkinter.Button(root2,font=('times', 13, 'bold'),text="Login",bg="sky blue",command=login)
    btn_login.pack(fill="both",expand=1)
    root2.mainloop()

def login():
    pas=txt_pass.get()
    f=open("abc.txt","r")
    x=f.read()
    if(pas==""):
        tkMessageBox.showerror("Error", "Enter a Password");
    elif(x==pas):
        root2.destroy()
        # Load an color image in grayscale
        files=os.listdir('dataSet')
        n=len(files)
        while n>0:
            file_name=files[n-1]
            n=n-6
            name='dataSet\\'+file_name
            img = cv2.imread(name,0)
            cv2.imshow('image',img)
            file_name=file_name[4:19]
            tkMessageBox.showinfo("Reported ID", file_name);
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        login.count=login.count+1;
        if(login.count>3):
            root2.destroy()
            tkMessageBox.showinfo("Exceeded limit", "Exceeded the count");
        else:
            x=str(3-login.count)
            tkMessageBox.showwarning("","Worng Password. \n"+x+" attempts left.");
    f.close()
login.count=0
global root11 
root11=Tkinter.Tk()
root11.geometry('200x60+0+0')
root11.title("University Messenger")
btn_message=Tkinter.Button(root11,font=('times', 13, 'bold'),text="Enter \n Messenger",bg="sky blue",command=univmess.messenger)
btn_message.grid(row=0,column=0)
btn_admin=Tkinter.Button(root11,font=('times', 13, 'bold'),text="Admin \n Login",bg="sky blue",command=admin)
btn_admin.grid(row=0,column=3)
root11.mainloop()

