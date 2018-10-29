from protocol import Protocol as MiniTcp
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    address = (str(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) == 4 else None 
    print(address)
    mini_tcp = MiniTcp(receiver_addr=address)
    mini_tcp.send_file(filename)
    print("\033[92m {}\033[00m".format('OK'))
    exit()