import appdaemon.plugins.hass.hassapi as hass
import globals

class Messenger(hass.Hass):

    stnotify = "notify/push_staci"
    snotify = "notify/push_simon"
    mnotify = "notify/push_megan"
    dnotify = "notify/push_delia"      
    hnotify = "notify/push_hassio"
    
    enotify = "notify/email_dd"

    hangify = "notify/hang_home"

    discify = "notify/discord_thompson"
    dischook = "notify/discord_webhook"

    mess_platform = "Discord"

    #discord
    channel = ""
    userSimon = ""
    userMegan = ""
    userStaci = ""
    userDelia = ""

    dmessage = """
    Hi all,

    I am the Thompson-HQ Home Assistant and I would like to help organise your next D&D Session.
    I can't do much yet, but at least I can get you communicating!

    Who is available?
    
    Player      |   THA     |   Siobhan |   Martino |   Michael |   Wenche  |   Brian   |   Megan   |   Simon   |
    Avaiable    |   Y       |    
    Venue Pref  |   O       |              
    Campaign    |   Ma      |
    Food Pref   |   Other   |

    Venues (SM Siobhan & Martino's, WB Wenche & Brian's, KM Ksenia & Michael's, MS Megan & Simon's, O Online)
    Campaign (Pz Path to Zox, Dp Demon Pits, Ho Hobbitses, Am Amnesia, Ot games, Ma The Matrix)
    Foods (Pizza, Turkish, Thai, Chicken&Chips, Other) 
    
    Hopefully this finds you well, and good luck for your adventures!

    Yours in automation,

    Thompson-HQ Home Assistant :)"""


    def initialize(self):
        
        self.channel = globals.get_arg(self.args, "channel")
        self.userSimon = globals.get_arg(self.args, "userA")
        self.userMegan = globals.get_arg(self.args, "userB")
        self.userStaci = globals.get_arg(self.args, "userC")
        self.userDelia = globals.get_arg(self.args, "userD")

        #set messaging platform
        self.listen_state(self.mess_flag, "input_select.message_flag")

    def mess_flag(self, entity, attribute, old, new, kwargs):
        self.mess_platform = self.get_state("input_select.message_flag")

    def notify(self, mess, dd=False):
        if dd == True:
            self.call_service(self.enotify,title=mess,message=self.dmessage)
        else:
            if self.mess_platform == "Pushbullet":
                self.call_service(self.mnotify,message=mess)
                self.call_service(self.snotify,message=mess)
                self.call_service(self.dnotify,message=mess)
                self.call_service(self.stnotify,message=mess)
            elif self.mess_platform  == "Hangouts":
                self.call_service(self.hangify,message=mess)
            elif self.mess_platform  == "Discord":
                self.call_service(self.dischook,message=mess)
            elif self.mess_platform == "Discord_Component":
                self.call_service(self.discify,target=self.channel,message=mess)
