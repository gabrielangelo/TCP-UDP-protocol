# packet.py - Packet-related functions

# Creates a packet from a sequence number and byte data

class Packet:
    
    def __init__(self, data='', seq_num=None, ack=None, is_empty=False, end=final):
        self.ack = ack # add validation routine
        self.data = data
        self.seq_num = (seq_num).to_bytes(4, byteorder = 'little', signed = True) if (seq_num is not None) else None
        self.checksum = self.checksum(data)
        self.is_empty = False
        self.end = end

    def checksum(self, strData):
        chksum = 0
        chksum = chksum	^ (int(str(int("20", 16)), 10))
        chksum = chksum	^ (int(str(int("03", 16)), 10))
        for char in strData:
            chksum = chksum ^ ord(char)
        chksum = chksum	^ (int(str(int("04", 16)), 10))
        return chksum
    
    @classmethod
    def make(cls, seq_num=None, data=None, ack=None):
        print(seq_num, data, ack)
        if not (seq_num and data and ack):
            return cls(is_empty=True)
        return cls(data=data, seq_num=seq_num, ack=ack)

def make(seq_num, data = b''):
    seq_bytes = (seq_num).to_bytes(4, byteorder = 'little', signed = True)
    checksum = checksum(data)
    return seq_bytes + data

# Creates an empty packet
def make_empty():
    return b''

# Extracts sequence number and data from a non-empty packet
def extract(packet):
    seq_num = int.from_bytes(packet[0:4], byteorder = 'little', signed = True)
    return seq_num, packet[4:]
