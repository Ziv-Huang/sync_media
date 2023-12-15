import time
from IPC import Master, Slave


master = Master()
slave = Slave()

master.register_function()
print("#############################")
time.sleep(2)
slave.register_function()
