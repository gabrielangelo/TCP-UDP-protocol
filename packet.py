# packet.py - Packet-related functions

# Creates a packet from a sequence number and byte data

class Packet:
    
    def __init__(self, data= b'', seq_num=0, ack=0, is_empty=False, end=False, checksum=None):
        self.ack = ack # add validation routine
        self.data = data if type(data) == bytes else data.encode('utf-8')
        self.seq_num = seq_num#(seq_num).to_bytes(4, byteorder = 'little', signed = True) if (seq_num is not None) else None
        self.checksum = checksum#self.checksum(self.data.decode('utf-8')) if data else 0
        self.is_empty = is_empty
        self.end = end
    
    @classmethod
    def make(cls, seq_num=None, data=b'', checksum=None, ack=None):
        if ((seq_num is None) and (data is None) and (ack is None)):
            return cls(is_empty=True)
        if data:
            checksum = checksum(data)
        return cls(data=data, seq_num=seq_num, ack=ack, checksum=checksum)
