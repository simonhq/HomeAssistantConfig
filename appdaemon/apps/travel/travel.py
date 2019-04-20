#
#The aim of this is to control the travel functions for individuals

# Version 2 - March 2019

import appdaemon.plugins.hass.hassapi as hass
import time
import globals

class Travel_Messages(hass.Hass):

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
    umess = "The best route to City West is via "

    t_mess = " which is approx "
    e_mess = " minutes away via "

    def initialize(self):

        # bring in the messaging module
        self.notifier = self.get_app('messaging')

        # car connection messages
        self.listen_state(self.con_car, "binary_sensor.drive_meg")
        self.listen_state(self.con_car, "binary_sensor.drive_simon")
        # megan car or walkbus
        self.listen_state(self.meg_trav, "binary_sensor.megan_car")
        self.listen_state(self.meg_trav, "binary_sensor.megan_walkbus")
        # simon car or walkbus
        self.listen_state(self.sim_trav, "binary_sensor.simon_car")
        self.listen_state(self.sim_trav, "binary_sensor.simon_walkbus")
        # staci car or walkbus
        self.listen_state(self.sta_trav, "binary_sensor.staci_car")
        self.listen_state(self.sta_trav, "binary_sensor.staci_walkbus")
        # delia car or walkbus
        self.listen_state(self.del_trav, "binary_sensor.delia_car")
        self.listen_state(self.del_trav, "binary_sensor.delia_walkbus")
        

        # tasker proximity code - trial
        self.listen_state(self.arr_task, "input_boolean.simon_outback_home")
        self.listen_state(self.arr_task, "input_boolean.megan_outback_home")
        #these maybe needed if the girls starting driving - not implemented now
        #self.listen_state(self.arr_task, "input_boolean.staci_outback_home")
        #self.listen_state(self.arr_task, "input_boolean.delia_outback_home")

        # ha proximity code - doesn't work consistently due to gps
        self.listen_state(self.arr_prox, "proximity.home_meg")
        self.listen_state(self.arr_prox, "proximity.home_simon")
        #these maybe needed if the girls starting driving - not implemented now
        #self.listen_state(self.sta_prox, "proximity.home_staci")
        #self.listen_state(self.del_prox, "proximity.home_delia")

        # car away
        self.listen_state(self.car_away, "input_boolean.presence_holiday")
        # keep track of locations
        self.listen_state(self.sim_loc, "device_tracker.sphone")
        self.listen_state(self.meg_loc, "device_tracker.mphone")
        self.listen_state(self.sta_loc, "device_tracker.stphone")
        self.listen_state(self.del_loc, "device_tracker.dphone")

    def car_away(self, entity, attribute, old, new, kwargs):
        self.away_flag = new

    def sim_loc(self, entity, attribute, old, new, kwargs):
        self.s_loc = new
        if new != 'home' and self.m_loc != 'home':
            self.set_state("input_select.master_fan_flag", state="Transition") #set to transition to ensure in correct state
            self.set_state("input_select.master_fan_flag", state="Off")
    
    def meg_loc(self, entity, attribute, old, new, kwargs):
        self.m_loc = new
        if new != 'home' and self.s_loc != 'home':
            self.set_state("input_select.master_fan_flag", state="Transition") #set to transition to ensure in correct state
            self.set_state("input_select.master_fan_flag", state="Off")

    def sta_loc(self, entity, attribute, old, new, kwargs):
        self.st_loc = new
        if new != 'home':
            self.set_state("input_select.staci_fan_flag", state="Transition") #set to transition to ensure in correct state
            self.set_state("input_select.staci_fan_flag", state="Off")

    def del_loc(self, entity, attribute, old, new, kwargs):
        self.d_loc = new
        if new != 'home':
            self.set_state("input_select.delia_fan_flag", state="Transition") #set to transition to ensure in correct state
            self.set_state("input_select.delia_fan_flag", state="Off")


    ###
    #   This sets the proximity through the proximity platform
    ###
    
    def arr_prox(self, entity, attribute, old, new, kwargs):
        
        self.sendmess = ""
        
        if new != "not_set":
            # leaving/arriving canberra region
            if entity == "proximity.home_simon":
                if self.get_state("input_select.trav_simon") == "Car":
                    if int(self.get_state("proximity.home_simon")) <= 1:
                        if self.get_state("sensor.s_travel_direction") == "towards":
                            # proximity under 1 kilometre, and arriving by car - open garage door
                            self.call_service("cover/open_cover", entity_id = "cover.near_garage_door")
                            self.sendmess = "Opening the Garage Door for Simon arriving by car (Proximity)"
                    #holiday
                    elif int(self.get_state("proximity.home_simon")) > 50:
                        if self.get_state("input_boolean.presence_holiday") == 'off':
                            self.turn_on('input_boolean.presence_holiday')
                            self.sendmess = "Car is going outside Canberra Region, messages around driving disabled"
                    #coming home from holiday
                    elif int(self.get_state("proximity.home_simon")) < 50:
                        if self.get_state("input_boolean.presence_holiday") == 'on':
                            self.turn_off('input_boolean.presence_holiday')
                            self.sendmess = "Car has returned to the Canberra Region, messages around driving enabled"
            elif entity == "proximity.home_meg":
                if self.get_state("input_select.trav_megan") == "Car":
                    if int(self.get_state("proximity.home_meg")) <= 1:
                        if self.get_state("sensor.m_travel_direction") == "towards":
                            # proximity under 1 kilometre, and arriving by car - open garage door
                            self.call_service("cover/open_cover", entity_id = "cover.near_garage_door")
                            self.sendmess = "Opening the Garage Door for Megan arriving by car (Proximity)"
                    #holiday
                    elif int(self.get_state("proximity.home_meg")) > 50:
                        if self.get_state("input_boolean.presence_holiday") == 'off':
                            self.turn_on('input_boolean.presence_holiday')
                            self.sendmess = "Car is going outside Canberra Region, messages around driving disabled"
                    #coming home from holiday
                    elif int(self.get_state("proximity.home_meg")) < 50:
                        if self.get_state("input_boolean.presence_holiday") == 'on':
                            self.turn_off('input_boolean.presence_holiday')
                            self.sendmess = "Car has returned to the Canberra Region, messages around driving enabled"
            
    ###
    #   watches the tasker proximity for Simon & Megan and if they are in the car, open the garage door
    ###
    
    def arr_task(self, entity, attribute, old, new, kwargs):
 
        self.sendmess = ""

        # arriving home - open garage door
        if entity == "input_boolean.simon_outback_home" and new == "on": #simon coming home via tasker
            if self.get_state("binary_sensor.drive_simon") == "on" and self.get_state("input_boolean.outback_just") == "off": #is driving and not just started the car
                self.call_service("cover/open_cover", entity_id = "cover.near_garage_door")
                self.sendmess = "Opening the Garage Door for Simon arriving by car (Tasker/Proximity)"
        elif entity == "input_boolean.megan_outback_home" and new == "on": #simon coming home via tasker
            if self.get_state("binary_sensor.drive_meg") == "on" and self.get_state("input_boolean.outback_just") == "off": #is driving and not just started the car
                self.call_service("cover/open_cover", entity_id = "cover.near_garage_door")
                self.sendmess = "Opening the Garage Door for Megan arriving by car (Tasker/Proximity)"
                        
        #send the message
        if self.sendmess != "":
            self.notifier.notify(self.sendmess)

    ###
    #   watches the connection to the car and send the appropriate message
    ###

    def con_car(self, entity, attribute, old, new, kwargs):
        
        self.sendmess = ""

        # only do this if the car is in the canberra region
        if self.away_flag == "off":

            if entity == 'binary_sensor.drive_meg' and new == 'on':
                # build a message for Meg being in the car
                self.sendmess = "Megan is now driving, use text messages if you need to contact her. " + "\n"
                # if at home, show the distances to others and to work
                if self.m_loc != "home":
                    self.sendmess += self.hmess + self.get_state("sensor.m_to_h_route") + "\n"
                else:
                    self.sendmess += self.wmess + self.get_state("sensor.m_to_w_route") + "\n"

                if self.s_loc != "home": # if not at home, show directions if they are more than 5 minutes away
                    if int(self.get_state("sensor.waze_meg_to_simon")) >= 5:
                        self.sendmess += self.smess + self.s_loc + self.t_mess + self.get_state("sensor.waze_meg_to_simon") + self.e_mess + self.get_state("sensor.m_to_s_route") + "\n"
                if self.st_loc != "home":
                    if int(self.get_state("sensor.waze_meg_to_staci")) >= 5:
                        self.sendmess += self.stmess + self.st_loc + self.t_mess + self.get_state("sensor.waze_meg_to_staci") + self.e_mess + self.get_state("sensor.m_to_st_route") + "\n"
                if self.d_loc != "home":
                    if int(self.get_state("sensor.waze_meg_to_delia")) >= 5:
                        self.sendmess += self.dmess + self.d_loc + self.t_mess + self.get_state("sensor.waze_meg_to_delia") + self.e_mess + self.get_state("sensor.m_to_d_route") + "\n"
            
            elif entity == 'binary_sensor.drive_simon' and new == 'on':
                # build a message for Meg being in the car
                self.sendmess = "Simon is now driving, use text messages if you need to contact him. " + "\n"
                # if at home, show the distances to others and to work
                if self.s_loc != "home":
                    self.sendmess += self.hmess + self.get_state("sensor.s_to_h_route") + "\n"
                else:
                    self.sendmess += self.umess + self.get_state("sensor.s_to_w_route") + "\n"

                if self.m_loc != "home": # if not at home, show directions if they are more than 5 minutes away
                    if int(self.get_state("sensor.waze_meg_to_simon")) >= 5:
                        self.sendmess += self.mmess + self.m_loc + self.t_mess + self.get_state("sensor.waze_meg_to_simon") + self.e_mess + self.get_state("sensor.m_to_s_route") + "\n"
                if self.st_loc != "home":
                    if int(self.get_state("sensor.waze_simon_to_staci")) >= 5:
                        self.sendmess += self.stmess + self.st_loc + self.t_mess + self.get_state("sensor.waze_simon_to_staci") + self.e_mess + self.get_state("sensor.s_to_st_route") + "\n"
                if self.d_loc != "home":
                    if int(self.get_state("sensor.waze_simon_to_delia")) >= 5:
                        self.sendmess += self.dmess + self.d_loc + self.t_mess + self.get_state("sensor.waze_simon_to_delia") + self.e_mess + self.get_state("sensor.s_to_d_route") + "\n"
                
            #send the message
            if self.sendmess != "":
                self.notifier.notify(self.sendmess)


    ###
    #   These set the input select to what we believe is the correct function at the time.
    ###
    def meg_trav(self, entity, attribute, old, new, kwargs):
        
        self.sendmess = ""

        ### Showing as just arrived home
        if self.get_state("input_select.trav_megan") != 'Home' and self.get_state("person.megan") == 'home' and self.get_state('binary_sensor.drive_meg') == 'off':
            # if both of these are true then Meg must have just arrived home (as the sensors are only true when not_home)
            # check if by car or by foot, and unlock the appropriate door
            if self.get_state("input_select.trav_megan") == "Car":
                # arrived by car
                # unlock the garage rear entry door
                self.turn_off("input_boolean.gdoor")
                self.sendmess = 'Welcome home Megan, I am ensuring the garage entry door is unlocked for you.' 
            elif self.get_state("input_select.trav_megan") == "Walk":
                # arrived by walking
                # unlock the front door
                self.turn_off("input_boolean.fdoor")
                self.sendmess = 'Welcome home Megan, I am ensuring the front door is unlocked for you.'

            # set Megan to being at home
            self.set_state("input_select.trav_megan", state="Home")

        ### showing in the car (may be called when a passenger or the driver, but as it only sets the state no issue)
        elif self.get_state("binary_sensor.megan_car") == 'on':
            
            # set Megan to being in the car, either by herself or in the car with Simon)
            self.set_state("input_select.trav_megan", state="Car")

        ### Showing walking or catching the bus, nothing specific here now 
        elif self.get_state("binary_sensor.megan_walkbus") == 'on':
            
            #wait for a time to ensure not yet at home when you disconnect from the car
            self.handle = self.run_in(self.meg_walk, 180, **kwargs)

        #send the message
        if self.sendmess != "":
            self.notifier.notify(self.sendmess)
        
    def meg_walk(self, entity, attribute, old, new, kwargs):

        if self.get_state("input_select.trav_megan") != 'Home' and self.get_state("binary_sensor.megan_walkbus") == 'on':
            # set Megan to being walking
            self.set_state("input_select.trav_megan", state="Walk")


    def sim_trav(self, entity, attribute, old, new, kwargs):
        
        self.sendmess = ""
        
        ### Showing as just arrived home
        if self.get_state("input_select.trav_simon") != 'Home' and self.get_state("person.simon") == 'home' and self.get_state('binary_sensor.drive_simon') == 'off':
            # if both of these are true then Simon must have just arrived home (as the sensors are only true when not_home)
            # check if by car or by foot, and unlock the appropriate door
            if self.get_state("input_select.trav_simon") == "Car":
                # arrived by car
                # unlock the garage rear entry door
                self.turn_off("input_boolean.gdoor")
                self.sendmess = 'Welcome home Simon, I am ensuring the garage entry door is unlocked for you.' 
            elif self.get_state("input_select.trav_simon") == "Walk":
                # arrived by walking
                # unlock the front door
                self.turn_off("input_boolean.fdoor")
                self.sendmess = 'Welcome home Simon, I am ensuring the front door is unlocked for you.' 

            # set Simon to being at home
            self.set_state("input_select.trav_simon", state="Home")

        ### showing in the car (may be called when a passenger or the driver, but as it only sets the state no issue)
        elif self.get_state("binary_sensor.simon_car") == 'on':

            # set Simon to being in the car, either by herself or in the car with Megan)
            self.set_state("input_select.trav_simon", state="Car")

        ### Showing walking or catching the bus, nothing specific here now 
        elif self.get_state("binary_sensor.simon_walkbus") == 'on':

             #wait for a time to ensure not yet at home when you disconnect from the car
            self.handle = self.run_in(self.sim_walk, 180, **kwargs)

        #send the message
        if self.sendmess != "":
            self.notifier.notify(self.sendmess)
      
    def sim_walk(self, entity, attribute, old, new, kwargs):

        if self.get_state("input_select.trav_simon") != 'Home' and self.get_state("binary_sensor.simon_walkbus") == 'on':
            # set Simon to being walking
            self.set_state("input_select.trav_simon", state="Walk")

    def sta_trav(self, entity, attribute, old, new, kwargs):
        
        self.sendmess = ""

        ### Showing as just arrived home
        if self.get_state("input_select.trav_staci") != 'Home' and self.get_state("person.staci") == 'home':
            # if both of these are true then Staci must have just arrived home (as the sensors are only true when not_home)
            # check if by car or by foot, and unlock the appropriate door
            if self.get_state("input_select.trav_staci") == "Car":
                # arrived by car
                # unlock the garage rear entry door
                #self.turn_off("input_boolean.gdoor")
                self.sendmess = 'Welcome home Staci, you have come by car, so I am assuming the doors will be unlocked by another person.' 
            elif self.get_state("input_select.trav_staci") == "Walk":
                # arrived by walking
                # unlock the front door
                self.turn_off("input_boolean.fdoor")
                self.sendmess = 'Welcome home Staci, I am ensuring the front door is unlocked for you.' 

            # set Staci to being at home
            self.set_state("input_select.trav_staci", state="Home")

        ### showing in the car (may be called when a passenger or the driver, but as it only sets the state no issue)
        elif self.get_state("binary_sensor.staci_car") == 'on':           

            # set Staci to being in the car, either by herself or in the car with Simon/Megan)
            self.set_state("input_select.trav_staci", state="Car")

        ### Showing walking or catching the bus, nothing specific here now 
        elif self.get_state("binary_sensor.staci_walkbus") == 'on':

            # set Megan to being walking
            self.set_state("input_select.trav_staci", state="Walk")
        

        #send the message
        if self.sendmess != "":
            self.notifier.notify(self.sendmess)


    def del_trav(self, entity, attribute, old, new, kwargs):
        
        self.sendmess = ""

        ### Showing as just arrived home
        if self.get_state("input_select.trav_delia") != 'Home' and self.get_state("person.delia") == 'home':
            # if both of these are true then Delia must have just arrived home (as the sensors are only true when not_home)
            # check if by car or by foot, and unlock the appropriate door
            if self.get_state("input_select.trav_delia") == "Car":
                # arrived by car
                # unlock the garage rear entry door
                #self.turn_off("input_boolean.gdoor")
                self.sendmess = 'Welcome home Delia, you have come by car, so I am assuming the doors will be unlocked by another person.' 
            elif self.get_state("input_select.trav_delia") == "Walk":
                # arrived by walking
                # unlock the front door
                self.turn_off("input_boolean.fdoor")
                self.sendmess = 'Welcome home Delia, I am ensuring the front door is unlocked for you.' 

            # set Delia to being at home
            self.set_state("input_select.trav_delia", state="Home")

        ### showing in the car (may be called when a passenger or the driver, but as it only sets the state no issue)
        elif self.get_state("binary_sensor.delia_car") == 'on':

            # set Delia to being in the car, either by herself or in the car with Simon/Megan)
            self.set_state("input_select.trav_delia", state="Car")

        ### Showing walking or catching the bus, nothing specific here now 
        elif self.get_state("binary_sensor.delia_walkbus") == 'on':

            # set Delia to being walking
            self.set_state("input_select.trav_delia", state="Walk")
        
        #send the message
        if self.sendmess != "":
            self.notifier.notify(self.sendmess)
        

    





       


   

   
                

