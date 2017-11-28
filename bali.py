#!/usr/bin/env python3
# bali, the battery life monitor (alpha release)
# Released under GNU General Public License

# TODO
# notification for each 5% drop from user confiurable point
# constant notification and beep when battery below 5%
# automatically shutdown or sleep system when critical battery
# configuratoin file with sane defaults
# readme file

# import the serious stuff
import argparse
import subprocess


# check the battery, issue warnings
def check_battery(daemon=True, no_gui=False):
	# open the battery file
	battery_file = open('/sys/class/power_supply/BAT0/capacity')
	battery_value = battery_file.read().rstrip()
	
	# show battery if run in non-daemon mode
	if daemon == False:
		if no_gui == True:
			print('Battery is at ' + battery_value + '%')
			return
		subprocess.run(['notify-send', 'Battery is at ' + battery_value + '%'])
	
	# if battery value is below 10 percent, alert
	if int(battery_value) < 10:
		subprocess.run(['notify-send', 'Battery low! (at ' +
			battery_value + '%)'])
	
	return
		

# the main function
def main():
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
			check_battery(daemon=True)
			time.sleep(60)
	else:
		check_battery(daemon=False, no_gui=arguments.nogui)

main()
