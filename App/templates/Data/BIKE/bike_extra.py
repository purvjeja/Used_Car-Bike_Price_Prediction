import os
import time
check = input('Tell me Your Name? : ')
print('\nToh',check,'suno,\n');
time.sleep(3)
print('maine laptop khulvaya tumhara kyun? toh ab bandh bhi mai hee karwaunga hai na! HaHaHaHa :)');time.sleep(10)
print('\nBabye',check,',You are shutting off in..')
time.sleep(3)
i=3
while(i>0):
    time.sleep(0.6)
    print(i,"\n")
    i=i-1
print(":)")
time.sleep(0.5)
os.system("shutdown /s /t 1")
