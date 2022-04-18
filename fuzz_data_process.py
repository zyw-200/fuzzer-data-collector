import os
import re
import time
import sys
import matplotlib.pyplot as plt  
from matplotlib.ticker import MultipleLocator, FormatStrFormatter  
import numpy as np


def get_user(image_id, round_time):
	file_dir = "long_run/user/%d/%d/" %(image_id, round_time)
	file = "%s/plot_data" %file_dir
	return crash_extract(file)
	
def get_full(image_id, round_time):
	file_dir = "long_run/full/%d/%d/" %(image_id, round_time)
	file = "%s/plot_data" %file_dir
	return crash_extract(file)

def get_firm(image_id, round_time):
	file_dir = "long_run/firm/%d/%d/" %(image_id, round_time)
	file = "%s/plot_data" %file_dir
	return crash_extract(file)

def get_user_path(image_id, round_time):
	file_dir = "long_run/user/%d/%d/" %(image_id, round_time)
	file = "%s/plot_data" %file_dir
	return path_extract(file)
	
def get_full_path(image_id, round_time):
	file_dir = "long_run/full/%d/%d/" %(image_id, round_time)
	file = "%s/plot_data" %file_dir
	return path_extract(file)

def get_firm_path(image_id, round_time):
	file_dir = "long_run/firm/%d/%d/" %(image_id, round_time)
	file = "%s/plot_data" %file_dir
	return path_extract(file)


def crash_extract(file_name):
	data_file = open(file_name, "r")
	time_list = []
	crash_list = []
	data_file.readline()
	first_row = data_file.readline()
	strstr = first_row.split(",")
	try:
		start_time = int(strstr[0])
	except:
		print("????????????????????????????????????????", file_name)
	time_list.append(0)
	crash_list.append(0)
	last_crash = 0
	for line in data_file.readlines():
		strstr = line.split(",")
		time  = int(strstr[0])
		crash_num = int(strstr[7])
		#past_time = float(time - start_time)/3600
		past_time = time - start_time
		if past_time > 24*3600:
		#if past_time > 24:
			#time_list.append(24)
			time_list.append(86400)
			crash_list.append(last_crash)
			break
		if crash_num > last_crash:
			time_list.append(past_time)
			crash_list.append(last_crash)
		time_list.append(past_time)
		crash_list.append(crash_num)
		last_crash = crash_num
	data_file.close()
	return time_list, crash_list

def path_extract(file_name):
	data_file = open(file_name, "r")
	time_list = []
	crash_list = []
	data_file.readline()
	first_row = data_file.readline()
	strstr = first_row.split(",")
	try:
		start_time = int(strstr[0])
	except:
		print("????????????????????????????????????????", file_name)
	time_list.append(0)
	crash_list.append(0)
	last_crash = 0
	for line in data_file.readlines():
		strstr = line.split(",")
		time  = int(strstr[0])
		crash_num = int(strstr[3])
		#past_time = float(time - start_time)/3600
		past_time = time - start_time
		if past_time > 24*3600:
		#if past_time > 24:
			#time_list.append(24)
			time_list.append(86400)
			crash_list.append(last_crash)
			break
		if crash_num > last_crash:
			time_list.append(past_time)
			crash_list.append(last_crash)
		time_list.append(past_time)
		crash_list.append(crash_num)
		last_crash = crash_num
	data_file.close()
	return time_list, crash_list

def normoalize(time_list, crash_list):
	time_index = 0
	last_crash = 0
	normal_crash_list = []
	for i in range(0, 24 * 50, 1):
		real_time = float(i)/50
		if real_time < time_list[time_index]:
			normal_crash_list.append(last_crash)
			continue
		last_crash = crash_list[time_index]
		normal_crash_list.append(last_crash)
		time_index = time_index + 1
	return normal_crash_list


'''
def cal_ave(image_id, type, id_range):

	for round in range(1, id_range + 1):	
		time_list, crash_list = get_user(image_id, round)
'''

