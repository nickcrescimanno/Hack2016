import socket, traceback


class ControllerInput:
    s = 1

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(('', 4444))
        self.s.listen(1)
        print 'Listening'

        connection, address = self.s.accept()

    def close(self):
        connection.close()
        self.s.close()

    def poll(self):
        try:
            message = connection.recv(16)
            print "Got Mesage from %s: %s:" % (address, message)
        except(KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()

        normalized1 = (ord(message[0]) - 128) / 128.0
        normalized2 = (ord(message[1]) - 128) / 128.0
        normalized3 = (ord(message[2])) / 256.0
        return normalized1, normalized2, normalized3, ord(message[3])

