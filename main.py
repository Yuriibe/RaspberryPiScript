import socket
import pickle  # Import the pickle module for deserializing data
import time

NULL_CHAR = chr(0)
KEY_W = chr(26)
KEY_A = chr(4)
KEY_S = chr(22)
KEY_D = chr(7)
KEY_Space = chr(44)
def get_key_value(key):
    if key == "W":
        return KEY_W
    elif key == "A":
        return KEY_A
    elif key == "S":
        return KEY_S
    elif key == "D":
        return KEY_D
    elif key == "space":
        return KEY_Space
    else:
        return None
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def press_key_hid(key_value):
    report = NULL_CHAR * 2 + key_value + NULL_CHAR * 5
    print("Sending report:", ':'.join("{:02x}".format(ord(c)) for c in report))  # This will print the report in hex
    write_report(report)
    # Release keys
    time.sleep(0.1)  # Short delay to simulate key press
    write_report(NULL_CHAR * 8)

# Your HID emulation code here

if __name__ == "__main__":
    pi_port = 12345  # Choose the same port number as in the PC script

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("0.0.0.0", pi_port))
            server_socket.listen()

            print("Waiting for key sequence from PC...")


            while True:
                client_socket, client_address = server_socket.accept()
                print("Connected to PC:", client_address)

                # Receive and deserialize the key sequence
                key_sequence_bytes = client_socket.recv(4096)
                key_sequence = pickle.loads(key_sequence_bytes)

                print("Received key sequence:", key_sequence)

                # Process and simulate the key presses
                print("key_sequence" + key_sequence)
                for key in key_sequence:
                    key_value = key
                    print("key: " + key)
                    if key_value:
                        press_key_hid(key_value)

                print("Key sequence processed")


    except Exception as e:
        print(f"Error: {str(e)}")