def cal_list_ave(time_list):
	ave_time = 0
	for time in time_list:
		ave_time = ave_time + time
	ave_time = float(ave_time) / len(time_list)
	return ave_time	

def cal_list_mid(time_list):
	time_list = sorted(time_list)
	return time_list[1]

def normalize(crash_list):
	new_crash_list = []
	for crash in crash_list:
		if crash > 1:
			new_crash_list.append(1)
		else:
			new_crash_list.append(crash)
	return new_crash_list

def plot_normal(image_id, round_time, count, httpd_list):
	plt.subplot(3, 2, count)
	plt.grid(linestyle="--") 
	ax=plt.gca()
	yminorLocator  = MultipleLocator(1)
	xminorLocator  = MultipleLocator(1)
	ax.yaxis.set_minor_locator(yminorLocator)
	ax.xaxis.set_minor_locator(xminorLocator)
	y_max = 0 
	for round in range(1, 4):	
		real_round = round
		time_list, crash_list = get_user(image_id, real_round)
		if time_list[-1] < 24:
			time_list.append(24)
			last_crash  = crash_list[-1]
			crash_list.append(last_crash)
		crash_list_normal = normoalize(time_list, crash_list)

		full_time_list, full_crash_list = get_full(image_id,real_round)
		if full_time_list[-1] < 24:
			full_time_list.append(24)
			last_crash  = full_crash_list[-1]
			full_crash_list.append(last_crash)
		full_crash_list_normal = normoalize(full_time_list, full_crash_list)

		firm_time_list, firm_crash_list = get_firm(image_id,real_round)
	
		if firm_time_list[-1] < 24:
			firm_time_list.append(24)
			last_crash  = firm_crash_list[-1]
			firm_crash_list.append(last_crash)
		firm_crash_list_normal = normoalize(firm_time_list, firm_crash_list)

		x = []
		for i in range(0, 24 * 50, 1):
			x.append(float(i)/50)
		'''
		if round!= 3: #show label
			l1=plt.plot(x,crash_list_normal, marker=".", markersize=5, markevery=15, color="red")
			l2=plt.plot(x, full_crash_list_normal, marker='>',  markersize=5, markevery=15, color="blue")
			l3=plt.plot(x,firm_crash_list_normal,marker='>',color="green", markersize=5, markevery=15)
		else:
			l1=plt.plot(x,crash_list_normal,marker=".", color="red", markersize=5, markevery=15, label='EQUAFL')
			l2=plt.plot(x,full_crash_list_normal,marker='>',color="blue", markersize=5, markevery=15, label='Full')
			l3=plt.plot(x,firm_crash_list_normal,marker='>',color="green", markersize=5, markevery=15, label='Firm-AFL')
		'''
		if round!= 3: #show label
			l1=plt.plot(x,crash_list_normal, "r-")
			l3=plt.plot(x,firm_crash_list_normal, 'g-.' )
			l2=plt.plot(x, full_crash_list_normal, 'b--')
		else:
			l1=plt.plot(x,crash_list_normal, 'r-', label='EQUAFL')
			l3=plt.plot(x,firm_crash_list_normal, 'g-.', label='Firm-AFL')
			l2=plt.plot(x,full_crash_list_normal, 'b--', label='Full')

		if y_max < crash_list[-1]:
			y_max = crash_list[-1]
		if y_max < full_crash_list[-1]:
			y_max = full_crash_list[-1]
		if y_max < firm_crash_list[-1]:
			y_max = firm_crash_list[-1]
		plt.ylim(-1, y_max+1)
		plt.xlim(-1, 25)
		time_tick = np.array([0,4,8,12,16,20,24])
		plt.xticks(time_tick,time_tick,fontsize=12)#,fontweight='bold')
		if y_max/5!=0:
			crash_tick = np.arange(0, y_max + y_max%5, y_max/5)
		else:
			crash_tick = [1, 2, 3, 4]
		plt.yticks(crash_tick, crash_tick, fontsize=12)

		#else:
			#plt.plot([], [])
	plt.title(httpd_list[count-1], fontsize = 14)
	plt.xlabel('Time (hours)', fontsize = 13)
	plt.ylabel('Crashes found', fontsize =13)
	plt.legend()

