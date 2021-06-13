import socket
import os
import sys
import time
from colorama import init, Fore

init(autoreset=True)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
help = '''
Usage example: 'python3 client.py -l <connect ip> -p <connect port>'
'''

def client_info():
        try:
                return str(sys.argv[int(sys.argv.index("-l") + 1)]), int(sys.argv[int(sys.argv.index("-p") + 1)])

        except ValueError as e:
                print(Fore.RED + "[!] Invalid parameters")
                print(Fore.GREEN + f"{help}\n")
                print(e)

def connect():
	client.connect((ip, port))
	connected = True
	print(Fore.CYAN + f"[+] Succefully connected to {ip} !")
	while connected:
		command = input(f"#{ip}> ")
		client.send(command.encode('utf-8'))
		data = client.recv(2048).decode('utf-8')
		print(Fore.YELLOW + f"{data}")
		write_info(command, data)
		if command == 'exit':
			connected = False
	client.close()

def write_info(command, result):
	with open("result.txt", "a") as file:
		file.write(f"<{time.asctime()}>: {command}\n{result}\n\n")


if __name__ == "__main__":
        try:
                ip, port = client_info()
                connect()

        except OSError as e:
                print(Fore.RED + "[!] The requested ip address or port number is invalid\n")
                print(Fore.RED + e)

