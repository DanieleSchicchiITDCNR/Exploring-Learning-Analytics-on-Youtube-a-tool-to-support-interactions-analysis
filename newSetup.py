import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from lib import create_connection

def callback(input): 
      
    if input.isdigit(): 
        print(input) 
        return True
                          
    elif input == "": 
        print(input) 
        return True
  
    else: 
        print(input) 
        return False

def save(account,method,steps,time,query,iterations,frequency,gradeFrequency):
    forConversion={"Minuti":60,"Ore":3600,"Giorni":3600*24}
    DBquery="insert into setupsessione(account,tipo,query,steps,viewTime,status,frequency,iterations) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    connection= create_connection("localhost","root","","tesi")
    cursor=connection.cursor()
    
    cursor.execute(DBquery,[account,method,query,steps,time,"ready",int(frequency)*int(forConversion[gradeFrequency]),iterations])
    connection.commit()
    

accountList={" Account iscritto ad alcuni canali":"emailperlatesi@gmail.com"," Account pulito":"emailperlatesi3@gmail.com"}

methodList={" Per successivo":1," Tutti i correlati":2}



window = tk.Tk() 

window.title("New session setup")
window.geometry("450x320")

print(list(methodList.keys()))
fontExample = ("Courier", 16, "bold")

#----creazione Combobox per la selezione dell'account con cui effettuare la sessione----------
accountLabel = tk.Label(window,text = "Seleziona tipologia account")
accountLabel.place(x=20,y=10,width=150)
accountCombo = ttk.Combobox(window,values=list(accountList.keys()))
accountCombo.place(x=20,y=30,width=200)

#----/creazione Combobox per la selezione dell'account con cui effettuare la sessione----------

#----creazione Combobox per la selezione del metodo con cui effettuare la sessione----------
methodLabel = tk.Label(window,text = "Seleziona metodo esplorazione")
methodLabel.place(x=245,y=10,width=180)
methodCombo = ttk.Combobox(window,values=list(methodList.keys()))
methodCombo.place(x=250,y=30,width=180)
#----/creazione Combobox per la selezione del metodo con cui effettuare la sessione----------

#----creazione casella di testo per inserimento del numero di passi da effettuare durante la sessione----------
stepsLabel = tk.Label(window,text = "Inserisci il numero di passi")
stepsLabel.place(x=230,y=60,width=180)
stepsEntry = ttk.Entry(window) 
stepsEntry.place(x = 250, y = 80) 
reg = window.register(callback) 
stepsEntry.config(validate ="key",  validatecommand =(reg, '%P')) 
#----/creazione casella di testo per inserimento del numero di passi da effettuare durante la sessione----------
  
#----creazione casella di testo per inserimento del tempo di visualizzazione dei video----------
timeLabel = tk.Label(window,text = "Inserisci tempo visualizzazione in secondi")
timeLabel.place(x=15,y=60,width=230)
timeEntry = ttk.Entry(window) 
timeEntry.place(x = 20, y = 80) 
reg = window.register(callback) 
timeEntry.config(validate ="key",  validatecommand =(reg, '%P')) 
#----/creazione casella di testo per inserimento del tempo di visualizzazione dei video----------
  
#----creazione casella di testo per inserimento della query di ricerca----------
queryLabel = tk.Label(window,text = "Inserisci query di ricerca")
queryLabel.place(x=-8,y=110,width=180)
queryEntry = ttk.Entry(window) 
queryEntry.place(x =20 , y = 130,width=300) 
#----/creazione casella di testo per inserimento della query di ricerca----------

#----creazione casella di testo per inserimento del numero di iterazioni----------
iterationsLabel = tk.Label(window,text = "Quante volte vuoi eseguire la ricerca?")
iterationsLabel.place(x=18,y=160,width=200)
iterationsEntry = ttk.Entry(window) 
iterationsEntry.place(x =20 , y = 180,width=50) 
reg = window.register(callback) 
iterationsEntry.config(validate ="key",  validatecommand =(reg, '%P')) 
#----/creazione casella di testo per inserimento del numero di iterazioni----------

#----creazione casella di testo per inserimento della frequenza----------
frequencyLabel = tk.Label(window,text = "Con che frequenza?")
frequencyLabel.place(x=-20,y=210,width=180)
frequencyEntry = ttk.Entry(window) 
frequencyEntry.place(x =20 , y = 230,width=80) 
reg = window.register(callback) 
frequencyEntry.config(validate ="key",  validatecommand =(reg, '%P')) 

frequencyCombo = ttk.Combobox(window,values=["Minuti","Ore","Giorni"])
frequencyCombo.place(x=105,y=230,width=180)
#----/creazione casella di testo per inserimento della frequenza----------

saveButton=ttk.Button(window,text="Save setup",command=lambda:save(accountList[accountCombo.get()],methodList[methodCombo.get()],stepsEntry.get(),timeEntry.get(),queryEntry.get(),iterationsEntry.get(),frequencyEntry.get(),frequencyCombo.get()))
saveButton.place(x=180, y=270)
window.mainloop()
'''

accountList={" Account iscritto ad alcuni canali":"emailperlatesi@gmail.com"," Account pulito":"emailperlatesi2@gmail.com"}

print('Seleziona l\'account da utilizzare, inserisci:\n 1. per l\'account iscritto a canali "controversi"\n 2. per l\'account "pulito"  ')
account=int(input())
metodo=input('Seleziona il metodo di esplorazione, inserisci:\n 1. per seguire i video successivi\n 2. per guardare i correlati  ')
tempo_osservazione=int(input('Inserisci il tempo di osservazione desiderato (in secondi):'))
query=input('Inserisci la parola o frase che vuoi cercare su youtube:')
steps=int(input('Inserisci il numero di steps da eseguire:'))

if(metodo=="1"):
    exec(open("exploreByNext.py").read(),{'account':list(accountList.values())[account-1],'tempo_osservazione':tempo_osservazione,'steps':steps})
else:
    exec(open("exploreByRelated.py").read(),{'account':list(accountList.values())[account-1],'tempo_osservazione':tempo_osservazione,'steps':steps})'''