import pigpio

pi = pigpio.pi()
print("set mode")
for i in range(26):
    print('pin',i,'mode',pi.get_mode(i))
print("get mode")
for i in range(1,26):
    pi.set_mode(i, pigpio.OUTPUT)

