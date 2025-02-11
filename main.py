from text import root
from datetime import datetime
import time
# # from developer2 import Developer
# root.mainloop()
# # Developer.mainloop()


print(datetime.now().strftime("%Y%m%d%H%M%S"))
print(datetime.now().strftime("%Y%m%d%H%M%S"))
print(str(time.time()).split('.'))
ti = ""
for i in str(time.time()).split('.'):
    ti += i
print(ti)
print(time.time())
time.sleep(0.01)
print(time.time())  