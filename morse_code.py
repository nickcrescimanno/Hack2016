#!/usr/bin/env python

# morse_code.py
# 2015-06-17
# Public Domain

# ./morse_code.py [ message [ micros [ gpio ] ] ]

import sys
import time

import pigpio

morse={
'a':'.-'   , 'b':'-...' , 'c':'-.-.' , 'd':'-..'  , 'e':'.'    ,
'f':'..-.' , 'g':'--.'  , 'h':'....' , 'i':'..'   , 'j':'.---' ,
'k':'-.-'  , 'l':'.-..' , 'm':'--'   , 'n':'-.'   , 'o':'---'  ,
'p':'.--.' , 'q':'--.-' , 'r':'.-.'  , 's':'...'  , 't':'-'    ,
'u':'..-'  , 'v':'...-' , 'w':'.--'  , 'x':'-..-' , 'y':'-.--' ,
'z':'--..' , '1':'.----', '2':'..---', '3':'...--', '4':'....-',
'5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.',
'0':'-----'}

NONE=0

DASH=3
DOT=1

GAP=1
LETTER_GAP=3-GAP
WORD_GAP=7-LETTER_GAP

text = """Now is the winter of our discontent
made glorious summer by this sun of York"""

if len(sys.argv) > 1:
   text = sys.argv[1]

micros = 20000

if len(sys.argv) > 2:
   micros = int(sys.argv[2])

GPIO=22

if len(sys.argv) > 3:
   GPIO = int(sys.argv[3])

def transmit_string(pi, gpio, message):

   print(message)

   pi.wave_clear() # clear all waveforms

   wf=[]

   for C in message:
      c=C.lower()
      if c in morse:
         k = morse[c]
         for x in k:

            if x == '.':
               wf.append(pigpio.pulse(1<<gpio, NONE, DOT * micros))
            else:
               wf.append(pigpio.pulse(1<<gpio, NONE, DASH * micros))

            wf.append(pigpio.pulse(NONE, 1<<gpio, GAP * micros))

         wf.append(pigpio.pulse(NONE, 1<<gpio, LETTER_GAP * micros))

      elif c == ' ':
         wf.append(pigpio.pulse(NONE, 1<<gpio, WORD_GAP * micros))

   pi.wave_add_generic(wf)

   wid = pi.wave_create()

   if wid >= 0:
      pi.wave_send_once(wid)

pi = pigpio.pi() # connect to local Pi

pi.set_mode(GPIO, pigpio.OUTPUT)

transmit_string(pi, GPIO, text)

while pi.wave_tx_busy():
   time.sleep(0.1)

pi.stop() # disconnect from Pi

