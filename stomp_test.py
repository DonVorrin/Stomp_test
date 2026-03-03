import time
import sys
import stomp

class MsgListener(stomp.ConnectionListener):
    def on_error(self, message):
        print('received an error "%s"' % message.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)

AMQHOST = "" 
AMQPORT = "" 
AMQUSER = "" 
AMQPASS = ""  
TOPICNAME = ""
hosts = [(AMQHOST, AMQPORT)]


conn = stomp.Connection(host_and_ports=hosts)
conn.set_listener('stomp_listener', MsgListener())


conn.connect(AMQUSER, AMQPASS, wait=True, headers={'client-id': 'testClient'})


message = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else "testStomp"
conn.send(body=message, destination=TOPICNAME)
print(f"Messages Send - {TOPICNAME}: {message}")


time.sleep(3)


conn.subscribe(destination=TOPICNAME, id=1, ack='auto')
print(f"subscribe - {TOPICNAME}")


print("Wait messages...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDisconnect")
    conn.disconnect()
