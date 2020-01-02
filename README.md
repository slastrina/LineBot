# LineBot

* Install python 3.7+
* create an ngrok account and download latest binary
* pip install requirements file
* create line messaging api account
* two environment variables and populate them  
  * LINE_CHANNEL_SECRET  
  * LINE_CHANNEL_ACCESS_TOKEN  
* run tool 'python app.py'
* run ngrok on port 5000
* add endpoint to your line app channel i.e. https://d989404f.ngrok.io/callback
* click verify, verification should pass and your good to go.

Commands:  
* sambot
* sambot hello <name>
* sambot ead <name>
* sambot praise <name>
* sambot scold <name>
* sambot nuke
* sambot russian_roulette
* sambot decide_for_us <option1> <option2> <option#>
* sambot tell_me_a_joke <neutral|chuck|all>
* sambot translate <fromlang> <tolang> <content> (https://ctrlq.org/code/19899-google-translate-languages)