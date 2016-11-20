import socket, traceback

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', 4444))

s.listen(1)

print "Listening for broadcasts..."

while 1:

    connection, address = s.accept()

    try:
        message = connection.recv(16)
        print "Got message from %s: %s" % (address, message)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
    finally:
        connection.close()