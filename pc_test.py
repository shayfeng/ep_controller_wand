# -*- encoding:utf-8 -*-
#!/usr/bin/env python3

''' 
// =============================================================================
// 程序基本说明（保持不变）
// =============================================================================
'''	

import sys
import os
import argparse
import time
import struct
from port_manager import *
from yis_std_dec import *
import robomaster
from robomaster import robot
from robomaster import led

# 全局解码结果变量
yis_out = {'tid':1, 'roll':0.0, 'pitch':0.0, 'yaw':0.0, \
			'q0':1.0, 'q1':1.0, 'q2':0.0, 'q3':0.0, \
			'sensor_temp':25.0, 'acc_x':0.0, 'acc_y':0.0, 'acc_z':1.0, \
			'gyro_x':0.0, 'gyro_y':0.0, 'gyro_z':0.0,	\
			'norm_mag_x':0.0, 'norm_mag_y':0.0, 'norm_mag_z':0.0,	\
			'raw_mag_x':0.0, 'raw_mag_y':0.0, 'raw_mag_z':0.0,	\
			'lat':0.0, 'longt':0.0, 'alt':0.0,	\
			'vel_e':0.0, 'vel_n':0.0, 'vel_u':0.0, \
			'ms':0, 'year': 2022, 'month':8, 'day': 31, \
			'hour':12, 'minute':0, 'second':0,	\
			'smp_timestamp':0, 'ready_timestamp':0 ,'status':0
			}

# 全局解析缓冲区
dec_buf = bytearray()
			
def check_version():
    '''检查Python版本≥3.8'''
    print("Current Python version is {}.{}.{}.".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    if sys.version_info < (3, 8):
        print("Required Python 3.8 or higher.")
        sys.exit(1)

def check_port_name(port):
	'''检查串口名称合法性'''
	if 'posix' == os.name:
		if -1 == port.find("/dev/tty"):
			print('port name error')
	elif 'nt' == os.name:
		if -1 == port.find("COM"):
			print('port name error')
	else:
		print('unknown os')
	
def main_func(port, baudrate, dbg_flg):
	'''YESENSE Python Decoder Version V2.0.0'''
	global dec_buf
	
	check_version()
	if dbg_flg:
		print(port)
		print(baudrate)
	check_port_name(port)
	decoder = std_decoder()
	ser = open_port(port, baudrate)
	
	# ------------------------------
	# 新增：4个连续触发计数器（对应4种打印场景）
	# ------------------------------
	count_111 = 0  # 统计连续打印"111"的次数
	count_112 = 0  # 统计连续打印"112"的次数
	count_221 = 0  # 统计连续打印"221"的次数
	count_222 = 0  # 统计连续打印"222"的次数
	count_000 = 0
	while True:
		# ep_led = ep_robot.led
		
		data = rd_data(ser)
		num = len(data)
		if(num > 0):
			dec_buf.extend(bytearray(data))	
			if dbg_flg:
				print(f'rd len {num}, total len {len(dec_buf)}')
				decoder.hex_show(dec_buf, len(dec_buf))
				
		if len(dec_buf) > 0:
			ret = decoder.proc_data(dec_buf, len(dec_buf), yis_out, dbg_flg)
			if True == ret:
				''' 处理加速度触发条件 '''
				# 1. acc_x > 5：打印111，计数器累加，满8次输出blue
				if yis_out['acc_x'] > 5:
					print("111")
					count_111 += 1
					if count_111 == 8:
						print("blue")
						# ep_led.set_led(comp='all', r=0, g=0, b=255, effect='on', freq=1)
						count_111 = 0  # 重置计数器，准备下一次连续触发
				# 2. acc_x < -5：打印112，计数器累加，满8次输出red
				elif yis_out['acc_x'] < -5:
					print("112")
					count_112 += 1
					if count_112 == 8:
						print("red")
						# ep_led.set_led(comp='all', r=255, g=0, b=0, effect='on', freq=1)
						count_112 = 0
				# 3. acc_y > 5：打印221，计数器累加，满8次输出green
				if yis_out['acc_y'] > 5:
					print("221")
					count_221 += 1
					if count_221 == 8:
						print("green")
						# ep_led.set_led(comp='all', r=0, g=255, b=0, effect='on', freq=1)
						count_221 = 0
				# 4. acc_y < -5：打印222，计数器累加，满8次输出yellow
				elif yis_out['acc_y'] < -5:
					print("222")
					count_222 += 1
					if count_222 == 8:
						print("yellow")
						# ep_led.set_led(comp='all', r=200, g=100, b=0, effect='on', freq=1)
						count_222 = 0
				if yis_out['acc_z'] > 10:
					print("000")
					count_000 += 1
					if count_000 == 8:
						print("white")
						# ep_led.set_led(comp='all', r=255, g=255, b=255, effect='on', freq=1)
						count_000 = 0
				''' 原四元数打印逻辑（保持注释或按需启用） '''
				# if yis_out['acc_x'] > 5:
				#     print("111")
				# elif yis_out['acc_x'] < -5:
				#     print("112")
				# if yis_out['acc_y'] > 5:
				#     print("221")
				# elif yis_out['acc_y'] < -5:
				#     print("222")
				# if yis_out['acc_z'] > 10:
				#     print("331")
				# elif yis_out['acc_z'] < 5:
				#     print("332")
				
			# ------------------------------
			# 可选：保留原四元数打印逻辑（按需启用）
			# ------------------------------
			# if yis_out['acc_x'] > 5:
			#     print("111")
			# elif yis_out['acc_x'] < -5:
			#     print("112")
			# if yis_out['acc_y'] > 5:
			#     print("221")
			# elif yis_out['acc_y'] < -5:
			#     print("222")
			# if yis_out['acc_z'] > 10:
			#     print("331")
			# elif yis_out['acc_z'] < 5:
			#     print("332")
			
		time.sleep(0.001)  

	close_port(ser)
	
# ------------------------------
# 程序入口（保持不变）
# ------------------------------
if __name__ == '__main__':
	parse = argparse.ArgumentParser(description='YESENSE python decoder!')
	parse.add_argument('--port', type=str, required=True, help='The name of serial port to be connected (e.g., COM3 or /dev/ttyUSB0)')
	parse.add_argument('--bps', type=int, default=460800, help='The baud rate for the serial connection (default: 460800)')	
	parse.add_argument('--dbg', action='store_true' , help='Enable logging for debugging  --dbg ')		
	args = parse.parse_args()
	# ep_robot = robot.Robot()
	# ep_robot.initialize(conn_type="ap")
	main_func(args.port, args.bps, args.dbg)
	


	time.sleep(5)
	# ep_robot.close()