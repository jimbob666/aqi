# aqi
This is based on this project https://openschoolsolutions.org/measure-particulate-matter-with-a-raspberry-pi/


The addtional features include the following
*1. Remote JSON File* 
Copies .json files to GitHub page after each run. This allows for the viewing web UI to be viewed from anywhere. 

*2. Google Doc Support*
Each time the script runs it logs the results to a Google sheet. This allows you to chart over time how good or bad the air quality is. Also allows you to add notes to groups or runs like (Ran from person X's house)

*3. IFTTT Support*
If the AQI reaches a certain threashold it send a WebHook event to IFFF to do things like turn your Nest Fan on or maybe a WebMo plug on to turn on (Or off) a Hepa Filter. 

*4. External & Internal IP*
If going to run in different locations having the internal or etxernal IP can be usful to help geo locate where the reading was taken or based on a certin IP or location to do something different. For example if running from home then IFTT will trigger Nest fan where if elsewhere you may not want this. 

