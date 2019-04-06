#
#The aim of this is to do send messages about car 

import appdaemon.plugins.hass.hassapi as hass
import time

class Car_Messages(hass.Hass):

    stnotify = "notify/push_staci"
    snotify = "notify/push_simon"
    mnotify = "notify/push_megan"
    dnotify = "notify/push_delia"      
    hnotify = "notify/push_hassio"
    hangify = "notify/hang_home"
    
    mess_platform = "Hangouts"
    away_flag = "off"

    s_loc = "home"
    m_loc = "home"
    st_loc = "home"
    d_loc = "home"

    sendmess = ""

    smess = "Simon is currently at "
    mmess = "Megan is currently at "
    stmess = "Staci is currently at "
    dmess = "Delia is currently at "
    hmess = "The best route home is via "
    wmess = "The best route to the city is via "

    t_mess = " which is approx "
    e_mess = " minutes away via "

    def initialize(self):
        self.listen_state(self.meg_car, "input_boolean.megan_outback")
        self.listen_state(self.sim_car, "input_boolean.simon_outback")
        # car away
        self.listen_state(self.car_away, "input_boolean.presence_holiday")

        # keep track of locations
        self.listen_state(self.sim_loc, "device_tracker.sphone")
        self.listen_state(self.meg_loc, "device_tracker.mphone")
        self.listen_state(self.sta_loc, "device_tracker.stphone")
        self.listen_state(self.del_loc, "device_tracker.dphone")

        #set messaging platform
        self.listen_state(self.mess_flag, "input_select.message_flag")

    def car_away(self, entity, attribute, old, new, kwargs):
        self.away_flag = new

    def sim_loc(self, entity, attribute, old, new, kwargs):
        self.s_loc = new
    
    def meg_loc(self, entity, attribute, old, new, kwargs):
        self.m_loc = new

    def sta_loc(self, entity, attribute, old, new, kwargs):
        self.st_loc = new

    def del_loc(self, entity, attribute, old, new, kwargs):
        self.d_loc = new

    def mess_flag(self, entity, attribute, old, new, kwargs):
        self.mess_platform = new

    def meg_car(self, entity, attribute, old, new, kwargs):
        if new == "on":
            if self.away_flag == "off":
                #meg is connected to the car
                self.sendmess = "Megan is now driving, use text messages if you need to contact her. " + "\n"
                if self.m_loc != "home":
                    self.sendmess += self.hmess + self.get_state("sensor.m_to_h_route") + "\n"
                else:
                    self.sendmess += self.wmess + self.get_state("sensor.m_to_w_route") + "\n"
                #if self.s_loc != "home":
                self.sendmess += self.smess + self.s_loc + self.t_mess + self.get_state("sensor.waze_meg_to_simon") + self.e_mess + self.get_state("sensor.m_to_s_route") + "\n"
                #if self.st_loc != "home":
                self.sendmess += self.stmess + self.st_loc + self.t_mess + self.get_state("sensor.waze_meg_to_staci") + self.e_mess + self.get_state("sensor.m_to_st_route") + "\n"
                #if self.d_loc != "home":
                self.sendmess += self.dmess + self.d_loc + self.t_mess + self.get_state("sensor.waze_meg_to_delia") + self.e_mess + self.get_state("sensor.m_to_d_route") + "\n"
                if self.mess_platform == "Pushbullet":
                    self.call_service(self.mnotify,message=self.sendmess)
                    self.call_service(self.snotify,message=self.sendmess)
                    self.call_service(self.dnotify,message=self.sendmess)
                    self.call_service(self.stnotify,message=self.sendmess)
                elif self.mess_platform == "Hangouts":
                    self.call_service(self.hangify,message=self.sendmess)

    def sim_car(self, entity, attribute, old, new, kwargs):
        if new == "on":
            if self.away_flag == "off":
                #simon is connected to the car
                self.sendmess = "Simon is now driving, use text messages if you need to contact him. " + "\n"
                #if self.s_loc != "home":
                #    self.sendmess += self.hmess + self.get_state("sensor.s_to_h_route") + "\n"
                #if self.m_loc != "home":
                self.sendmess += self.mmess + self.m_loc + self.t_mess + self.get_state("sensor.waze_meg_to_simon") + self.e_mess + self.get_state("sensor.m_to_s_route") + "\n"
                #if self.st_loc != "home":
                self.sendmess += self.stmess + self.st_loc + self.t_mess + self.get_state("sensor.waze_simon_to_staci") + self.e_mess + self.get_state("sensor.s_to_st_route") + "\n"
                #if self.d_loc != "home":
                self.sendmess += self.dmess + self.d_loc + self.t_mess + self.get_state("sensor.waze_simon_to_delia") + self.e_mess + self.get_state("sensor.s_to_d_route") + "\n"
                if self.mess_platform == "Pushbullet":
                    self.call_service(self.mnotify,message=self.sendmess)
                    self.call_service(self.snotify,message=self.sendmess)
                    self.call_service(self.dnotify,message=self.sendmess)
                    self.call_service(self.stnotify,message=self.sendmess)
                elif self.mess_platform == "Hangouts": 
                    self.call_service(self.hangify,message=self.sendmess)


   

   
                

