from protocol import Protocol
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    mini_tcp = Protocol()
    mini_tcp.send_file(filename)