from protocol import Protocol as MiniTcp
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    mini_tcp = MiniTcp()
    mini_tcp.send_file(filename)
    exit()