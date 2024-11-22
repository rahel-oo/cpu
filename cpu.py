import threading
import time

# INDEX_OF_OTHER_PROCESS_ADR
#          |
#          | PROCESS_ID_ADR                                                                              IRET_DESTINATION_ADR
#          | |                                                                                                     |
#          v v                                                                                                     v
storage = [8,0,"NOP","NOP","NOP","NOP", "JMP", 2, "NOP", "NOP", "NOP", "NOP", "NOP", "JMP", 8,"ISR", "TGL", "IRET",0]
ir = False
index = 2

# TODO: allow IRET_DESTINATION to be at different places
IRET_DESTINATION_ADR=len(storage)-1
PROCESS_ID_ADR=1
INDEX_OF_OTHER_PROCESS_ADR=0

def execute():
    global index
    global ir
    while True:
        if ir: 
            storage[IRET_DESTINATION_ADR]=storage[INDEX_OF_OTHER_PROCESS_ADR]
            storage[INDEX_OF_OTHER_PROCESS_ADR]=index
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
    if storage[PROCESS_ID_ADR]==0:
        storage[PROCESS_ID_ADR]=1
    else: 
        storage[PROCESS_ID_ADR]=0 
    print("TGL: toggle process") 
    index +=1
    
def executeIRET():
    global index
    global ir
    index = storage[IRET_DESTINATION_ADR]
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
