import requests
from time import sleep

class Alarm(object):
    def __init__(self, token):
        self.base_url = "https://api.ws.sonos.com/control/api/v1/"
        self.household_url = self.base_url + "households"
        self.auth= {"Authorization": token["token_type"] + " " + token["access_token"]}


    def get_household(self):
        r = requests.get(self.household_url, headers=self.auth)
        if r.ok:
            self.household = r.json()["households"][0]["id"]
            self.playlist_get_url = self.household_url + '/' + self.household + '/playlists'
            self.group_url = self.household_url + '/' + self.household + '/groups'
            return self.household
        else:
            raise ValueError("Unable to retrieve the households")


    def get_group(self):
        r = requests.get(self.group_url, headers=self.auth)
        if r.ok:
            group = r.json()['groups'][0]
            self.group_id_url = self.group_url + '/' + group["id"]
            self.playlist_post_url = self.group_id_url + '/playlists'
            return group["id"]
        raise ValueError("Unable to find groups")


    def get_alarm_playlist(self):
        r = requests.get(self.playlist_get_url, headers=self.auth)
        if r.ok:
            for playlist in r.json()['playlists']:
                if playlist["name"] == "Timer":
                    self.playlist_id = playlist["id"]
                    return self.playlist_id
        raise ValueError("The playlist with the name 'Timer' could not be found")


    def set_up_alarm(self):
        self.get_household()
        self.get_group()
        self.get_alarm_playlist()


    def ring(self, ring_length): # ring length is in minutes
        params = {
            "playlistId": self.playlist_id,
            "playOnCompletion": True,
            "playModes":{
                "shuffle": True
                }
        }
        r = requests.post(self.playlist_post_url, headers=self.auth, json=params)

        if r.ok:
            sleep(ring_length*60)
            pause_url = self.group_id_url + '/playback/pause'
            pause = requests.post(pause_url, headers=self.auth)
            if pause.ok:
                print("The alarm has stopped.")
                return
            raise ValueError("The playlist could not be loaded.")
        raise ValueError("The playlist could not be loaded.")
