# thunderboard-reader
Read data over USB from the Silicon Labs Thunderboard Sense2 for plotting and saving to CSV


## Installation instructions

Check to see if your system already has python3:

* On MAC in a terminal type (and probably linux):
` python --version `

* On Windows in the Start menu type 'command' and select 'command prompt'. Type `python3 --version` in the command prompt. 

If you don't have python3 install it using these [Python downloads](https://www.python.org/downloads/). 
On Windows be sure to select "Add Python to System Path" during the installation.

Next we will use `pip` to install the Thunderboard package

In a terminal or Windows CMD prompt type:

```
pip install thunderboard-reader 
```

Alternatively if `pip` is not found as a command:
```
python3 -m pip install thunderboard-reader 
```

Connect the Thunderboard to your computer via USB. Next, launch the mobile phone app, connect to the thunderboard, and startup the environment sensing data. Then within the same terminal / command prompt try these commands. 

```
python tboard_read.py --help

python tboard_read.py --sensor Temp

python tboard_read.py --sensor all

python tboard_read.py --sensor eCO2 --time 5
```
On Windows you may need to be in the same directory as this script. To determine the directory you can type 
```
tboard_read.py
``` 


