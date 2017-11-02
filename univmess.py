import Tkinter
import cv2
import numpy as np
from twilio.rest import Client
import urllib
from geopy.geocoders import Nominatim
import urllib
import requests
import json
import time
import tkMessageBox
import re
import csv
time1 = ''
confile = open('contact.csv', 'r')
for row in csv.DictReader(confile):
  contacts=row
account_sid=""    #enter sid from twilio
auth_token=""     #enter auth_token from twilio
client=Client(account_sid,auth_token)
def check_profanity(text):
  req = urllib.urlopen("http://www.wdylike.appspot.com/?q="+text)
  output = req.read()
  return output
  req.close()
def weather():
    try:
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url,timeout=30)
        j = json.loads(r.text)
        geolocator = Nominatim()
        lat=str(j['latitude'])
        lon=str(j['longitude'])
        con=lat+','+lon
        location = geolocator.reverse(con,timeout=30)
        
        req=requests.get('https://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lon+'&APPID=',timeout=30) #enter appid from openweather
        jweather=json.loads(req.text)
        
        temp=int(jweather['main']['temp'])
        temp=temp-273
        temp=str(temp)
        hum=str(jweather['main']['humidity'])
        wind=str(jweather['wind']['speed'])
        lbl_loc["text"]=jweather['name']+"\n"+location.raw['address']['state_district']+", "+location.raw['address']['state']+", "+location.raw['address']['country']+"\n"+"Temperature: "+temp+" C \n"+"Humidity: "+hum+"% \n"+"Wind Speed: "+wind+" mph"
    except:
        lbl_loc["text"]="Service Unavialable"
def tick():
    global time1
    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    clock.after(200, tick)
def send_message():
  match=re.search(r'RA\d{13}',txt_reg.get())
  if(txt_num.get()== ""):
    num1=lb_code.get("active")
  else:
    num1=txt_num.get()
  curse=0
  while True:
    id=txt_reg.get()
    mess=txt_msg.get()
    mess=mess+" -from "+id
    fw=open('message.txt','w')
    fw.write(mess)
    fw=open('message.txt','r')
    contents_of_file = fw.read()
    fw.close()
    m=check_profanity(contents_of_file)
    if m=="true":
      if(txt_reg.get()==""):
                  tkMessageBox.showerror("No Registration Number", "Enter Registration Number!")
                  break
      elif(match==None):
                  tkMessageBox.showerror("No Registration Number", "Enter Correct Registration Number!")
                  break;
      tkMessageBox.showwarning("User Reported", "You entered curse word!!");
      facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
      cam=cv2.VideoCapture(0);
      sample=0
      while(True):
          ret,img=cam.read();
          gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
          faces=facedetect.detectMultiScale(gray,1.3,5);
          for(x,y,w,h) in faces:
              sample=sample+1;
              cv2.imwrite("dataSet/Reg_"+str(id)+"."+str(sample)+".jpg",gray[y:y+h,x:x+w])
              cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
              cv2.waitKey(100);
          cv2.imshow("Face",img);
          cv2.waitKey(1);
          if(sample>5):
              break;
      cam.release()
      cv2.destroyAllWindows()
      txt_num.delete(0,'end')
      txt_msg.delete(0,'end')
      txt_reg.delete(0,'end')
      break;
    else:
        try:
            num=contacts[num1]
            if(txt_reg.get()==""):
                tkMessageBox.showerror("No Registration Number", "Enter Registration Number!")
                break;
            elif(match==None):
                tkMessageBox.showerror("No Registration Number", "Enter Correct Registration Number!")
                txt_reg.delete(0,'end')
                break;
            message=client.messages.create(
                body=mess,
                to=num,
                from_="+14086694793"
                )
            lbl_num["text"]=num
            tkMessageBox.showinfo("Success", "Message sent successfully to "+num1+"!!\nMessage Id: "+message.sid)
            txt_num.delete(0,'end')
            txt_msg.delete(0,'end')
            txt_reg.delete(0,'end')
            break;
        except:
            lbl_num["text"]="\0"
            tkMessageBox.showerror("Error", "Unregistered Number!");
            txt_num.delete(0,'end')
            txt_msg.delete(0,'end')
            txt_reg.delete(0,'end')
            break;
def messenger():
    root=Tkinter.Tk()
    root.geometry('400x800+0+0')
    root.title("University Messenger")
    lbl_output=Tkinter.Label(root,font=('times', 13),text="Registration Number",bg="sky blue",fg="black")
    lbl_output.pack(fill="both", expand=1)
    global txt_reg
    txt_reg=Tkinter.Entry(root,font=('times', 12, 'bold'),fg="blue",justify="center")
    txt_reg.pack(fill="both", expand=1)
    lbl_contact=Tkinter.Label(root,font=('times', 13),text="Contacts",bg="sky blue")
    lbl_contact.pack(fill="both", expand=1)
    global txt_num
    txt_num=Tkinter.Entry(root,font=('times', 12, 'bold'),fg="red",justify="center")
    txt_num.pack(fill="both", expand=1)
    global lbl_num
    lbl_num=Tkinter.Label(root,font=('times', 13),bg="sky blue")
    lbl_num.pack(fill="both", expand=1)
    global lb_code
    lb_code=Tkinter.Listbox(root,font=('times', 13),fg="red",height=4,selectbackground="green",cursor="ul_angle")
    for people in contacts:
        lb_code.insert("end",people)
    lb_code.pack(fill="both", expand=1)
    lbl_output=Tkinter.Label(root,font=('times', 13),text="Message",bg="sky blue")
    lbl_output.pack(fill="both", expand=1)
    global txt_msg
    txt_msg=Tkinter.Entry(root,font=('times', 12,'bold'),fg="blue")
    txt_msg.pack(fill="both", expand=1)
    btn_message=Tkinter.Button(root,font=('times', 13, 'bold'),text="Send Message",bg="sky blue", command=send_message)
    btn_message.pack()
    lbl_time=Tkinter.Label(root,font=('times', 13),text="Time",bg="sky blue")
    lbl_time.pack(fill="both", expand=1)
    global clock
    clock = Tkinter.Label(root, font=('times', 15, 'bold'))
    clock.pack(fill="both", expand=1)
    tick()
    lbl_add=Tkinter.Label(root,font=('times', 13),text="Location",bg="sky blue")
    lbl_add.pack(fill="both", expand=1)
    global lbl_loc
    lbl_loc=Tkinter.Label(root,font=('times', 12))
    lbl_loc.pack(fill="both", expand=1)
    weather()
    root.mainloop()

