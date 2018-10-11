import threading

from TCP_over_UDP import TCP
cur_ip = ""
cur_port = ""
cur_sock = None

def connect():
    try:
        cur_sock = TCP()
        cur_sock.connect((cur_ip, cur_port))
        return cur_sock
    except Exception as error:
        print "An error has occured: error is:%s." % error

@staticmethod
def close_connection():
    cur_sock.close()

def receiving_msg1():
    if cur_sock is not None:
        try:
            while True:
                data = cur_sock.recv()
                if data == "Disconnected":
                    print data
                    return
                else:
                    print(data)
                    # self.ids.chat_scroll_text.text += data + "\n"
        except Exception as error:
            print "an error " + str(error)
    pass

def receiving_msg_handle1():
    try:
        t = threading.Thread(target=receiving_msg1)
        t.start()
    except Exception as error:
        print "an error" + str(error)

def send_message(msg):
    cur_sock.send(msg)

def run():
    receiving_msg_handle1()
    while True:
        msg = input('send a message')
        connect()
        send_message(msg)
        close_connection()


        





