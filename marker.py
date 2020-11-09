#!/usr/bin/env python3
from __future__ import print_function
from transliterate import translit, get_available_language_codes
import requests
import time
import os
import sys
import json

RED = "\033[31m"
GRN = "\033[32m"
ORG = "\033[33m"
YEL = "\033[93m"
BLD = "\033[1m"
RES = "\033[0m"
CONN = [RED, RED, ORG, YEL, GRN]
while True:
	r = requests.get("https://dnevnik.mos.ru/reports/api/progress/json?academic_year_id=8&student_profile_id=<ID>", headers = {
		"Content-Type": "application/json",
		"Accept": "*/*",
		"Accept-Language": "ru",
		"Accept-Encoding": "gzip, deflate, br",
		"Host": "dnevnik.mos.ru",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
		"Connection": "keep-alive",
		"Referer": "https://dnevnik.mos.ru/diary/diary/marks",
		"Cookie": "<COOKIE>",
		"Auth-Token": "<TOKEN>",
		"Profile-Type": "student",
		"Profile-Id": "<ID>"
	})
	resp_json = r.json()
	if r.status_code != 200:
		if '-v' in sys.argv:
			print(f'{RED + BLD}ERROR:{RES} Got {r.status_code} response code')
		else:
			os.system('sudo telegrambotreport [MARKER]: Error with response code ' + r.status_code)
		exit(-1)
	if '-i' in sys.argv:
		open('/bin/marker_data/marker_cache.json', "w").write(r.text)
		exit(0)
	if '-v' in sys.argv:
		for i in resp_json:
			print(f'{BLD}{i["subject_name"]}{RES} [{i["avg_five"]}]: ', end = "")
			for j in i["periods"]:
				for k in j["marks"]:
					val = int(k["values"][0]["five"])
					if k["weight"] != 1:
						print(BLD, end = "")
					print(f'{CONN[val - 1]}{val}{RES}', end = "")
					if k["weight"] == 2:
						print("₂", end = "")
					elif k["weight"] == 3:
						print("₃", end = "")
					print(', ', end = "")
			print()
		exit(0)
	else:
		with open('/bin/marker_data/marker_cache.json', 'r') as read_file:
			cache_json = json.load(read_file)
#		with open('/bin/marker_data/marker_cache2.json', 'r') as read_file:
#			resp_json = json.load(read_file)

		for i in range(len(cache_json)):
			marks = []
			for j in cache_json[i]["periods"]:
				for k in j["marks"]:
					marks.append(k["values"][0]["original"])
			markss = []
			for j in resp_json[i]["periods"]:
				for k in j["marks"]:
					markss.append(k["values"][0]["original"])
			a = len(markss)
			b = a - len(marks)
			for j in range(b):
				os.system(f'report New mark: {translit((cache_json[i]["subject_name"]), "ru", reversed = True)}, {markss[a - b]}')
		open('marker_cache.json', "w").write(r.text)
		time.sleep(180)
