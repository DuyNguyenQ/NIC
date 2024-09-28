import json
import struct
import socket
import logging

PACK_FMT_STR = '!BBHLH6s'

class frame:
    def creat(reqId, msgType, msg={}):
        msgLen = 0
        jsonStr = json.dumps(msg)
        if (msg != {}):
            msgLen = len(jsonStr)
        rawMsg = struct.pack(PACK_FMT_STR, 0x5A, 0x01, reqId, msgLen,msgType, b'\x00\x00\x00\x00\x00\x00')

        if (msg != {}):
            rawMsg += bytearray(jsonStr,'ascii')
        return rawMsg
class tranmit:
    def sendAPI(headerAPI:socket.socket,code_api:int,jsonstring:dict):
        headerAPI.send(frame.creat(1,code_api,jsonstring))
        dataall = b''
        try:    
            data = headerAPI.recv(16)
        except socket.timeout:
            print('timeout')
            headerAPI.close()
        if(len(data) < 16):
            print('Pack head error')
            headerAPI.close()
        else:
            header = struct.unpack(PACK_FMT_STR, data)
            jsonDataLen = header[3]
            backReqNum = header[4]
        dataall += data
        data = b''
        readSize = 1024
        try:
            while (jsonDataLen > 0):
                recv = headerAPI.recv(readSize)
                data += recv
                jsonDataLen -= len(recv)
                if jsonDataLen < readSize:
                    readSize = jsonDataLen
            data = json.loads(data)
            print(data)
            return data
        except socket.timeout:
            print('timeout')
            logging.info(str(headerAPI)+"/t: time out ----------------------------------------------------")
