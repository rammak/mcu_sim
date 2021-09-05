# LORIS ADCS communication simulator for MSP430
# Author: Rutwij Makwana
# Version: 0.1

import pandas as pd
import numpy as np
import json as js
import sys
import argparse

parser = argparse.ArgumentParser(description = 'LORIS ADCS comm simulator')

parser.add_argument('-f', metavar='file', type=str, help='The pseudoterminal file to be read and written by the simulator.')

args = parser.parse_args()

comm_file = args.f

print("LORIS ADCS MSP430 Comm simulator v0.1")
print("Importing data...")


# data from GPS
r_I = pd.read_excel(io='./r_I_record.xlsx', dtype=np.float64, names=['x', 'y', 'z'], header=None)  # estimated ECI radius
TIME = pd.read_excel(io='./TIME_record.xlsx', dtype=np.float64, names=['key', 'val'], header=None)  # Time
v_I = pd.read_excel(io='./v_I_record.xlsx', dtype=np.float64, names=['x', 'y', 'z'], header=None)  # estimated ECI velocity

# Magnetic sensor data = magSen
bk = pd.read_excel(io='./bk_record.xlsx', dtype=np.float64, names=['x', 'y', 'z'], header=None)

# angular velocity of the satellite = imu
w = pd.read_excel(io='./w_record.xlsx', dtype=np.float64, names=['x', 'y', 'z'], header=None)

# angular velocity of RW = rw_speed
wsi = pd.read_excel(io='./wsi_noise_record.xlsx', dtype=np.float64, names=['x', 'y', 'z'], header=None)

# Sun sensor values = sunSens
y = pd.read_excel(io='./y_record.xlsx', dtype=np.float64, names=['x+1', 'x+2', 'x+3',
                                                               'x-1', 'x-2', 'x-3',
                                                               'y+1', 'y+2', 'y+3',
                                                               'y-1', 'y-2', 'y-3',
                                                               'z+1', 'z+2', 'z+3',
                                                               'z-1', 'z-2', 'z-3'], header=None)


pd.set_option("precision", 3)
pd.set_option("display.max_columns", 999)
# print(TIME.head(1))

itr = 0             # current iteration
MAX_ITR = len(y)    # maximum number of iterations
print("Max iterations/number of records: ", MAX_ITR)
print("####### Iteration: ", itr)


def parse_input(ip: str):
    global itr
    print("Received command: ", ip)
    try:
        j = js.loads(ip)
        if 'fwVersion' in j:
            send_output({'fwVersion': 0.0})
            itr += 1                            # this command also increments the iterator, call once every second
            print("####### Iteration: ", itr)
        elif 'hwVersion' in j:
            send_output({'hwVersion': 0.0})
        elif 'rw_speed' in j:                   # wsi
            if j['rw_speed'] == 'write':
                send_output({'rw_speed': 'set'})
            else:
                send_output({'rw_speed': [wsi['x'][itr], wsi['y'][itr], wsi['z'][itr]]})
        elif 'rw_current' in j:
            send_output({'rw_current': [50, 100, 11]})
        elif 'mqtr_volts' in j:
            if j['mqtr_volts'] == 'write':
                send_output({'mqtr_volts': 'set'})
            else:
                send_output({'mqtr_volts': [10, -20, 30]})
        elif 'sunSen' in j:
            if j['face'] == 'x+':
                send_output({'sunSen': 'x+', 'lux': [y['x+1'][itr], y['x+2'][itr], y['x+3'][itr]]})
            elif j['face'] == 'y+':
                send_output({'sunSen': 'y+', 'lux': [y['y+1'][itr], y['y+2'][itr], y['y+3'][itr]]})
            elif j['face'] == 'z+':
                send_output({'sunSen': 'z+', 'lux': [y['z+1'][itr], y['z+2'][itr], y['z+3'][itr]], 'temp': 1249})
            elif j['face'] == 'x-':
                send_output({'sunSen': 'x-', 'lux': [y['x-1'][itr], y['x-2'][itr], y['x-3'][itr]]})
            elif j['face'] == 'y-':
                send_output({'sunSen': 'y-', 'lux': [y['y-1'][itr], y['y-2'][itr], y['y-3'][itr]]})
            elif j['face'] == 'z-':
                send_output({'sunSen': 'z-', 'lux': [y['y-1'][itr], y['y-2'][itr], y['y-3'][itr]], 'temp': 5555})
        elif 'magSen' in j:
            if j['magSen'] == 'reset':
                send_output({'magSen': 'restarted'})
            else:
                send_output({'magSen': [bk['x'][itr], bk['y'][itr], bk['z'][itr]]})
        elif 'imu' in j:
            if j['imu'] == 'reset':
                send_output({'imu': 'reset complete'})
            else:
                send_output({'imu': [w['x'][itr], w['y'][itr], w['z'][itr]]})
        elif 'current' in j:
            if j['current'] == 'rw':
                send_output({'current': 'rw', 'measured': [25, 15, 71]})
            else:
                send_output({'current': 'mqtr', 'measured': [51, 21, 17]})
        elif 'TIME' in j:          # temporary command
            send_output({'TIME': TIME['val'][itr]})

        elif 'r_I' in j:           # temporary command
            send_output({'r_I': [r_I['x'][itr], r_I['y'][itr], r_I['z'][itr]]})

#{"all": [x+1 sun, x+2 sun, x+3 sun, x-1 sun, x-2 sun, x-3 sun, y+1 sun, y+2 sun, y+3 sun, y-1 sun, y-2 sun, y-3 sun, z+1 sun, z+2 sun, z+3 sun, z-1 sun, z-2 sun, z-3 sun, x mag, y mag, z mag, x rw, y rw, z rw, x imu, y imu, z imu]}

        elif 'v_I' in j:           # temporary command
            send_output({'v_I': [v_I['x'][itr], v_I['y'][itr], v_I['z'][itr]]})
        elif 'all' in j:
            if j['all'] == 'read':
                send_output({'all': [ y['x+1'][itr], y['x+2'][itr], y['x+3'][itr], y['x-1'][itr], y['x-2'][itr], y['x-3'][itr], 
                                        y['y+1'][itr], y['y+2'][itr], y['y+3'][itr], y['y-1'][itr], y['y-2'][itr], y['y-3'][itr],
                                        y['z+1'][itr], y['z+2'][itr], y['z+3'][itr], y['z-1'][itr], y['z-2'][itr], y['z-3'][itr],
                                        bk['x'][itr], bk['y'][itr], bk['z'][itr],
                                        wsi['x'][itr], wsi['y'][itr], wsi['z'][itr],
                                        w['x'][itr], w['y'][itr], w['z'][itr] ]})
                itr += 1
                                        
        else:
            send_output({'error': 'json_unk', 'received': ip})
    except js.JSONDecodeError as e:
        print("JSON parsing error!\n", e)
        send_output({'error': 'json_format', 'received': ip})


def send_output(op: dict):
    o = js.dumps(op)
    print("Sending: ", o)
    with open(comm_file, "w") as f:
        f.write(o + '\n')

#parse_input('{"TIME": "get"}')
#parse_input('{"v_I": "get"}')
#parse_input('{"r_I": "get"}')
#parse_input('{"sunSen": "read", "face":"x+"}')
#parse_input('{"magSen": "read"}')
#parse_input('{"fwVersion": "get"}')

while(True):
    with open(comm_file, "r") as f:
        ip = f.readline()
        print(ip)
        parse_input(ip)
