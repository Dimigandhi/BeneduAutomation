import random
import time

oper = random.choice(['plus','minus'])

if(oper == 'plus'):
    time.sleep(5+3)
else:
    time.sleep(5-3)
print("2")

