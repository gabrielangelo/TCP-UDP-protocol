import threading
from time import sleep, time
import socket
import random 
import pickle

from conf import *	
from timer import Timer
from packet import Packet


class Protocol:
	def __init__(self, window_size=4, timeout=1,lost_packets_simulation=True, 
	checksum_error_simulation=True, receiver_addr=None):
		self.packets_buffer = []
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.mutex = threading.Lock()
		self.send_timer = Timer(timeout)
		self.base = 0
		self.window_size = window_size
		self.with_lost_packets_simulation = lost_packets_simulation
		self.with_checksum_error_simulation = checksum_error_simulation
		self.kill_receiver_client = False
		self.receiver_addr = RECEIVER_ADDR if receiver_addr is None else receiver_addr 

	@staticmethod
	def checksum(strData):
		strData = strData.decode('utf-8') if type(strData) == bytes else strData
		chksum = 0
		chksum = chksum	^ (int(str(int("20", 16)), 10))
		chksum = chksum	^ (int(str(int("03", 16)), 10))
		for char in strData:
			chksum = chksum ^ ord(char)
		chksum = chksum	^ (int(str(int("04", 16)), 10))
		return chksum

	def checksum_packet_is_valid(self, pkt):
		checksum_packet = pkt.checksum
		cmp_checksum = self.checksum(pkt.data)
		return True if checksum_packet == cmp_checksum else False
	 
	def set_window_size(self, num_packets):
		return min(self.window_size, num_packets - self.base)

	# Send a packet across the unreliable channel
	# Packet may be lost
	# bad implementation !!
	def send_packet(self, packet, addr):
		if self.with_lost_packets_simulation:
			if random.randint(0, DROP_PACKET_PROB) > 0:
				if self.with_checksum_error_simulation:
					if random.randint(0, DROP_PACKET_CHECKSUM) == 0:
						if packet.checksum:
							packet.checksum+=random.randint(0, DROP_PACKET_CHECKSUM)
						print('packet send with incorret checksum')
				self.socket.sendto(pickle.dumps(packet), addr)
			else:
				if packet.ack:
					print('packet %d lost in simulation' % packet.ack)
				elif packet.seq_num:
					print('packet %d lost in simulation' % packet.seq_num)
				elif packet.is_empty:
					print('empty pack lost in simulation')
		else:
			self.socket.sendto(pickle.dumps(packet), addr)
			
	# Receive a packet from the unreliable channel
	def recv_packet(self):
		data, addr = self.socket.recvfrom(1024)
		packet = pickle.loads(data)
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
			packet = Packet.make(seq_num, data, checksum=self.checksum)
			print('packet seqnum ->', packet.seq_num)
			self.packets_buffer.append(packet)#packet.make(seq_num, data))
			seq_num += 1
		
		# set last packet like final packet
		self.packets_buffer[-1].end = True
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
				self.send_packet(self.packets_buffer[next_to_send], self.receiver_addr)
				next_to_send += 1
					
			# Start the timer
			if not self.send_timer.running():
				print('Starting timer')
				self.send_timer.start()

			# Wait until a timer goes off or we get an ACK
			while self.send_timer.running() and not self.send_timer.timeout():
				self.mutex.release()
				# print('Sleeping')	
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
		
		self.send_packet(packet.make(), self.receiver_addr)
		end = time()
		time_to_send_all = end - start	
		print('time to send all packets(RTT): %.2f ms' % time_to_send_all)
		_file.close()
	
	# Receive packets from the sender
	def receive_worker_client(self):
		while not self.kill_receiver_client:
			packet_received, _ = self.recv_packet()
			ack = packet_received.ack 
			size_buffer = len(self.packets_buffer)
			if packet_received.end:
				print('break')
				self.kill_receiver_client=True
			# If we get an ACK for the first in-flight packet
			print('Got ACK', ack) 
			if (ack is not None and ack >= self.base):
				self.mutex.acquire()
				self.base = ack + 1
				print('Base updated', self.base)
				self.send_timer.stop()
				self.mutex.release()
		return 
	
	# optional function to assigment random name to file
	def _generate_filename(self):
		import string
		return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in 
		range(SIZE_RANDOM_FILENAME))

	def receive_worker_server(self):
		from io import StringIO, BytesIO
		import datetime
		
		stream = BytesIO()
		expected_num = 0
		data_to_put = None

		while True:
			# Get the next packet from the sender
			end_stream_transfer = False
			while not end_stream_transfer:
				packet_received, addr = self.recv_packet()
				if not packet_received:
					break

				# packet_received = pkt
				seq_num, data = packet_received.seq_num, packet_received.data
				
				print('Got packet', seq_num)
				
				# Send back an ACK
				if seq_num == expected_num and not self.checksum_packet_is_valid(packet_received):
					print('Got expected packet')
					print('Sending ACK', expected_num)
					packet = Packet.make(ack=expected_num)
					if packet_received.end:
						end_stream_transfer = True
						packet.end=True
					# self.send_packet(packet, addr)
					self.socket.sendto(pickle.dumps(packet), addr)
					expected_num += 1	
					stream.write(data)
					data_to_put = stream.getvalue()
				else:
					if not self.checksum_packet_is_valid(packet_received) and packet_received.seq_num:
						print('checksum error in packet sequence %d' % packet_received.seq_num)
					print('Sending last ACK', expected_num - 1)
					packet = Packet.make(ack=expected_num - 1)
					# self.send_packet(packet_received, addr)
					self.socket.sendto(pickle.dumps(packet), addr)
			
			# Open the file for writing
			date_file_name = datetime.datetime.now().strftime("%Y-%m-%d  %I:%M:%S")
			filename = 'data-receive-from %s in ' % addr[0]  +  date_file_name
			if end_stream_transfer:
				try:
					_file = open(filename, 'wb')
					_file.write(data_to_put)
					_file.close()
					stream = BytesIO()
					expected_num = 0
					data_to_put = None
					end_stream_transfer = False
				except IOError:
					print('Unable to open', filename)
					return
		
		# Send empty packet as sentinel
		self.send_packet(packet.make(), self.receiver_addr)
	
	def run_server(self, client_address=None):
		if client_address is None:
			client_address = RECEIVER_ADDR
		
		self.socket.bind(client_address)
		print('server running %s:%d' % (client_address[0], client_address[1]))
		self.receive_worker_server()	
		self.socket.close()

	


	
		
		
