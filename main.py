from control import AMR_APi
import random,string
from threading import Thread
import time

task = ["LM1", "LM2"]

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def run_process():
    while True:
        amr.navigation({
                        "id": task[1],
                        "operation": "WaitDI",
                        "source_id": "SELF_POSITION",
                        "task_id": id_generator(9),
                        "args": {
                            "DI": [
                            {
                                "id": 1,
                                "status": True
                            }
                            ],
                        }
                        }
                        )
        while (amr.check_target(amr.data_Status,target= task[1]) == False):
            pass
        
        amr.navigation({
                        "id": task[0],
                        "source_id": "SELF_POSITION",
                        "task_id": id_generator(9)}
                        )
        while (amr.check_target(amr.data_Status,target= task[0]) == False):
            pass
def Poll_status():
    while True:
        amr.status(key=amr.keys)
        time.sleep(1)
   

if __name__ == "__main__":

    amr = AMR_APi(host="192.168.1.99")
    
    amr.connect_config()
    amr.connect_status()
    amr.connect_navigation()
    amr.connect_control()
    amr.connect_other()
    amr.confirm_local()

    
    task_run = Thread(target=run_process,args=())
    task_status = Thread(target=Poll_status,args=())
    
    task_run.start()
    task_status.start()
     