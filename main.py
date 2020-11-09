import socket
import subprocess
import time
import json


def port_check(port: int) -> bool:
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)
    return True if result_of_check == 0 else False


class FAMI:
    def __init__(self):
        self.server_proc = None
        with open('fami_cfg.json') as f:
            data = json.load(f)
            self.map_list = data['maplist']
            self.timeout = int(data['timeout'])

        with open('config.json') as f:
            config = json.load(f)

        self.port = config['port']
        if not port_check(self.port):
            print(f'[FAMI] {self.port} is closed. Check it!!!!')
            # exit(1)

    def change_map(self, name: str):
        with open("config.json", "r") as f:
            data = json.load(f)

        data["map"] = f'/levels/{name}/info.json'

        with open("config.json", "w") as f:
            json.dump(data, f)

    def start_server(self):
        self.server_proc = subprocess.Popen("kissmp-server.exe", shell=False)

    def shutdown_server(self):
        self.server_proc.kill()

    def __del__(self):
        self.shutdown_server()

    def launch(self):
        self.start_server()


if __name__ == "__main__":
    fami = FAMI()
    fami.start_server()
    while True:
        for map in fami.map_list:
            print(f'[FAMI] Next map is {map}')
            time.sleep(fami.timeout)
            fami.change_map(map)
            print(f'[FAMI] Change map and restart server')
            fami.shutdown_server()
            fami.start_server()
