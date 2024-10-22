# Hacking Tools
Simple hacking tools written in Python

## ⚠️ DISCLAIMER ⚠️
**The tools provided in this repository are intended for educational purposes only. By using these tools, you acknowledge that you are responsible for your actions and any consequences that may arise from their use. The author does not endorse or condone any illegal or malicious activities. Use these tools at your own risk, and ensure that you have permission to test any systems or networks you interact with. The author disclaims any responsibility for any harm, damage, or legal issues that may result from the use of these tools.**

## Tools
- Port Scanner
	- V1: Fast but not powerful enough (could miss some ports)
	- V2: Powerful but not fast enough (could take a long time)

## How To Run
1. Clone this repo: `git clone https://github.com/BazarganDev/hacking-tools.git`
2. Install requirements: `pip install -r requirements.txt`
3. Run the script: `python SCRIPT_NAME.py`

## Where To Scan?
Since scanning ports on a host without a permission or authority is illegal in most cases, I recommend you to create a simple web server on your localhost with Python. Just go to the directory you want and create a HTTP server:<br>
```
~ cd DIRECTORY/FOR/CREATING/SERVER/
~ python -m http.server 8080
```
Now you can go to `http://localhost:8080` to check out your server. Now you can perform your hacking attempts on the localhost to avoid your IP being blacklisted on the internet or any other legal issues. 🙂

## ToDo
- [ ] Add a DDoS script
