# Bali 

The unobtrusive Battery Life monitor

## Introduction  
Bali is a lightweight program designed to alert you when your battery level goes
down. Minimal Linux installations often lack a mechanism to alert the user when
the system's battery level goes down. Yes, you can install a panel with a battery
widget. But it can steal some of your screen real estate and creates one more
guage for you to look on. Bali is designed to address this issue. It is designed
to be as unobtrusive as possbile. It uses libnotify to present battery value as
notifications only when required.

## Usage  
bali [options]  

    -h  --help      displays short help screen  
    -d  --daemon    runs Bali in daemon mode (default mode)  
    -n  --nogui     prints the battery status to stdout  

## Requirements  
* A notification daemon compatible with libnotify (dunst)
* libnotify
* cron

## Configuration
Bali can be configured by editing the configuration file at ~/.config/bali.conf  

    notification=30     set battery level notification at 30%
    notification=20     any number of notifications can be present  
    low_warning=10      shows battery low warning at 10%
    critical_warning=5  shows critical battery warning at 5%
    check_interval=1    check battery value every 1 minute
