import threading
import time

storage = [8,0,"NOP","NOP","NOP","NOP", "JMP", 2, "NOP", "NOP", "NOP", "NOP", "NOP", "JMP", 8,"ISR", "TGL", "IRET",0]
ir = False
index = 2

def execute():
    global index
    global ir
    while True:
        if ir: 
            storage[len(storage)-1]=storage[0]
            storage[0]=index
            index = 15
            ir = False

        item = storage[index]
        performAction(item)
        time.sleep(1)

def performAction(item):
    match item:
       case "NOP": executeNOP()
       case "JMP": executeJMP()
       case "TGL": executeTGL()
       case "ISR": executeISR()
       case "IRET": executeIRET()  

def executeNOP():
    global index
    print(f"NOP at position {index} for Process {storage[1]}")
    index += 1

def executeJMP():
    global index
    print(f"JMP to position: {storage[index+1]}")
    index = storage[index+1]

def executeTGL():
    global index
    if storage[1]==0:
        storage[1]=1
    else: 
        storage[1]=0 
    print("TGL: toggle process") 
    index +=1
    
def executeIRET():
    global index
    global ir
    index = storage[index+1]
    print(f"IRET: IR routine done, going to position: {index} of Process {storage[1]}")

def executeISR():
    print("ISR active")
    global index
    index += 1  

def interrupt():
    while True:
        global index
        global ir
        ir = True
        time.sleep(10)

cpu = threading.Thread(target = execute)
isr = threading.Thread(target = interrupt)

cpu.start()
isr.start()

cpu.join()
isr.join()
