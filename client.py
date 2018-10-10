import threading

from protocol import TCP

def send_message(msg):
    cur_sock.send('[b]' + ('[color=%s]' % cur_color) + cur_nick + msg + '[/color]' + '[/b]')
    print('[b]' + ('[color=%s]' % cur_color) + cur_nick + msg + '[/color]' + '[/b]')

def close_connection():
    cur_sock.close()

def receiving_msg(self):
    try:
        while True:
            data = cur_sock.recv()
            if data == "Disconnected":
                print(data) 
                return
            else:
                self.ids.chat_scroll_text.text += data + "\n"
    except Exception as error:
        print "an error " + str(error)

def receiving_msg_handle(self):
    try:
        t = threading.Thread(target=self.receiving_msg)
        t.start()
    except Exception as error:
        print("an error" + str(error))
