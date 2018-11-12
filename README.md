<h2>RPI Air Quality Index (AQI) Project</h2>
This is based on the below project by Stephan from https://openschoolsolutions.org.<br>
https://openschoolsolutions.org/measure-particulate-matter-with-a-raspberry-pi/<br>


Below are some additional features not included in the above project.<br>

**1. Remote JSON File**<br>
Copies .json files to GitHub page after each run. This allows viewing of the web UI from anywhere as well as a bookmarkable page. 

**2. Google Doc Support**<br>
Each time the script runs it logs the results to a Google sheet. This allows you to chart over time how good or bad the air quality is. Also allows you to add notes to groups or runs like (Ran from person X's house)

**3. IFTTT Support**<br>
If the AQI reaches a certain threshold it send a WebHook event to IFFF to do things like turn your Nest Fan on or maybe a WebMo plug on to turn on (Or off) a Hepa Filter. 

**4. External & Internal IP**<br>
If going to run in different locations having the internal or external IP can be useful to help geo locate where the reading was taken or based on a certain IP or location to do something different. For example if running from home then IFTTT will trigger Nest fan where if elsewhere you may not want this. 

TIP: If connecting to the RPI and you don't know the IP you can SSH, VNC, or http to it by its host name like below (assuming you are on the same network)<br>
*ssh pi@rpizw.local.* or ssh http://rpizw.local./aqi/index.html

<br><br><br>

**Parts**<br>
$5 RPI Zero W<br>
Things I had lying around that you may still need, 16gig mem card, USB power cord, USB battery, and for setup only micro HDMI and keyboard/mouse)<br>
https://www.microcenter.com/product/486575/raspberry-pi-zero-w

$1 USB Female to Micro USB (Needed for the Air sensor USB to plug into the RPI Zero W)<br>
https://www.amazon.com/gp/product/B071GTTW42/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1

$26 Air Sensor<br>
https://www.amazon.com/gp/product/B07H1SJ819/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1
<br><br>

**Optional Parts**<br>
$20 WeMo Smart Plug (To trigger turning on something like a hepa filter)<br>
https://www.amazon.com/Wemo-Smart-F7C063-RM2-Certified-Refurbished/dp/B079XWTJNH/ref=sr_1_6?s=lamps-light

$200 Nest Thermostat (Also to trigger the house fan to help clean the air)<br>
https://www.amazon.com/Nest-T3007ES-Thermostat-Temperature-Generation/dp/B0131RG6VK/ref=sr_1_4?s=hi&ie=UTF8

$16 Box Fan (Also to trigger to help clean the air)<br>
https://www.amazon.com/Lasko-3733-20-Fan-Box/dp/B00002ND67/ref=sr_1_6?s=hi&ie=UTF8

$51 Air Filter 20x20x1 MERV 13 - Box of 6 (Tape to the box fan)<br>
https://www.amazon.com/gp/product/B01HTL3W02/ref=oh_aui_search_detailpage?ie=UTF8&psc=1
<br><br><br>

**Images**<br>
RPI Zero + Air Sensor Setup (Optional standard USB battery)<br>
<img src=https://raw.githubusercontent.com/jimbob666/aqi/master/images/RPI_AQI.png height="50%" width="50%">

Optional Hepa Box Fan<br>
<img src=https://raw.githubusercontent.com/jimbob666/aqi/master/images/Box%20Fan%20Hepa%20Filter.png height="50%" width="50%">

