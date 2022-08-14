# The MIT License (MIT)

from rotary_irq_rp2 import RotaryIRQ
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
import time, utime

i2c_lcd = I2C(id=1,scl=Pin(27),sda=Pin(26),freq=100000)
lcd = I2cLcd(i2c_lcd, 0x27, 2, 16)

SW = Pin(13,Pin.IN,Pin.PULL_UP)

r = RotaryIRQ(pin_num_clk=14,
              pin_num_dt=15,
              min_val=0,
              max_val=23,
              reverse=True,
              range_mode=RotaryIRQ.RANGE_WRAP)

FILENAME = "horarios.txt"  #The filename to store data in
f = open(FILENAME, "w") #Open the file for writing (to empty it)
f.close() #Close the file

val_old = r.value()
opt = 1

hora = 0
minutos = 0
duracion = 0
lcd.clear()

while True:
    val_new = r.value()
    n = 0
    #hora = 0
    #minutos = 0
    #duracion = 0
    if SW.value() == 0 and n == 0:
        #f = open(FILENAME, "a") #Open the file for appending 
        if opt == 1:
            hora = r.value()
            print("Hora: ",hora)
            r.set(min_val=0, max_val=59)
            n = 1
            opt = 2
            while SW.value() == 0:
                r.reset()
                continue
        elif opt == 2:
            minutos = r.value()
            print("Minutos: ",minutos)
            r.set(min_val=0, max_val=20)
            n = 1
            opt = 3
            while SW.value() == 0:
                r.reset()
                continue
        elif opt == 3:
            duracion = r.value()
            print("Duracion de la alarma ",duracion)
            r.set(min_val=0, max_val=23)
            n = 1
            opt = 1
            fileString = str(hora) + ',' + str(minutos) + ',' + str(duracion)
            fileString = fileString + '\n'  #Add a new line (like pressing ENTER)
            f = open(FILENAME, "a") #Open the file for appending
            f.write(fileString) #Write the data to file
            f.close()
            while SW.value()==0:
                r.reset()
                continue
        #n = 0
        #Build up the string to write
        #fileString = str(hora) + ',' + str(minutos) + ',' + str(duracion)
        #fileString = fileString + '\n'  #Add a new line (like pressing ENTER)
        #f.write(fileString) #Write the data to file
        #f.close()
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
        #lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Time:")
    time.sleep_ms(50)
    