import threading
from time import sleep 
import socket

from packet import TCPPacket


class Protocol:
	def __init__(self, timeout=5, window_size=5):
		self.timeout=timeout
		self.packets_buffer = {}
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.window_size = window_size

	def check_received_packet(address, condition):
		sleep(self.timeout)
		try:
			return self.packets_received[condition][address]
		except KeyError
			return None
	 
	 def _checksum(self, source_string):
        	my_sum = 0
        	count_to = (len(source_string) / 2) * 2
        	count = 0
        	while count < count_to:
            		this_val = ord(source_string[count + 1])*256+ord(source_string[count])
            		my_sum += this_val
            		count += 2
        	if count_to < len(source_string):
            		my_sum += ord(source_string[len(source_string) - 1])
        	my_sum = (my_sum >> 16) + (my_sum & 0xffff)
        	my_sum += (my_sum >> 16)
        	answer = ~my_sum
        	answer = answer & 0xffff
        	answer = answer >> 8 | (answer << 8 & 0xff00)
        	return answer
	
	@classmethod
	def divide_data(self, data):
		pass
	
    def _gen_starting_seq_num(self):
        return random.randint(TCPPacket.SMALLEST_STARTING_SEQ, TCPPacket.HIGHEST_STARTING_SEQ)

	def check_arrived_packets(self, address):
		while True:
			pass
	
	def bulk_send_packets(self, data, address):
		data_parts = divide_data(data)
		seq = self._gen_starting_seq_num()
		global seq_base = seq	
		global seq_end = seq_base	
		aux_seq = seq
		first_packet_to_send = False
		for data in data_parts:
			packet = TCPPacket()
			aux_seq+=len(data)
			packet.seq = seq if first_packet_to_send else aux_seq 
			packet.data = data
			packet.checksum = self._checksum(data)
			try:
				self.socket.sendto(packet, address)
			except socket.error:
				print('socket error')
			
			if address in self.packets_list.keys:
				self.packets_buffer[adress].append(packet)
			else:
				self.packets_buffer[address] = [packet]
			
		
		