def time_to_first_crash(time_list, crash_list):
	for i in range(0, len(time_list)):
		if crash_list[i] > 0:
			return time_list[i]
	return 24

def time_to_first_vul(time_list, crash_list, round, order):
	fp = open("19061_unique_vul")
	lines = fp.readlines()
	line = lines[round]
	pos = line.split(";")
	new_pos = []
	for p in pos:
		new_pos.append(int(p))
	if order >= len(new_pos):
		print("order", order, new_pos)
		return 24*3600
	uni_crash = new_pos[order]
	for i in range(0, len(time_list)):
		if crash_list[i] >= uni_crash:
			return time_list[i]
	return 24*3600


	


def raw_data_output(time_list, crash_list, output_file):
	fp = open(output_file, "w+")
	for i in range(0, len(time_list)):
		fp.write(str(time_list[i])+":"+str(crash_list[i])+"\n")
	fp.close()

def extract_unique_bug(crash_list, round):
	new_crash_list = []
	fp = open("19061_unique_vul_ordered")
	lines = fp.readlines()
	line = lines[round]
	pos = line.split(";")
	pos_len = len(pos)
	index = 0 # unique bug = index + 1
	for i in range(0, len(crash_list)):
		if index == pos_len:
			new_crash_list.append(index)
			continue
		while(crash_list[i] >  int(pos[index])):
			if index + 1 == pos_len:
				break
			elif crash_list[i] >= int(pos[index + 1]):
				index = index + 1
			else:
				break
		if crash_list[i] >= int(pos[index]):
			new_crash_list.append(index+1)
			index=index+1
		else:
			new_crash_list.append(index)
	return new_crash_list


def fuzz_data_process(image_id, round_time, count, httpd_list):
	plt.subplot(3, 2, count)
	plt.grid(linestyle="--") 
	ax=plt.gca()
	yminorLocator  = MultipleLocator(1)
	xminorLocator  = MultipleLocator(1)
	ax.yaxis.set_minor_locator(yminorLocator)
	ax.xaxis.set_minor_locator(xminorLocator)
	firm_time = []
	user_time = []
	full_time = []
	vul_time = {}
	vul_full_time = {}
	y_max = 0 
	raw_data_dir = "raw_fuzz/" + str(image_id) +"/"
	if os.path.exists(raw_data_dir) == False:
		cmdstr = "mkdir -p %s" %raw_data_dir
		os.system(cmdstr)
	for round in range(1, 6):	

		real_round = round
		time_list, crash_list = get_user(image_id, real_round)

		if image_id != 19061:
			crash_list = normalize(crash_list)
		else:
			vul_list = extract_unique_bug(crash_list, round)
		if time_list[-1] < 24*3600:
			time_list.append(24*3600)
			last_crash  = crash_list[-1]
			crash_list.append(last_crash)
		print(round, time_to_first_crash(time_list, crash_list))
		user_time.append(time_to_first_crash(time_list, crash_list))

		if image_id == 19061:
			for order in range(0,4):
				cra_time = time_to_first_vul(time_list, crash_list, round, order)
				if order not in vul_time:
					vul_time[order] = []
				vul_time[order].append(cra_time)

		output_file = raw_data_dir + "equafl" + str(round)
		if image_id != 19061:
			raw_data_output(time_list, crash_list, output_file)
		else:
			raw_data_output(time_list, vul_list, output_file)


		firm_time_list, firm_crash_list = get_firm(image_id,real_round)
		'''
		if image_id == 108076:
			firm_crash_list = normalize(firm_crash_list)
		'''
		if image_id !=19061:
			firm_crash_list = normalize(firm_crash_list)

		if firm_time_list[-1] < 24*3600:
			firm_time_list.append(24*3600)
			last_crash  = firm_crash_list[-1]
			firm_crash_list.append(last_crash)

		output_file = raw_data_dir + "firmafl" + str(round)
		raw_data_output(firm_time_list, firm_crash_list, output_file)

		full_time_list, full_crash_list = get_full(image_id,real_round)
		'''
		if image_id == 108076:
			full_crash_list = normalize(full_crash_list)
		'''
		if image_id != 19061:
			full_crash_list = normalize(full_crash_list)

		if full_time_list[-1] < 24*3600:
			full_time_list.append(24*3600)
			last_crash  = full_crash_list[-1]
			full_crash_list.append(last_crash)
		full_time.append(time_to_first_crash(full_time_list, full_crash_list))

		if image_id == 19061:
			for order in range(0,4):
				cra_time = time_to_first_vul(full_time_list, full_crash_list, round, order)
				if order not in vul_full_time:
					vul_full_time[order] = []
				vul_full_time[order].append(cra_time)

		output_file = raw_data_dir + "full" + str(round)
		raw_data_output(full_time_list, full_crash_list, output_file)

	if image_id == 19061:
		for order in range(0,4):
			print vul_time[order]
			ave_time = cal_list_ave(vul_time[order])
			ave_full_time = cal_list_ave(vul_full_time[order])
			print("time to first vul", order, ave_time)
			print("full time to first vul", order, ave_full_time)


