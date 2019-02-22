import yaml
import pickle
from time import sleep

from sonos_alarm.auth import Authentication
from sonos_alarm.alarm import Alarm

def run():
    # read the config files
    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file)
    authentication = Authentication(config["client_pub_key"],
                                    config["client_priv_key"],
                                    config["redirect_uri"])

    # TODO: Add the ability to create a new token
    # read, renew, and rewrite the token
    with open('token.yaml', 'r') as token_file:
        authentication.token = yaml.load(token_file)
    authentication.renew_auth_token()
    with open('token.yaml', 'w') as outfile:
        yaml.dump(authentication.token, outfile, default_flow_style=False)

    # find the alarm playlist and load it
    alarm = Alarm(authentication.token)
    alarm.set_up_alarm()
    pomodoro = input("Is this a Pomodoro timer (y/n)? ")
    if pomodoro == "y":
        print("The alarm is set for 25 minutes, followed by a 5 minute break. Make sure you focus on work!")
        while True:
            sleep(25*60)
            alarm.ring(ring_length=1)
            sleep(5*60)
            alarm.ring(ring_length=1)
    else:
        timer = int(input("How long is the timer in minutes: "))
        print("Timer has started for {t} minutes.".format(t=timer))
        sleep(timer*60)
        alarm.ring(ring_length=0.5)
if __name__ == "__main__":
    run()
