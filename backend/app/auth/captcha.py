import time

send_records = {}

def can_send(target:str):
    now=time.time()
    last=send_records.get(target,0)
    return now-last >= 60

def record_send(target:str):
    send_records[target]=time.time()
