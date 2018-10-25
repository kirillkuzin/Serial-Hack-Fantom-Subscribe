import requests
import json
from web3 import Web3
from web3.auto import w3

class Fantom:
    DEFAULT_GAS_PRICE = '0x000000000001'
    DEFAULT_GAS = '0x27100'
    BASE_URL = 'http://18.221.128.6:8080/'

    def getAccount(self, publicKey):
        response = requests.get(self.BASE_URL + 'account/' + publicKey)
        accountData = response.json()
        return accountData

    def getNonce(self, publicKey):
        accountData = self.getAccount(publicKey)
        nonce = accountData['nonce']
        return nonce

    def getBalance(self, publicKey):
        accountData = self.getAccount(publicKey)
        balance = accountData['balance']
        return balance

    def generateTx(self, senderAddress, receiverAddress, value):
        nonce = self.getNonce(senderAddress)
        tx = {
            'to': receiverAddress,
            'value': value,
            'gasPrice': self.DEFAULT_GAS_PRICE,
            'gas': self.DEFAULT_GAS,
            'nonce': nonce,
            'data': '0x',
            'chainId': 1
        }
        return tx

    def signTx(self, tx, privateKey):
        signed = w3.eth.account.signTransaction(tx, privateKey)
        rawTransaction = Web3.toHex(signed['rawTransaction'])
        return rawTransaction

    def sendTx(self, tx):
        response = requests.post(self.BASE_URL + 'sendRawTransaction', data = tx)
        txData = response.json()
        return txData
