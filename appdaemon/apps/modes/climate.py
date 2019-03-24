#
#The aim of this is to control the travel functions for individuals

import appdaemon.plugins.hass.hassapi as hass
import time

class Climate_Control(hass.Hass):

    stnotify = "notify/push_staci"
    snotify = "notify/push_simon"
    mnotify = "notify/push_megan"
    dnotify = "notify/push_delia"      
    hnotify = "notify/push_hassio"
    hangify = "notify/hang_home"
    
    mess_platform = "Hangouts"
    mess_sent = ""

    sendmess = ""


    def initialize(self):
        # this checks
        self.listen_state(self.climate_fan, "binary_sensor.climate_hot_outside_on_fan")
        self.listen_state(self.climate_fan, "binary_sensor.climate_cool_outside_off_fan")
        self.listen_state(self.climate_fan, "binary_sensor.sphone", new='on')
        self.listen_state(self.climate_fan, "binary_sensor.mphone", new='on')
        self.listen_state(self.climate_fan, "binary_sensor.stphone", new='on')
        self.listen_state(self.climate_fan, "binary_sensor.dphone", new='on')

        self.listen_state(self.climate_cont, "binary_sensor.climate_hot_turn_on_cooling")
        self.listen_state(self.climate_cont, "binary_sensor.climate_cold_turn_on_warming")
        self.listen_state(self.climate_cont, "binary_sensor.presence_home", new='on')
        self.listen_state(self.climate_cont, "sun.sun")
        
        #reset messaging for the climate control messaging (does not effect the fan)
        self.listen_state(self.mess_reset, "input_select.time_mode")

        #set messaging platform
        self.listen_state(self.mess_flag, "input_select.message_flag")

    ###
    #   This sets the correct messaging platform
    ###
    def mess_flag(self, entity, attribute, old, new, kwargs):
        self.mess_platform = new

    ###
    #   This resets the messaging flag, so that it will sent a message, once for each mode
    ###
    def mess_reset(self, entity, attribute, old, new, kwargs):
        self.mess_sent = "N"

    ###
    #   These control the fans, and the messages for the heating and cooling.
    ###
    def climate_fan(self, entity, attribute, old, new, kwargs):

        self.sendmess = ""

        #only do stuff if someone is home
        if self.get_state("binary_sensor.presence_away") == 'off':

            if self.get_state('binary_sensor.climate_cool_outside_off_fan') == 'off' and self.get_state('binary_sensor.climate_hot_outside_on_fan') == 'on':
                # turn on the fans
                if self.get_state('person.simon') == 'home' or self.get_state('person.megan') == 'home':
                    self.set_state("input_select.master_fan_flag", state="Transition") #set to transition to ensure in correct state
                    self.set_state("input_select.master_fan_flag", state="1")
                    self.sendmess += 'Master fan to on.' + '\n'
                if self.get_state('person.staci') == 'home':
                    self.set_state("input_select.staci_fan_flag", state="Transition") #set to transition to ensure in correct state
                    self.set_state("input_select.staci_fan_flag", state="1")
                    self.sendmess += "Staci's fan to on." + '\n'
                if self.get_state('person.delia') == 'home':
                    self.set_state("input_select.delia_fan_flag", state="Transition") #set to transition to ensure in correct state
                    self.set_state("input_select.delia_fan_flag", state="1")
                    self.sendmess += "Delia's fan to on." + '\n'
            elif self.get_state('binary_sensor.climate_cool_outside_off_fan') == 'on' and self.get_state('binary_sensor.climate_hot_outside_on_fan') == 'off':
                # turn off the fans
                if self.get_state('person.simon') == 'home' or self.get_state('person.megan') == 'home':
                    self.set_state("input_select.master_fan_flag", state="Transition") #set to transition to ensure in correct state
                    self.set_state("input_select.master_fan_flag", state="Off")
                    self.sendmess += 'Master fan to off.' + '\n'
                if self.get_state('person.staci') == 'home':
                    self.set_state("input_select.staci_fan_flag", state="Transition") #set to transition to ensure in correct state
                    self.set_state("input_select.staci_fan_flag", state="Off")
                    self.sendmess += "Staci's fan to off." + '\n'
                if self.get_state('person.delia') == 'home':
                    self.set_state("input_select.delia_fan_flag", state="Transition") #set to transition to ensure in correct state
                    self.set_state("input_select.delia_fan_flag", state="Off")
                    self.sendmess += "Delia's fan to off." + '\n'
       
        if self.sendmess != "":
            # send any messages from the different 
            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=self.sendmess)
                self.call_service(self.snotify,message=self.sendmess)
                self.call_service(self.dnotify,message=self.sendmess)
                self.call_service(self.stnotify,message=self.sendmess)
            elif self.mess_platform == "Hangouts":
                self.call_service(self.hangify,message=self.sendmess)

    ###
    #   These control the fans, and the messages for the heating and cooling.
    ###
    def climate_cont(self, entity, attribute, old, new, kwargs):

        self.sendmess = ""

        # when someone is home (presence away is off), run the right options
        if self.get_state("binary_sensor.presence_away") == 'off':
       
            #no heating or cooling messages in winter
            if self.get_state('sensor.season') != 'winter':
                # if autumn or spring - warn about cooling and heating
                if self.get_state('sensor.season') != 'summer':
                    #climate is optimal (heating)
                    if self.get_state('binary_sensor.climate_opt_turn_off_warming') == 'on':
                        if self.get_state('sun.sun') == 'above_horizon':
                            self.sendmess += 'You may want to turn the heating off, as it is the optimal temperature inside and the sun is up.' + '\n'
                    #climate is low
                    else:  
                        if self.get_state('binary_sensor.climate_cold_turn_on_warming') == 'on':
                            self.sendmess += '\n' + 'You may want to turn on the heating as it is overly cold inside.' + '\n'

                    # Climate is optimal (cooling)
                    if self.get_state('binary_sensor.climate_opt_turn_off_cooling') == 'on':
                        if self.get_state('sun.sun') == 'below_horizon':
                            self.sendmess += 'You may want to turn the cooling off, as it is the optimal temperature inside and the sun has set' + '\n'
                    # climate is high
                    else:
                        if self.get_state('binary_sensor.climate_hot_turn_on_cooling') == 'on':
                            if self.get_state('sun.sun') == 'above_horizon':
                                self.sendmess += 'You may want to turn on the cooling as it is hot inside and the sun is up.' + '\n'
                    
                # if summer - only worry about cooling
                else:
                    # Climate is optimal
                    if self.get_state('binary_sensor.climate_opt_turn_off_cooling') == 'on':
                        if self.get_state('sun.sun') == 'below_horizon':
                            self.sendmess += 'You may want to turn the cooling off, as it is the optimal temperature inside and the sun has set' + '\n'
                    # climate is high
                    else:
                        if self.get_state('binary_sensor.climate_hot_turn_on_cooling') == 'on':
                            if self.get_state('sun.sun') == 'above_horizon':
                                self.sendmess += 'You may want to turn on the cooling as it is hot inside and the sun is up.' + '\n'

        if self.sendmess != "" and self.mess_sent == "N":
            # send any messages from the different 
            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=self.sendmess)
                self.call_service(self.snotify,message=self.sendmess)
                self.call_service(self.dnotify,message=self.sendmess)
                self.call_service(self.stnotify,message=self.sendmess)
            elif self.mess_platform == "Hangouts":
                self.call_service(self.hangify,message=self.sendmess)
            
            self.mess_sent = "Y"
            
        
        





       


   

   
                