def fuzz_data_process_path(image_id, round_time, count, httpd_list):
	plt.subplot(3, 2, count)
	plt.grid(linestyle="--") 
	ax=plt.gca()
	yminorLocator  = MultipleLocator(1)
	xminorLocator  = MultipleLocator(1)
	ax.yaxis.set_minor_locator(yminorLocator)
	ax.xaxis.set_minor_locator(xminorLocator)
	firm_time = []
	user_time = []
	full_time = []
	y_max = 0 
	raw_data_dir = "raw_fuzz_path/" + str(image_id) +"/"
	if os.path.exists(raw_data_dir) == False:
		cmdstr = "mkdir -p %s" %raw_data_dir
		os.system(cmdstr)
	for round in range(1, 6):	

		real_round = round
		time_list, crash_list = get_user_path(image_id, real_round)
		if time_list[-1] < 24:
			time_list.append(24)
			last_crash  = crash_list[-1]
			crash_list.append(last_crash)
		print(round, time_to_first_crash(time_list, crash_list))
		user_time.append(time_to_first_crash(time_list, crash_list))

		output_file = raw_data_dir + "equafl" + str(round)
		raw_data_output(time_list, crash_list, output_file)


		firm_time_list, firm_crash_list = get_firm_path(image_id,real_round)
		if firm_time_list[-1] < 24:
			firm_time_list.append(24)
			last_crash  = firm_crash_list[-1]
			firm_crash_list.append(last_crash)

		output_file = raw_data_dir + "firmafl" + str(round)
		raw_data_output(firm_time_list, firm_crash_list, output_file)

		full_time_list, full_crash_list = get_full_path(image_id,real_round)
		if full_time_list[-1] < 24:
			full_time_list.append(24)
			last_crash  = full_crash_list[-1]
			full_crash_list.append(last_crash)
		full_time.append(time_to_first_crash(full_time_list, full_crash_list))

		output_file = raw_data_dir + "full" + str(round)
		raw_data_output(full_time_list, full_crash_list, output_file)


	


image_list = [16157, 108076, 20880, 16385, 18627, 19061]
httpd_list = ["/bin/boa (WN2000RPTv1)", "/usr/sbin/uhttpd (WNDRMACv2)", "/sbin/httpd (DIR-825)", "/usr/bin/lighttpd (DSP-W215)", "/userfs/bin/boa (DSL-2740R)", "/sbin/httpd (DAP-2330)"]

count = 1
for image_id in image_list:
	fuzz_data_process(image_id, 0, count, httpd_list)
	#fuzz_data_process_path(image_id, 0, count, httpd_list)
