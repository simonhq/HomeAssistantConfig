#
#The aim of this is to do all the notifiers based on putting them in the calendar when they are happening and the notifiers running hours or days before
#Fluff #CalendarFlag
#

import appdaemon.plugins.hass.hassapi as hass
import time
import globals

class CalendarNotifier(hass.Hass):
    
    # message offsets in days for each event - can move these to the apps.yaml...
    binc = 1
    skipc = 1
    greenc = 1 
    danddc = 8
    recyclec = 1
    cleanerc = 1
    # month counts to calc offsets
    months = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    
    # messages
    bmessage = "Bin pick up is tomorrow, can it be put out please, Thanks!"
    cmessage = "Tony is coming to clean tomorrow! tidy up please"
    rmessage = "Recycling pick up is tomorrow, can it be put out please, Thanks!"
    gmessage = "Green Waste pick up is tomorrow, can it be put out please, Thanks!"
    smessage = "Skip Bin pick up is tomorrow, anything to go out?"
    cmessage_issue = "Couldn't recognise person to cook, setting 'Easy'"
    hotmessage = "It will be hot today, you may want to consider the cooling."
    omessage = ""
    mmessage = ""
    dtitle = ""

    def initialize(self):

        # bring in the messaging module
        self.notifier = self.get_app('messaging')

        #cooking
        self.listen_state(self.cook_flag, "sensor.cook_calendar")
        #messaging
        self.listen_state(self.messages, "input_boolean.send_message", new = "on")
        
   
    def cook_flag(self, entity, attribute, old, new, kwargs):
        v = self.get_state("sensor.cook_calendar")
        #self.log(v)
        cook = v[0:2]
        #self.log(cook)
        if cook == "Si" or cook == "si":
            self.set_state("input_select.cooking", state="Simon")
        elif cook == "Me" or cook == "me":
            self.set_state("input_select.cooking", state="Megan")
        elif cook == "St" or cook == "st":
            self.set_state("input_select.cooking", state="Staci")
        elif cook == "De" or cook == "de":
            self.set_state("input_select.cooking", state="Delia")
        elif cook == "Ea" or cook == "ea":
            self.set_state("input_select.cooking", state="Easy")
        elif cook == "Go" or cook == "go":
            self.set_state("input_select.cooking", state="Going Out")
    
    def messages(self, entity, attribute, old, new, kwargs):

        dayw = time.strftime("%a")
        dayn = int(time.strftime("%d"))
        daym = int(time.strftime("%m"))
        self.omessage = ""

        #- sensor.bin_calendar
        if self.checker(self.get_state("sensor.bin_calendar"), dayw, dayn, daym, self.binc) == True:
            self.omessage += self.bmessage + "\n"
            
        #- sensor.cleaner_calendar
        if self.checker(self.get_state("sensor.cleaner_calendar"), dayw, dayn, daym, self.cleanerc) == True:
            self.omessage += self.cmessage + "\n"
            
        #- sensor.recycling_calendar
        if self.checker(self.get_state("sensor.recycling_calendar"), dayw, dayn, daym, self.recyclec) == True:
            self.omessage += self.rmessage + "\n"
            
        #- sensor.greenwaste_calendar
        if self.checker(self.get_state("sensor.greenwaste_calendar"), dayw, dayn, daym, self.greenc) == True:
            self.omessage += self.gmessage + "\n"
            
        #- sensor.skipbin_calendar
        if self.checker(self.get_state("sensor.skipbin_calendar"), dayw, dayn, daym, self.skipc) == True:
            self.omessage += self.smessage + "\n"

        #- sensor.climate_warn_hot
        if self.get_state("binary_sensor.climate_warn_hot") == 'on':
            self.omessage += self.hotmessage + "\n"
        

        #- sensor.dandd_calendar
        if self.checker(self.get_state("sensor.dandd_calendar"), dayw, dayn, daym, self.danddc) == True:
            self.dtitle = "Session " + self.get_state("sensor.dandd_calendar")
            self.messager("DD")
        
        # morning message
        self.buildmorning()
        self.messager("Morning")

        #set the check flag back off after sending messages
        self.turn_off("input_boolean.send_message")

    # split the sensor to get the day, day month values
    # Thu 01/04 
    # 012345678
    def splitcaldayw(self, calstr):
        #self.log(weekday)
        weekday = list(calstr)
        wday = weekday[0] + weekday[1] + weekday[2]
        return wday

    def splitcaldayn(self, calstr):
        #self.log(calstr)
        day = list(calstr)
        wday = day[4] + day[5]
        return int(wday)

    def splitcaldaym(self, calstr):
        day = list(calstr)
        wday = day[7] + day[8]
        return int(wday)
    
    def buildmorning(self):
        self.mmessage = "Good Morning, \n\n"
        self.mmessage += self.omessage
        self.mmessage += "Cooking Tonight: " + self.get_state("input_select.cooking") + "\n\n"        
        self.mmessage += "Weather today: \n"
        self.mmessage += "Min/Max: " + self.get_state("sensor.dark_sky_overnight_low_temperature_0d") + "/" + self.get_state("sensor.dark_sky_daytime_high_temperature_0d") + "\n"
        self.mmessage += "Chance of Rain: " + self.get_state("sensor.dark_sky_precip_probability_0d") + "\n"
        self.mmessage += "Windspeed: " + self.get_state("sensor.dark_sky_wind_speed_0d") + "\n"
        self.mmessage += "UV Index: " + self.get_state("sensor.dark_sky_uv_index_0d") + "\n"
        self.mmessage += "\nHave a great day"
        #self.log(self.mmessage)

    # send a message self.call_service(“notify/a_notifier”,message=“blabla”)
    # dayw, dayn, daym is today
    # sdayw, sdayn, sdaym is the next event
    # if the event is the right number of days (see offsets at top) then send the message

    #checking
    def checker(self, calstr, dayw, dayn, daym, offset_data):
        
        sendmessage = False
        # check if the bin is tomorrow, if so send message
        if calstr != "None":
            sdayw = self.splitcaldayw(calstr)
            sdayn = self.splitcaldayn(calstr)
            sdaym = self.splitcaldaym(calstr)
            
            # over month check logic - this will be wrong for leap year events that fall over the 29th with offset... I am willing to accept that one day wrong for the notifiers
            # event is 4/5 + 30 (for april, current month) = 34
            # current date is 26/4 + 8 (for offset) = 34     

            if sdaym == daym: #same month
                if sdayn == dayn + offset_data: #event day is today + offset (event 11, today 10 + offset 1)
                    sendmessage = True #then we will send the message
            elif sdaym != daym: #not the same month 
                if sdaym == daym + 1: #event next month (but could be tomorrow)
                    if sdayn + int(self.months[daym]) == dayn + offset_data: #if event date + current month equals the current date + offset - then the send the message
                        sendmessage = True #send the message
            
            #bstr = str(sdayn) +" "+ str(self.months[daym]) +" "+ str(dayn) +" "+ str(offset_data) +" "+ str(sendmessage)
            #self.log(bstr)

        return sendmessage

    #messaging
    def messager(self, mtype):
        
        if mtype == "DD":
            self.log("dandd message")
            self.notifier.notify(self.dtitle, True)
        elif mtype == "Morning":
            self.log(self.mmessage)
            self.notifier.notify(self.mmessage)
        else:
            self.log("Unknown Message Call")
            self.notifier.notify("Unknown Message Call")

