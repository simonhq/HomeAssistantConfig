
import appdaemon.plugins.hass.hassapi as hass
import datetime
import random
from pykevoplus import KevoLock
import globals

class DoorLock(hass.Hass):

    lock = ""
    kuser = ""
    kpass = ""
    sname = ""

    def initialize(self):
            
        #create and set instance variables
        self.lock = globals.get_arg(self.args, "lock_id")
        self.kuser = globals.get_arg(self.args, "k_user")
        self.kpass = globals.get_arg(self.args, "k_pass")
        self.sname = globals.get_arg(self.args, "select_name")

        self.a_lock = KevoLock.FromLockID(self.lock, self.kuser, self.kpass)
        self.select_name = 'input_boolean.' + self.sname

        # locked = on , unlocked = off

        #self.set_state(self.select_name, state= self.a_lock.GetBoltState())
        self.listen_state(self.changer,  self.select_name)
        ti_now = datetime.datetime.now()
        r_next = random.randint(4,9)
        self.log("Update " + self.sname + " every " + str(r_next) + " minutes")
        self.run_every(self.lock_status, ti_now, r_next * 60)
                  
    def changer(self, entity, attribute, old, new, kwargs):

        self.a_lock.StartSession()
        current = self.a_lock.GetBoltState()

        if new == "on" and current == "Unlocked":
            self.a_lock.Lock()
        elif new == "off" and current == "Locked":
            self.a_lock.Unlock()

        state = self.a_lock.GetBoltState()
        if state == "Locked":
            self.turn_on(self.select_name)
        elif state == "Unlocked":
            self.turn_off(self.select_name)
            
        self.a_lock.EndSession()
        
        self.log("change " + entity + " to " + new)

    def lock_status(self, kwargs):

        #get the state
        self.a_lock.StartSession()
        state = self.a_lock.GetBoltState()
        self.a_lock.EndSession()
        #set the lock state
        if state == "Locked":
            self.turn_on(self.select_name)
        elif state == "Unlocked":
            self.turn_off(self.select_name)
        #show in the log
        self.log(self.select_name + " status checked")
        