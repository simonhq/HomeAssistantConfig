###################################################################
#
# This module will unlock doors based upon people walking home or driving home
#
# It uses HA zone automation to turn on flags and timers, if the timers expire, 
# the flags turn off, otherwise doors will be unlocked on people returning home
#
###################################################################

import appdaemon.plugins.hass.hassapi as hass
import datetime

class WalkLock(hass.Hass):

    stnotify = "notify/push_staci"
    snotify = "notify/push_simon"
    mnotify = "notify/push_megan"
    dnotify = "notify/push_delia"       
    hangify = "notify/hang_home"
    #hnotify = "notify/push_hassio"
    #smessage_mc = "Garage Entry Unlocked for Meg"
    #smessage_st = "Front Door Unlocked for Staci"
    #smessage_d = "Front Door Unlocked for Delia"
    #omessage_home = "Front Door Unlocked by your friendly smart home!"
    #cmessage_home = "Garage Entry Unlocked by your friendly smart home!"
    
    smessage_home = "Front Door Unlocked for Simon"
    mmessage_home = "Front Door Unlocked for Megan"
    stmessage_home = "Front Door Unlocked for Staci"
    dmessage_home = "Front Door Unlocked for Delia"
    mmessage_garage = "Garage Entry Unlocked for Meg"

    mess_platform = "Hangouts"

    def initialize(self):
             
        self.listen_state(self.walk_check,  "device_tracker.sphone")
        self.listen_state(self.walk_check,  "device_tracker.mphone")
        self.listen_state(self.walk_check,  "device_tracker.stphone")
        self.listen_state(self.walk_check,  "device_tracker.dphone")
        #car
        self.listen_state(self.car_check,  "device_tracker.mphone")
        #
        self.listen_state(self.mess_flag, "input_select.message_flag")

    def mess_flag(self, entity, attribute, old, new, kwargs):
        self.mess_platform = self.get_state("input_select.message_flag")    
        
    def walk_check(self, entity, attribute, old, new, kwargs):

        if entity == "device_tracker.sphone" and new == "home":
            if self.get_state("input_boolean.walking_home_s") == "on":
                self.turn_off("input_boolean.fdoor")
                self.turn_off("input_boolean.walking_home_s")
                if self.mess_platform == "Pushbullet":
                    self.call_service(self.mnotify,message=self.smessage_home)
                    self.call_service(self.snotify,message=self.smessage_home)
                    self.call_service(self.dnotify,message=self.smessage_home)
                    self.call_service(self.stnotify,message=self.smessage_home)
                elif self.mess_platform == "Hangouts":
                    self.call_service(self.hangify,message=self.smessage_home)
                #self.call_service("hangouts/send_message",target=[{ "name": "Home" }] ,message=[{ "text": self.smessage_home }])
                #self.call_service(self.snotify,message=self.smessage_home)
        elif entity == "device_tracker.mphone" and new == "home":
            if self.get_state("input_boolean.walking_home_m") == "on":
                self.turn_off("input_boolean.fdoor")
                self.turn_off("input_boolean.walking_home_m")
                if self.mess_platform == "Pushbullet":
                    self.call_service(self.mnotify,message=self.mmessage_home)
                    self.call_service(self.snotify,message=self.mmessage_home)
                    self.call_service(self.dnotify,message=self.mmessage_home)
                    self.call_service(self.stnotify,message=self.mmessage_home)
                elif self.mess_platform == "Hangouts":
                    self.call_service(self.hangify,message=self.mmessage_home)
                #self.call_service("hangouts/send_message",target=[{ "name": "Home" }] ,message=[{ "text": self.mmessage_home }])
                #self.call_service(self.mnotify,message=self.omessage_home)
                #self.call_service(self.snotify,message=self.smessage_m)
        elif entity == "device_tracker.stphone" and new == "home":
            if self.get_state("input_boolean.walking_home_st") == "on":
                self.turn_off("input_boolean.fdoor")
                self.turn_off("input_boolean.walking_home_st")
                if self.mess_platform == "Pushbullet":
                    self.call_service(self.mnotify,message=self.stmessage_home)
                    self.call_service(self.snotify,message=self.stmessage_home)
                    self.call_service(self.dnotify,message=self.stmessage_home)
                    self.call_service(self.stnotify,message=self.stmessage_home)
                elif self.mess_platform == "Hangouts":
                    self.call_service(self.hangify,message=self.stmessage_home)
                #self.call_service("hangouts/send_message",target=[{ "name": "Home" }] ,message=[{ "text": self.stmessage_home }])
                #self.call_service(self.stnotify,message=self.omessage_home)
                #self.call_service(self.snotify,message=self.smessage_st)
        elif entity == "device_tracker.dphone" and new == "home":
            if self.get_state("input_boolean.walking_home_d") == "on":
                self.turn_off("input_boolean.fdoor")
                self.turn_off("input_boolean.walking_home_d")
                if self.mess_platform == "Pushbullet":
                    self.call_service(self.mnotify,message=self.dmessage_home)
                    self.call_service(self.snotify,message=self.dmessage_home)
                    self.call_service(self.dnotify,message=self.dmessage_home)
                    self.call_service(self.stnotify,message=self.dmessage_home)
                elif self.mess_platform == "Hangouts":
                    self.call_service(self.hangify,message=self.dmessage_home)
                #self.call_service("hangouts/send_message",target=[{ "name": "Home" }] ,message=[{ "text": self.dmessage_home }])
                #self.call_service(self.dnotify,message=self.omessage_home)
                #self.call_service(self.snotify,message=self.smessage_d)

    def car_check(self, entity, attribute, old, new, kwargs):

        if entity == "device_tracker.mphone" and new == "home":
            if self.get_state("input_select.trans_megan") == "Car":
                self.turn_off("input_boolean.gdoor")
                self.set_state("input_select.trans_megan", state="Walk")
                if self.mess_platform == "Pushbullet":
                    self.call_service(self.mnotify,message=self.mmessage_garage)
                    self.call_service(self.snotify,message=self.mmessage_garage)
                    self.call_service(self.dnotify,message=self.mmessage_garage)
                    self.call_service(self.stnotify,message=self.mmessage_garage)
                elif self.mess_platform == "Hangouts":
                    self.call_service(self.hangify,message=self.mmessage_garage)
                #self.call_service("hangouts/send_message",target=[{ "name": "Home" }] ,message=[{ "text": self.mmessage_garage }])
                #self.call_service(self.mnotify,message=self.cmessage_home)
                #self.call_service(self.snotify,message=self.smessage_mc)

        

        
        