from hcloud import Client
from hcloud.images.domain import Image
from hcloud.servers.domain import Server
from hcloud.server_types.domain import ServerType
from hcloud.volumes.domain import Volume
import time

class GameData:
    running = False
    
    def __init__(self, token, name, servertype, snapshot, volume):
        self.name = name
        self.servertype = servertype
        self.client = Client(token=token)
        
        # get id from snapshot
        images = self.client.images.get_all()
        for i in images:
            if i.data_model.description == snapshot:
                imageId = i.data_model.id
        self.snapshot = imageId

        # get id from volume
        volumes = self.client.volumes.get_all()
        for i in volumes:
            if i.data_model.name == volume:
                volumeId = i.data_model.id
        self.volume = volumeId

        # check for running server
        servers = self.client.servers.get_all()
        self.server = None
        for i in servers:
            if i.data_model.name == name:
                self.server = i.data_model
                self.running = True
                print("existing server " + self.server.status)

    def start(self):
        if self.running == False:
            print("Starting " + self.name)
            response = self.client.servers.create(
                self.name,
                server_type=ServerType(name=self.servertype),
                image=Image(self.snapshot),
                volumes=[Volume(self.volume)]
            )
            self.server = response.server;
            #while self.server.status != Server.STATUS_RUNNING:
            #    print(self.server.status)
            #    time.sleep(2)
            #    serv = self.client.servers.get_by_id(self.server.id)
            #    self.server = serv
            #print("Server is now running")
            self.running = True
        else:
            print(self.name + " is already running")

    def stop(self):
        if self.running == True:
            print("Stopping " + self.name)
            self.client.servers.shutdown(self.server)
            while self.server.status != Server.STATUS_OFF:
                print(self.server.status)
                time.sleep(5)
                serv = self.client.servers.get_by_id(self.server.id)
                self.server = serv
            print("Server is now stopped")
            self.client.volumes.detach(Volume(self.volume))
            self.client.servers.delete(self.server)
            self.running = False
            self.server = None
        else:
            print(self.name + " isn't running")

    def status(self):
        msg = self.name
        if self.server == None:
            msg += " isn't running"
        else:
            self.server = self.client.servers.get_by_id(self.server.id)
            msg += " is in status "
            msg += self.server.status
            msg += "\n"
            msg += "and has the IP:\n"
            ip = self.server.public_net.ipv4.ip
            msg += ip + "\n"
        return msg

    def isRunning(self):
        return self.running

