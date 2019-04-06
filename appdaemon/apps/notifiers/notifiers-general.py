#
#The aim of this is to do send messages about things in the house
#

import appdaemon.plugins.hass.hassapi as hass
import time

class General_Messages(hass.Hass):

    stnotify = "notify/push_staci"
    snotify = "notify/push_simon"
    mnotify = "notify/push_megan"
    dnotify = "notify/push_delia"      
    hnotify = "notify/push_hassio"
    hangify = "notify/hang_home"
    
    mess_platform = "Hangouts"

    mess = ""
    flag = 0
    washer = "Washing Machine stopped"
    dryer = "Dryer stopped"
    batt = "'s phone is low on battery"
    printer = "'s printer ink is low"
    disk = "Hassio Pi Server harddrive is almost full"
    cpu = "Hassio Pi Server CPU is very high"
    
    def initialize(self):
        self.listen_state(self.disk_set, "binary_sensor.disk_alert")
        self.listen_state(self.cpu_set, "binary_sensor.cpu_alert")

        self.listen_state(self.ink_set, "binary_sensor.ink_black_alert")
        self.listen_state(self.ink_set, "binary_sensor.ink_cyan_alert")
        self.listen_state(self.ink_set, "binary_sensor.ink_magenta_alert")
        self.listen_state(self.ink_set, "binary_sensor.ink_yellow_alert")

        self.listen_state(self.batt_set, "binary_sensor.simon_batt_low")
        self.listen_state(self.batt_set, "binary_sensor.megan_batt_low")
        self.listen_state(self.batt_set, "binary_sensor.staci_batt_low")
        self.listen_state(self.batt_set, "binary_sensor.delia_batt_low")

        self.listen_state(self.batt_notify, "input_boolean.batt_notify_system")
        self.listen_state(self.printer_notify, "input_boolean.ink_notify_system")
        self.listen_state(self.disk_notify, "input_boolean.disk_notify_system")
        self.listen_state(self.cpu_notify, "input_boolean.cpu_notify_system")

        self.listen_state(self.washing_notify, "binary_sensor.samwash")
        self.listen_state(self.drying_notify, "binary_sensor.samdry")

        #self.listen_state(self.gps_notify, "device_tracker.sphone_net")
        #self.listen_state(self.gps_notify, "device_tracker.mphone_net")
        #self.listen_state(self.gps_notify, "device_tracker.stphone_net")
        #self.listen_state(self.gps_notify, "device_tracker.dphone_net")

        self.listen_state(self.gps_notify, "sensor.sphone_gps_up")
        self.listen_state(self.gps_notify, "sensor.mphone_gps_up")
        self.listen_state(self.gps_notify, "sensor.stphone_gps_up")
        self.listen_state(self.gps_notify, "sensor.dphone_gps_up")

        #set messaging platform
        self.listen_state(self.mess_flag, "input_select.message_flag")
        
    def mess_flag(self, entity, attribute, old, new, kwargs):
        self.mess_platform = self.get_state("input_select.message_flag")

    def ink_set(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.turn_on("input_boolean.ink_notify_system")

    def batt_set(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.turn_on("input_boolean.batt_notify_system")
    
    def disk_set(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.turn_on("input_boolean.disk_notify_system")

    def cpu_set(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.turn_on("input_boolean.cpu_notify_system")

    def washing_notify(self, entity, attribute, old, new, kwargs):
        if new == "off":
            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=self.washer)
                self.call_service(self.snotify,message=self.washer)
                self.call_service(self.stnotify,message=self.washer)
                self.call_service(self.dnotify,message=self.washer)
            elif self.mess_platform == "Hangouts":
                self.call_service(self.hangify,message=self.washer)

    def drying_notify(self, entity, attribute, old, new, kwargs):
        if new == "off":
            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=self.dryer)
                self.call_service(self.snotify,message=self.dryer)
                self.call_service(self.stnotify,message=self.dryer)
                self.call_service(self.dnotify,message=self.dryer)
            elif self.mess_platform == "Hangouts":
                self.call_service(self.hangify,message=self.dryer)
    
    def disk_notify(self, entity, attribute, old, new, kwargs):
        if new == "off":
            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=self.disk)
                self.call_service(self.snotify,message=self.disk)
                self.call_service(self.stnotify,message=self.disk)
                self.call_service(self.dnotify,message=self.disk)
            elif self.mess_platform == "Hangouts":
                self.call_service(self.hangify,message=self.disk)
            
            self.turn_off("input_boolean.disk_notify_system")

    def cpu_notify(self, entity, attribute, old, new, kwargs):
        if new == "off":
            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=self.cpu)
                self.call_service(self.snotify,message=self.cpu)
                self.call_service(self.stnotify,message=self.cpu)
                self.call_service(self.dnotify,message=self.cpu)
            elif self.mess_platform == "Hangouts":
                self.call_service(self.hangify,message=self.cpu)

            self.turn_off("input_boolean.cpu_notify_system")

    def printer_notify(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.mess = ""
            self.flag = 0

            if self.get_state("binary_sensor.ink_black_alert") == "on":
                self.mess = "Black"
                self.flag = 1

            if self.get_state("binary_sensor.ink_cyan_alert") == "on":
                if self.flag > 0:
                    self.mess += " & Cyan"
                else:
                    self.mess = "Cyan"
                    self.flag = 1
            
            if self.get_state("binary_sensor.ink_magenta_alert") == "on":
                if self.flag > 0:
                    self.mess += " & Magenta"
                else:
                    self.mess = "Magenta"
                    self.flag = 1

            if self.get_state("binary_sensor.ink_yellow_alert") == "on":
                if self.flag > 0:
                    self.mess += " & Yellow"
                else:
                    self.mess = "Yellow"
                    flag = 1

            self.mess += self.printer            
            self.turn_off("input_boolean.ink_notify_system")

            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=self.mess)
                self.call_service(self.snotify,message=self.mess)
                self.call_service(self.stnotify,message=self.mess)
                self.call_service(self.dnotify,message=self.mess)
            elif self.mess_platform == "Hangouts":
                self.call_service(self.hangify,message=self.mess)

    def batt_notify(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.mess = ""
            self.flag = 0

            if self.get_state("binary_sensor.simon_batt_low") == "on":
                self.mess = "Simon"
                self.flag = 1

            if self.get_state("binary_sensor.megan_batt_low") == "on":
                if self.flag > 0:
                    self.mess += " & Megan"
                else:
                    self.mess = "Megan"
                    self.flag = 1
            
            if self.get_state("binary_sensor.staci_batt_low") == "on":
                if self.flag > 0:
                    self.mess += " & Staci"
                else:
                    self.mess = "Staci"
                    self.flag = 1

            if self.get_state("binary_sensor.delia_batt_low") == "on":
                if self.flag > 0:
                    self.mess += " & Delia"
                else:
                    self.mess = "Delia"
                    flag = 1

            self.mess += self.batt
            self.turn_off("input_boolean.batt_notify_system")            

            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=self.mess)
                self.call_service(self.snotify,message=self.mess)
                self.call_service(self.stnotify,message=self.mess)
                self.call_service(self.dnotify,message=self.mess)
            elif self.mess_platform == "Hangouts":
                self.call_service(self.hangify,message=self.mess)

    def gps_notify(self, entity, attribute, old, new, kwargs):
        self.mess = ""

        if entity == 'sensor.sphone_gps_up':
            if float(self.get_state('sensor.sphone_gps_up')) >= 2:
                self.mess = "Hi Simon, logging hasn't reported for a while, can you check it please."
        elif entity == 'sensor.mphone_gps_up':
            if float(self.get_state('sensor.mphone_gps_up')) >= 2:
                self.mess = "Hi Megan, logging hasn't reported for a while, can you check it please."
        elif entity == 'sensor.stphone_gps_up':
            if float(self.get_state('sensor.stphone_gps_up')) >= 2:
                self.mess = "Hi Staci, logging hasn't reported for a while, can you check it please."
        elif entity == 'sensor.dphone_gps_up':
            if float(self.get_state('sensor.dphone_gps_up')) >= 2:
                self.mess = "Hi Delia, logging hasn't reported for a while, can you check it please."

        if self.mess_platform == "Pushbullet":
            self.call_service(self.mnotify,message=self.mess)
            self.call_service(self.snotify,message=self.mess)
            self.call_service(self.stnotify,message=self.mess)
            self.call_service(self.dnotify,message=self.mess)
        elif self.mess_platform == "Hangouts":
            self.call_service(self.hangify,message=self.mess)


