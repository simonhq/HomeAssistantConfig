#
#The aim of this is to do send messages about transport
#

import appdaemon.plugins.hass.hassapi as hass
import time
import globals

class Transport_Messages(hass.Hass):
    
    smess_tugg = "Simon just left Tuggeranong Interchange"
    smess_171 = "Simon is on the 171 bus home"
    smess_300 = "Simon is on the 300 bus to Tuggeranong"
    smess_300W = "Simon just left Woden heading to Tuggeranong"
    smess_300C = "Simon just left Woden heading to City"
    #dmess_home = "Delia just got home"
    dmess_bus = "Delia just left Tuggeranong Interchange"
    #stmess_home = "Staci just got home"
    mmess_300 = "Megan is on the 300 bus to Tuggeranong"
    mmess_300W = "Megan just left Woden heading to Tuggeranong"
    mmess_car = "Megan is heading to the car from work"
    stmess_3 = "Staci is on the 3 into the city, will arrive in about 20 minutes!"
    stmess_300H = "Staci is on the 300 to tuggeranong, about 45 minutes"
    stmess_300C = "Staci is on the 300 from CIT, might be going to the City or Tuggeranong"
    stmess_67 = "Staci is on the 67 from Canberra Hospital, heading home"
    stmess_66 = "Staci is on the 66 from Canberra Hospital, heading to Calwell shops in about 15 minutes, or Tuggeranong in 30 minutes"


    def initialize(self):
        
        # bring in the messaging module
        self.notifier = self.get_app('messaging')

        self.listen_state(self.reset_transport, "input_boolean.mode_return_home")
        self.listen_state(self.transport_simon, "input_select.trans_simon")
        self.listen_state(self.transport_megan, "input_select.trans_megan")
        self.listen_state(self.transport_staci, "input_select.trans_staci")
        self.listen_state(self.transport_delia, "input_select.trans_delia")
        #set messaging platform
        self.listen_state(self.mess_flag, "input_select.message_flag")
        #self.listen_state(self.screens, "input_select.presence_mode") # done in automation/presence

    def mess_flag(self, entity, attribute, old, new, kwargs):
        self.mess_platform = self.get_state("input_select.message_flag")
    
    def screens(self, entity, attribute, old, new, kwargs):
        sflag = 0
        if new == "Someone Home" and old == "All Away":
            sflag = 1
        elif new == "All Home" and old == "All Away":
            sflag = 1
        elif new == "All Away":
            sflag = 2
        else:
            sflag = 3

        if sflag == 1:
            self.call_service(self.hnotify,message=self.hmessage_home)
        elif sflag == 2:
            self.call_service(self.hnotify,message=self.hmessage_away)

    ################## look at this

    def reset_transport(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.set_state("input_select.trans_simon", state="Nil")
            self.set_state("input_select.trans_megan", state="Nil")
            self.set_state("input_select.trans_staci", state="Nil")
            self.set_state("input_select.trans_delia", state="Nil")

    ################## look at this      

    def transport_simon(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_boolean.mode_return_home") == "on":
            if new == "Bus":
                self.notifier.notify(self.smess_tugg)
            elif new == "171":
                self.notifier.notify(self.smess_171)
            elif new == "300":
                self.notifier.notify(self.smess_300)
            elif new == "300W" and old == "300":
                self.notifier.notify(self.smess_300W)
            elif new == "300W" and old == "Bus":
                self.notifier.notify(self.smess_300C)

    def transport_delia(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_boolean.mode_return_home") == "on":
            if new == "Bus":
                self.notifier.notify(self.dmess_bus)
                
    def transport_megan(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_boolean.mode_return_home") == "on":
            if new == "300C":
                if self.get_state("input_boolean.bus_meg_300_city") == "on":
                    self.notifier.notify(self.mmess_300)
                    #self.turn_off("input_boolean.bus_meg_300_city") #done in transport.yaml
            elif new == "300W" and old == "300C":
                self.notifier.notify(self.mmess_300W)
            elif new == "Car":
                self.notifier.notify(self.mmess_car)
                                
    def transport_staci(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_boolean.mode_return_home") == "on":
            if new == "300H":
                if self.get_state("input_boolean.bus_staci_300_city") == "on":
                    self.turn_off("input_boolean.bus_staci_300_city")
                    self.notifier.notify(self.stmess_300H)
            elif new == "3":
                self.notifier.notify(self.stmess_3)
            elif new == "300C":
                self.notifier.notify(self.stmess_300C)
            elif new == "66":
                self.notifier.notify(self.stmess_66)
            elif new == "67":
                self.notifier.notify(self.stmess_67)
                
                

