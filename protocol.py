import threading
from time import sleep, time
import socket
import random 

import packet
from conf import *	
from timer import Timer


class Protocol:
	def __init__(self, window_size=4):
		self.packets_buffer = []
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.mutex = threading.Lock()
		self.send_timer = Timer(TIMEOUT_INTERVAL)
		self.base = 0
		self.window_size = window_size
		self.with_lost_packets_simulation = True
	
	def set_window_size(self, num_packets):
		return min(self.window_size, num_packets - self.base)

	# Send a packet across the unreliable channel
	# Packet may be lost
	def send_packet(self, packet, addr):
		seq_num, _ = packet.extract(packet)
		if self.with_lost_packets_simulation:
			if random.randint(0, DROP_PROB) > 0:
				print('packet %d dont lost in simulation' % seq_num)
				self.socket.sendto(packet, addr)
		else:
			print('packet %d lost in simulation', seq_num)
		return
	
	# Receive a packet from the unreliable channel
	def recv_packet(self):
		packet, addr = self.socket.recvfrom(1024)
		return packet, addr
	
	def send_file(self, filename):
		start = time()
		try:
		    _file = open(filename, 'rb')
		except IOError:
		    print('Unable to open', filename)
		    return
		
		# Add all the packets to the buffer
		seq_num = 0
		while True:
			data = _file.read(PACKET_SIZE)
			if not data:
				break
			self.packets_buffer.append(packet.make(seq_num, data))
			seq_num += 1

		num_packets = len(self.packets_buffer)
		print('I gots', num_packets)
		next_to_send = 0
		window_size = self.set_window_size(num_packets)

		# Start the receiver thread
		t = threading.Thread(target=self.receive_worker_client)
		t.start()

		while self.base < num_packets:
			self.mutex.acquire()
			# Send all the packets in the window
			while next_to_send < self.base + window_size:
				print('Sending packet', next_to_send)
				self.send_packet(self.packets_buffer[next_to_send], RECEIVER_ADDR)
				next_to_send += 1

			# Start the timer
			if not self.send_timer.running():
				print('Starting timer')
				self.send_timer.start()

			# Wait until a timer goes off or we get an ACK
			while self.send_timer.running() and not self.send_timer.timeout():
				self.mutex.release()
				print('Sleeping')
				sleep(SLEEP_INTERVAL)
				self.mutex.acquire()

			if self.send_timer.timeout():
				# Looks like we timed out
				print('Timeout')
				self.send_timer.stop()
				next_to_send = self.base
			else:
				print('Shifting window')
				window_size = self.set_window_size(num_packets)
			self.mutex.release()
		
		self.send_packet(packet.make_empty(), RECEIVER_ADDR)
		end = time()
		time_to_send_all = end - start
		print('time to send all packets: %.2f' % time_to_send_all)
		_file.close()
		# Receive packets from the sender
	def receive_worker_client(self):

		while True:
			pkt, _ = self.recv_packet();
			ack, _ = packet.extract(pkt);

			# If we get an ACK for the first in-flight packet
			print('Got ACK', ack)
			if (ack >= self.base):
				self.mutex.acquire()
				self.base = ack + 1
				print('Base updated', self.base)
				self.send_timer.stop()
				self.mutex.release()
	
	def __generate_filename(self):
		import string
		return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in 
		range(SIZE_RANDOM_FILENAME))

	def receive_worker_server(self):
		# Open the file for writing
		filename = self.__generate_filename()
		try:
			_file = open(filename, 'wb')
		except IOError:
			print('Unable to open', filename)
			return
		
		expected_num = 0
		while True:
			# Get the next packet from the sender
			pkt, addr = self.recv_packet()
			if not pkt:
				break
			seq_num, data = packet.extract(pkt)
			print('Got packet', seq_num)
			
			# Send back an ACK
			if seq_num == expected_num:
				print('Got expected packet')
				print('Sending ACK', expected_num)
				pkt = packet.make(expected_num)
				self.send_packet(pkt,  addr)
				expected_num += 1
				_file.write(data)
			else:
				print('Sending ACK', expected_num - 1)
				pkt = packet.make(expected_num - 1)
				self.send_packet(pkt, addr)

		_file.close()

		# Send empty packet as sentinel
		self.send_packet(packet.make_empty(), RECEIVER_ADDR)
	
	def run_server(self, client_address=None):
		if client_address is None:
			client_address = RECEIVER_ADDR
		
		self.socket.bind(client_address)
		print('server running %s:%d' % (client_address[0], client_address[1]))
		self.receive_worker_server()	
		self.socket.close()

	


	
		
		
