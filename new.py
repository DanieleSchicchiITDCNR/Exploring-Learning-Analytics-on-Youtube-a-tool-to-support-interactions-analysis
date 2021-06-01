import schedule 

from subprocess import Popen, PIPE
import subprocess

process = Popen(['python','main.py'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
print(stderr)

#schedule.every(2).minutes.do(call_me())
'''while True: 
    try:
        schedule.run_pending()
    except:
        print("terminato con errore")'''