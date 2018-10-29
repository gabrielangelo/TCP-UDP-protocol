# packet.py - Packet-related functions

# Creates a packet from a sequence number and byte data

class Packet:
    
    def __init__(self, data= b'', seq_num=0, ack=0, is_empty=False, end=False):
        self.ack = ack # add validation routine
        self.data = data if type(data) == bytes else data.encode('utf-8')
        self.seq_num = seq_num#(seq_num).to_bytes(4, byteorder = 'little', signed = True) if (seq_num is not None) else None
        self.checksum_data = self.checksum(self.data.decode('utf-8')) if data else 0
        self.is_empty = is_empty
        self.end = end

    def checksum(self, strData):
        strData = strData.decode('utf-8') if type(strData) == bytes else strData
        chksum = 0
        chksum = chksum	^ (int(str(int("20", 16)), 10))
        chksum = chksum	^ (int(str(int("03", 16)), 10))
        for char in strData:    
            chksum = chksum ^ ord(char)
        chksum = chksum	^ (int(str(int("04", 16)), 10))
        return chksum
    
    @classmethod
    def make(cls, seq_num=None, data=b'', ack=None):
        if ((seq_num is None) and (data is None) and (ack is None)):
            return cls(is_empty=True)
        return cls(data=data, seq_num=seq_num, ack=ack)
