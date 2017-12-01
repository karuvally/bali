#!/usr/bin/env python3
# bali, the battery life monitor (alpha release)
# Released under GNU General Public License

# TODO
# constant notification and beep when battery below 5%
# automatically shutdown or sleep system when critical battery
# coloured notifications
# installation script
# multi battery support
# to cron or not to cron
# also show battery status (charging/discharging/unknown)

# import the serious stuff
import argparse
import subprocess
import os


# read and process configuration
def read_configuration_file(configuration_file_path):
	# essential variables
	configuration_dictionary = {}
	notification_list = []

	# read file and generate dictionary
	configuration_file = open(configuration_file_path, 'r')
	for line in configuration_file:
		if line[0] == '#' or not line.strip():
			continue
		else:
			configuration = line.strip().split('=')
			if configuration[0] == 'notification':
				notification_list.append(int(configuration[1]))
				configuration_dictionary['notifications'] = notification_list
			else:
				configuration_dictionary[configuration[0]] = int(configuration[1])

	# close file and return data
	configuration_file.close()
	return configuration_dictionary


# check the battery, issue warnings
def check_battery(configuration, daemon=True, no_gui=False):
	# open the battery file
	battery_file = open('/sys/class/power_supply/BAT0/capacity')
	battery_value = battery_file.read().rstrip()
	
	# show battery if run in non-daemon mode
	if daemon == False:
		if no_gui == True:
			print('Battery is at ' + battery_value + '%')
			return
		subprocess.run(['notify-send', 'Battery is at ' + battery_value + '%'])
		return
		
	# show user defined notification
	for notification_level in configuration['notifications']:
		if notification_level == battery_value:
			subprocess.run(['notify-send', 'Battery is at ' + battery_value +
				'%'])
			return
	
	# low battery alert
	if int(battery_value) < configuration['low_warning']:
		subprocess.run(['notify-send', 'Battery low! (at ' +
			battery_value + '%)'])
		return

	# critical battery alert
	if int(battery_value) < configuration['critical_warning']:
		subprocess.run(['notify-send', 'Battery critical! (at ' +
			battery_value + '%)'])
	
	return	

# the main function
def main():
	# read configuration data
	user = os.getlogin()
	configuration_dictionary = read_configuration_file('/home/' + user +
		'/.config/bali.conf')
	
	# process command line arguments
	parser = argparse.ArgumentParser(
		description='The Battery Life monitor, alpha release')
	
	parser.add_argument('-d', '--daemon', action='store_true',
		help = 'start in daemon mode')
	
	parser.add_argument('-n', '--nogui', action='store_true',
		help = 'start in non-gui mode')
	
	arguments = parser.parse_args()
	
	# loop only if started in daemon mode
	if arguments.daemon:
		while True:
			check_battery(configuration=configuration_dictionary, daemon=True)
			time.sleep(configuration_dictionary['check_interval'])
	else:
		check_battery(configuration=configuration_dictionary, daemon=False,
			no_gui=arguments.nogui)

main()
