import sqlite3
import time
import web3
from web3 import Web3, Account

class Core:
    def createUser(self, publicKey, privateKey):
        sql = 'INSERT INTO users (public_key, private_key) VALUES ("{publicKey}", "{privateKey}")'.format(
            publicKey = publicKey,
            privateKey = privateKey
        )
        try:
            db = sqlite3.connect('db.db')
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def getUsers(self):
        sql = 'SELECT * FROM users'
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        result = cursor.execute(sql)
        users = result.fetchall()
        usersData = list()
        for user in users:
            userData = {
                'id': user[0],
                'publicKey': user[1],
                'privateKey': user[2]
            }
            usersData.append(userData)
        return usersData

    def getServices(self):
        sql = 'SELECT * FROM services'
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        result = cursor.execute(sql)
        services = result.fetchall()
        servicesData = list()
        for service in services:
            serviceData = {
                'id': service[0],
                'name': service[1],
                'value': service[2],
                'wallet': service[3],
                'period': service[4]
            }
            servicesData.append(serviceData)
        return servicesData

    def getServiceState(self, publicKey, serviceId):
        serviceColumnName = 'service_' + str(serviceId)
        sql = 'SELECT {serviceId}, {serviceIdTimestamp} FROM users WHERE public_key = "{publicKey}"'.format(
            serviceId = serviceColumnName,
            serviceIdTimestamp = serviceColumnName + '_payment_timestamp',
            publicKey = publicKey
        )
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        result = cursor.execute(sql)
        serviceData = result.fetchall()[0]
        serviceState = {
            'state': serviceData[0],
            'timestamp': serviceData[1]
        }
        return serviceState

    def subscribe(self, publicKey, serviceId):
        serviceColumnName = 'service_' + str(serviceId)
        timestamp = time.time()
        timestamp = str(timestamp).split('.')[0]
        sql = 'UPDATE users SET {serviceId} = {serviceStatus}, {serviceIdTimestamp} = {timestamp} WHERE public_key = "{publicKey}"'.format(
            serviceId = serviceColumnName,
            serviceStatus = 1,
            serviceIdTimestamp = serviceColumnName + '_payment_timestamp',
            timestamp = timestamp,
            publicKey = publicKey
        )
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        result = cursor.execute(sql)
        db.commit()

    def unsubscribe(self, publicKey, serviceId):
        serviceColumnName = 'service_' + str(serviceId)
        sql = 'UPDATE users SET {serviceId} = {serviceStatus} WHERE public_key = "{publicKey}"'.format(
            serviceId = serviceColumnName,
            serviceStatus = 0,
            publicKey = publicKey
        )
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        result = cursor.execute(sql)
        db.commit()

    def subscribeAll(self, publicKey):
        services = self.getServices()
        for service in services:
            serviceId = service['id']
            self.subscribe(publicKey, serviceId)

    def unsubscribeAll(self, publicKey):
        services = self.getServices()
        for service in services:
            serviceId = service['id']
            self.unsubscribe(publicKey, serviceId)

    def getServicesWithStates(self, publicKey):
        services = self.getServices()
        for service in services:
            serviceId = service['id']
            state = self.getServiceState(publicKey, serviceId)
            state = state['state']
            service.update({'state': state})
        return services

    def checkWallet(self, publicKey, privateKey):
        try:
            publicKey = Web3.toChecksumAddress(publicKey)
            account = Account.privateKeyToAccount(privateKey)
            if account.address == publicKey:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
