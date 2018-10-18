from protocol import Protocol as MiniTcp

if __name__ == '__main__':
    mini_tcp = MiniTcp()
    mini_tcp.run_server()