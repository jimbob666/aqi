#!/usr/bin/env python
# coding=utf-8
# "DATASHEET": http://cl.ly/ekot
# https://gist.github.com/kadamski/92653913a53baf9dd1a8
from __future__ import print_function

## NEW: Added requests + github_token and iftt_key. Need to create "config.py to store token and key values. 
#OLD Ver import serial, struct, sys, time, json
import serial, struct, sys, time, json, requests
from config import github_token, iftt_key


## NEW:
timestamp = time.strftime("%m.%d.%Y %H:%M:%S")
#print (timestamp)
print("Start Script on " + timestamp) 


## NEW: pip install pygithub
import base64
from github import Github
from github import InputGitTreeElement

## NEW: Setup Google Doc Auth
import gspread
from oauth2client.service_account import ServiceAccountCredentials

## NEW: use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('AQI-RPI-Secret.json', scope)
client = gspread.authorize(creds)


## NEW: Get External IP Adress
import urllib
import re

## NEW: Get External IP Adress
def get_external_ip():
	site = urllib.urlopen("http://checkip.dyndns.org/").read()
	grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
	address = grab[0]
	return address

if __name__ == '__main__':
	external_ip = (get_external_ip())
	print("External IP:", external_ip)


## NEW: Get Internal IP Adress
import socket
def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
        internal_ip = (get_internal_ip())
        print("Internal IP:", internal_ip)




DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1
TRIGGER_THRESHOLD_PM10 = 10
TRIGGER_THRESHOLD_PM25 = 10


ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 9600

ser.open()
ser.flushInput()

byte, data = 0, ""

def dump(d, prefix=''):
    print(prefix + ' '.join(x.encode('hex') for x in d))

def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret

def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    return [pm25, pm10]
    #print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))

def process_version(d):
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(ord(v) for v in d[2:8])%256
    print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]), "OK" if (checksum==r[4] and r[5]==0xab) else "NOK"))

def read_response():
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)

    d = ser.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d

def cmd_set_mode(mode=MODE_QUERY):
    ser.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()

def cmd_query_data():
    ser.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    values = []
    if d[1] == "\xc0":
        values = process_data(d)
    return values

def cmd_set_sleep(sleep=1):
    mode = 0 if sleep else 1
    ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()

def cmd_set_working_period(period):
    ser.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()

def cmd_firmware_ver():
    ser.write(construct_command(CMD_FIRMWARE))
    d = read_response()
    process_version(d)

def cmd_set_id(id):
    id_h = (id>>8) % 256
    id_l = id % 256
    ser.write(construct_command(CMD_DEVICE_ID, [0]*10+[id_l, id_h]))
    read_response()

print("\nReading API Sensor")

if __name__ == "__main__":
    while True:
        cmd_set_sleep(0)
        cmd_set_mode(1);
        for t in range(15):
            values = cmd_query_data();
            if values is not None:
	        try:
			print("PM2.5: ", values[0], ", PM10: ", values[1])
			time.sleep(2)
		except IndexError:
			print("There was an IndexRange error")
			__name__ = ""

	timestamp = time.strftime("%m.%d.%Y %H:%M:%S")

        # open stored data
	with open('/var/www/html/aqi/aqi.json') as json_data:
		data = json.load(json_data)

        # check if length is more than 100 and delete first element
        if len(data) > 100:
            data.pop(0)

        # append new values
        data.append({'pm25': values[0], 'pm10': values[1], 'time': timestamp})
        # Use for debugging if Google Doc does not work data.append({'pm25': values[0], 'pm10': values[1], 'time': time.strftime("%m.%d.%Y %H:%M:%S"), 'ext_ip': external_ip, 'int_ip': internal_ip})

        # save it
        with open('/var/www/html/aqi/aqi.json', 'w') as outfile:
            json.dump(data, outfile)


	## NEW: Copy aqi.json file to Github https://github.com/jimbob666/aqi

	token = github_token
	g = Github(token)
	repo = g.get_user().get_repo('aqi')
	file_list = [
    		'aqi.json'
	]
	commit_message = 'Add simple regression analysis'
	master_ref = repo.get_git_ref('heads/master')
	master_sha = master_ref.object.sha
	base_tree = repo.get_git_tree(master_sha)
	element_list = list()
	for entry in file_list:
	    	with open(entry, 'rb') as input_file:
			data = input_file.read()
		if entry.endswith('.png'):
			data = base64.b64encode(data)
    		element = InputGitTreeElement(entry, '100644', 'blob', data)
    		element_list.append(element)
	tree = repo.create_git_tree(element_list, base_tree)
	parent = repo.get_git_commit(master_sha)
	commit = repo.create_git_commit(commit_message, tree, [parent])
	master_ref.edit(commit.sha)
	""" An egregious hack to change the PNG contents after the commit """
	for entry in file_list:
    		with open(entry, 'rb') as input_file:
        		data = input_file.read()
    		if entry.endswith('.png'):
        		old_file = repo.get_contents(entry)
        		commit = repo.update_file('/' + entry, 'Update PNG content', data, old_file.sha)


	print("\nCoping aqi.json to GitHub - https://jimbob666.github.io/aqi/")



	## Update Google Doc Section
	## Find a workbook by name and open the first sheet
	sheet = client.open("AQI RPI").sheet1
	row_values = [values[0], values[1], timestamp, external_ip, internal_ip]
	row_number = 2
	result = sheet.insert_row(row_values, row_number)

	print("Updating Google Doc to http://bit.ly/aqi-rpi")




	## NEW: IFTT Section
	IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/aqi/with/key/' + iftt_key

	def post_ifttt_webhook():
		ifttt_event_url = IFTTT_WEBHOOKS_URL.format()
		# Sends a HTTP POST request to the webhook URL
		requests.post(ifttt_event_url)

	pm10_trigger = values[1]

	# Send IFTT notification
	if pm10_trigger > 10:
        	post_ifttt_webhook()
        	print("IFFF Trigger Sent")
	else:
	        print("No IFTT trigger Sent")


        print("Going to sleep for 5min...\n")

        cmd_set_mode(0);
        cmd_set_sleep()
        time.sleep(300)
