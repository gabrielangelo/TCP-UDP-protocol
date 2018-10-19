# packet.py - Packet-related functions

# Creates a packet from a sequence number and byte data

class Packet:
    
    def __init__(self, data='', seq_num=0, ack=0, is_empty=False, end=False):
        self.ack = ack # add validation routine
        self.data = data
        self.seq_num = seq_num#(seq_num).to_bytes(4, byteorder = 'little', signed = True) if (seq_num is not None) else None
        # self.checksum = self.checksum(data)
        self.is_empty = is_empty
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
        if ((seq_num is None) and (data is None) and (ack is None)):
            return cls(is_empty=True)
        return cls(data=data, seq_num=seq_num, ack=ack)
