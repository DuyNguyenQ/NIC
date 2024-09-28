#!/usr/bin/python3
from socket import socket
from frame import frame, tranmit
from api import status, navigation, config, control, other
import socket
import time
import logging


format_HMS = '%H:%M:%S'

class AMR_APi:
    def __init__(self,host:str):
        self.host = host
        self.apiRobotStatus     = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.apiRobotNavigation = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.apiRobotOther      = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.apiRobotConfig      = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.apiRobotControl      = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.keys = {
        "keys":["vehicle_id","area_ids","confidence","current_station","last_station","vx","vy","blocked","block_reason","battery_level","task_status","target_id","emergency","reloc_status","fatals","errors","warnings","notices","current_ip",'x','y','fork_height',"current_map","angle"],
        "return_laser":False,
        "return_beams3D":False
        }
        self.data_Status={}
    
    def connect_status(self):
        self.apiRobotStatus.settimeout(3000)
        self.apiRobotStatus.connect((self.host,19204))

    def connect_navigation(self):
        self.apiRobotNavigation.settimeout(3000)
        self.apiRobotNavigation.connect((self.host,19206))

    def connect_other(self):
        self.apiRobotOther.settimeout(3000)
        self.apiRobotOther.connect((self.host,19210))

    def connect_config(self):
        self.apiRobotConfig.settimeout(3000)
        self.apiRobotConfig.connect((self.host,19207))
        
    def connect_control(self):
        self.apiRobotControl.settimeout(3000)
        self.apiRobotControl.connect((self.host,19205))

    def navigation(self,jsonstring:dict):
        result = tranmit.sendAPI(self.apiRobotNavigation, navigation.robot_task_gotarget_req, jsonstring)
        logging.info(result)
        while result['ret_code'] != 0:
            result = tranmit.sendAPI(self.apiRobotNavigation, navigation.robot_task_gotarget_req, jsonstring)
            logging.info(result)
        return True
    def status(self,key):
        #request location robot
        self.data_Status = tranmit.sendAPI(self.apiRobotStatus, status.robot_status_all1_req, key)
    
    def confirm_local(self):
        tranmit.sendAPI(self.apiRobotControl,control.robot_control_comfirmloc_req,{})
    def cancel_navigation(self):
        tranmit.sendAPI(self.apiRobotNavigation,navigation.robot_task_cancel_req,{})

    def device_setShelf(self,jsonString:dict):
        result = tranmit.sendAPI(self.apiRobotConfig, config.robot_config_set_shelfshape_req, jsonString)
        logging.info(result)
        while result['ret_code'] != 0:
            result = tranmit.sendAPI(self.apiRobotConfig, config.robot_config_set_shelfshape_req, jsonString)
            logging.info(result)
        return True
    
    def device_unsetShelf(self,jsonString:dict):
        result = tranmit.sendAPI(self.apiRobotConfig, config.robot_config_clear_goodsshape_req, jsonString)
        logging.info(result)
        while result['ret_code'] != 0:
            result = tranmit.sendAPI(self.apiRobotConfig, config.robot_config_clear_goodsshape_req, jsonString)
            logging.info(result)
        return True
    
    def control_audio(self,jsonString:dict):
        return tranmit.sendAPI(self.apiRobotOther, other.robot_other_play_audio_req, jsonString)
        
    def navigation_move_task_list(self,jsonstring:dict):
        return tranmit.sendAPI(self.apiRobotNavigation, navigation.robot_task_gotargetlist_req, jsonstring)
    
    def device_map(self,map_name:str):
        return tranmit.sendAPI(self.apiRobotConfig,config.robot_config_downloadmap_req,{"map_name":map_name})

    def check_target(self,data_status:dict, target:str):
        time.sleep(1)
        if(data_status['task_status'] == 4):
            if(data_status['current_station']) == target:
                return True
            else:
                return False
        else:
            return False
