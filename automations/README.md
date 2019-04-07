# Rushbrook Overlook Automations

I use a mix of HA Automations and Appdaemon python code to automate functionality. 

Here is an overview of the logic of some of the HA Automation.

## Motion Lights

* I have a number of rooms with motion sensors in them, bathrooms, laundry and garage. While I want the lights to be on while people are using them, I also want to ensure that we are using electricity efficiently. Therefore I have setup the following logic to aim to use the lights only while the rooms are in use.

![Motion Lights](images/motionlights.png)

### Hardware in use

* [Hue](https://www2.meethue.com/en-au) Motion Sensor
* [Hue](https://www2.meethue.com/en-au) Lights

### State Variables in use

timer.yaml
* Room [Timer](https://www.home-assistant.io/components/timer/) - Actions {Start, Cancel} & Events {Finished} 

input_select.yaml
* Room [Input_Select](https://www.home-assistant.io/components/input_select/) - Allowed values 
    * 'Motion' - motion lights function, 
    * 'On' - lights stay on, 
    * 'Off' - lights stay off.
* Time [Input_Select](https://www.home-assistant.io/components/input_select/) - See Time modes for more details
    * 'Morining', 'Day', 'Evening', 'Night' 

input_boolean.yaml
* Room [Input_Boolean](https://www.home-assistant.io/components/input_boolean/) - The current state for the lights
    * 'On' - there has been motion in the room, 
    * 'Off' - there has not been motion in the room for the length of the timer.

sensor.yaml
* [Rest](https://www.home-assistant.io/components/sensor.rest/) Sensor to see the current motion sensor - motion value
* [Rest](https://www.home-assistant.io/components/sensor.rest/) Sensor to see the current motion sensor - lux value

### known issues

* The Hue rest sensor's lux reading is not reading the value often enough to allow for the lux to be used efficiently so I have chosen lux numbers that are higher than the number that the reading shows when the lights are on in the room, otherwise, the reading will be held from when the lights were on, and the system will not turn on the lights because it thinks it is already well lit in the room, meaning you stand in the dark waving your arms for 5 minutes waiting for it to do another lux reading.
* I had transferred this logic into Appdaemon but with the extra lag from passing the settings, it was taking too long for the lights to turn on, so I moved it back into HA Automation, which is much more code, but runs much faster.


