import time
import threading
from fantom import Fantom
from core import Core

class Payment(threading.Thread):
    def __init__(self):
        self.ftm = Fantom()
        self.core = Core()
        self.users = self.core.getUsers()
        self.services = self.core.getServices()
        threading.Thread.__init__(self)

    def run(self):
        while True:
            for user in self.users:
                userId = user['id']
                for service in self.services:
                    try:
                        serviceId = service['id']
                        userWallet = user['publicKey']
                        serviceState = self.core.getServiceState(userWallet, serviceId)
                        state = serviceState['state']
                        if state == 1:
                            timestamp = serviceState['timestamp']
                            nowTimestamp = time.time()
                            nowTimestamp = str(nowTimestamp).split('.')[0]
                            serviceTimestamp = service['period']
                            if int(nowTimestamp) - timestamp > serviceTimestamp:
                                userPrivateKey = user['privateKey']
                                serviceWallet = service['wallet']
                                value = service['value']
                                tx = self.ftm.generateTx(userWallet, serviceWallet, int(value))
                                signTx = self.ftm.signTx(tx, userPrivateKey)
                                txData = self.ftm.sendTx(signTx)
                                self.core.subscribe(userWallet, serviceId)
                                print(txData)
                    except Exception as e:
                        print(e)
            try:
                self.users = self.core.getUsers()
                self.services = self.core.getServices()
            except Exception as e:
                print(e)
            time.sleep(10)
