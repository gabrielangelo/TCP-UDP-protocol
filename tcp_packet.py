import random


class TCPPacket(object):
    """
    Add Documentation here
    """
    SMALLEST_STARTING_SEQ = 0
    HIGHEST_STARTING_SEQ = 4294967295

    def __init__(self):
        # self.src_port = src_port  # 16bit
        # self.dst_port = dst_port  # 16bit
        self.seq = TCPPacket.gen_starting_seq_num()  # 32bit
        self.ack = 0  # 32bit
        self.data_offset = 0  # 4 bits
        self.reserved_field = 0  # 3bits saved for future use must be zero assert self.reserved_field = 0
        #FLAGS
        self.flag_ns = 0  # 1bit
        self.flag_cwr = 0  # 1bit
        self.flag_ece = 0  # 1bit
        self.flag_urg = 0  # 1bit
        self.flag_ack = 0  # 1bit
        self.flag_psh = 0  # 1bit
        self.flag_rst = 0  # 1bit
        self.flag_syn = 0  # 1bit
        self.flag_fin = 0  # 1bit
        #window size
        self.window_size = 0  # 16bit
        #checksum
        self.checksum = 0  # 16bit
        #urgent pointer
        self.urgent_pointer = 0  # 16bit
        #options
        self.options = 0  # 0-320bits, divisible by 32
        #padding - TCP packet must be on a 32bit boundary this ensures that it is the padding is filled with 0's
        self.padding = 0  # as much as needed
        self.data = ""

    def __repr__(self):
        return "TCPPacket()"

    def __str__(self):
        return "SEQ Number: %d, ACK Number: %d, ACK:%d, SYN:%d, FIN:%d, TYPE:%s, DATA:%s" \
               % (self.seq, self.ack, self.flag_ack, self.flag_syn, self.flag_fin, self.packet_type(), self.data)

    def __cmp__(self, other):
        return cmp(self.seq, other.seq)

    def packet_type(self):
        packet_type = ""
        if self.flag_syn == 1 and self.flag_ack == 1:
            packet_type = "SYN-ACK"
        elif self.flag_ack == 1 and self.flag_fin == 1:
            packet_type = "FIN-ACK"
        elif self.flag_syn == 1:
            packet_type = "SYN"
        elif self.flag_ack == 1:
            packet_type = "ACK"
        elif self.flag_fin == 1:
            packet_type = "FIN"
        elif self.data != "":
            packet_type = "DATA"
        return packet_type

    def set_flags(self, ack=False, syn=False, fin=False):
        if ack:
            self.flag_ack = 1
        else:
            self.flag_ack = 0
        if syn:
            self.flag_syn = 1
        else:
            self.flag_syn = 0
        if fin:
            self.flag_fin = 1
        else:
            self.flag_fin = 0

    @staticmethod
    def gen_starting_seq_num():
        return random.randint(TCPPacket.SMALLEST_STARTING_SEQ, TCPPacket.HIGHEST_STARTING_SEQ)