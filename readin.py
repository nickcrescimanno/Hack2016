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

    def poll(self):
        # returns latest input from controller
        connection, address = s.accept()

        try:
            message = connection.recv(16)
            print "Got Mesage from %s: %s:" % (address, message)
        except(KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()
        finally:
            connection.close()
        # if len(message) == 4:
        #	print struct.unpack('bbbb', message)

        # print '1',message[0],'2',ord(message[1]),'3',ord(message[2]),'4',ord(message[3])
        # input=' '.join(format(ord(x), 'b') for x in message)
        # a=input.split(' ')
        # print '1',ord(message[0]),'2',ord(message[1]),'3',ord(message[2]),'4',ord(message[3])
        normalized1 = (ord(message[0]) - 128) / 128
        normalized2 = (ord(message[1]) - 128) / 128
        normalized3 = (ord(message[1]) - 256) / 256
        return normalized1, normalized2, normalized3, ord(message[3])
