import socket
import threading
import sys
import subprocess


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

help = '''
Usage example: 'python3 server.py -l <listen ip> -p <listen port>'
'''


def server_info():
	try:
		return sys.argv[int(sys.argv.index("-l") + 1)], int(sys.argv[int(sys.argv.index("-p") + 1)])
	except ValueError as e:
		print("[!] Invalid parameters")
		print(f"{help}\n")
		print(e)


def handle_connection(conn):
	connected = True

	while connected:
		data = conn.recv(2048).decode('utf-8')
		print(data)
		if data=="exit":
			connected = False
		else:
			try:
				response = check_response(data)
				conn.send(response)
			except FileNotFoundError as e:
				conn.send(str(e).encode('utf-8'))
				print(e)
	conn.close()



def listen():
	server.listen()
	while True:
		try:
			conn, addr = server.accept()
			client = threading.Thread(target=handle_connection, args=[conn])
			client.start()
			print(f"[+] Client {addr} connected")
		except KeyboardInterrupt:
			server.close()
			exit()


def check_response(command):
	command = command.split()
	cmd = subprocess.check_output(command, stderr=subprocess.STDOUT)
	return cmd



if __name__ == "__main__":
	try:
		ip, port = server_info()
		server.bind((ip, port))
		listen()

	except OSError as e:
		print("[!] The requested ip address or port number is invalid\n")
		print(e)

