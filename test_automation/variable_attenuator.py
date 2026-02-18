import serial
import time
import logging

# Configure logging to track instrument communication
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class VariableAttenuator:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200, timeout=1):
        """
        Initialize the connection to the variable attenuator.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            logging.info(f"Connected to attenuator at {self.port}")
            # Clear any stale data in the buffer
            self.connection.reset_input_buffer()
        except serial.SerialException as e:
            logging.error(f"Failed to connect to {self.port}: {e}")
            raise

    def disconnect(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            logging.info("Disconnected from attenuator.")

    def _send_command(self, cmd):
        """Helper to send commands and return response."""
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Device not connected.")

        # Add termination characters (CR/LF is common for SCPI/Serial instruments)
        full_cmd = f"{cmd}\r\n"
        self.connection.write(full_cmd.encode('utf-8'))

        # Wait briefly for device processing
        time.sleep(0.1)

        response = self.connection.readline().decode('utf-8').strip()
        return response

    def set_attenuation(self, db_value):
        """
        Sets the attenuation level.
        Note: Verify the specific command syntax for your hardware vendor
        (e.g., Mini-Circuits often uses plain numbers or specific codes).
        """
        # Input validation (Example: 0 to 90dB range)
        if not (0 <= db_value <= 90):
            logging.error(f"Value {db_value} is out of valid range (0-90 dB).")
            return False

        try:
            # Command syntax varies by vendor (e.g. Vaunix, Mini-Circuits)
            # Scenario A: SCPI Style -> ":ATT:SET 20"
            # Scenario B: Mini-Circuits Style -> "20" or "SETATT=20"
            cmd = f"SETATT={db_value}"

            logging.info(f"Setting attenuation to {db_value} dB...")
            self._send_command(cmd)
            return True
        except Exception as e:
            logging.error(f"Error setting attenuation: {e}")
            return False

    def get_attenuation(self):
        """Reads back the current setting to verify."""
        try:
            response = self._send_command("GETATT?")
            logging.info(f"Device reports: {response} dB")
            return response
        except Exception as e:
            logging.error(f"Error reading attenuation: {e}")
            return None


# --- Usage Example ---
if __name__ == "__main__":
    # Context manager usage is safer for ensuring the port closes
    att = VariableAttenuator(port='/dev/ttyACM0')

    try:
        att.connect()
        att.set_attenuation(15.5)  # Set to 15.5 dB
        current_val = att.get_attenuation()  # Verify

    except Exception as e:
        print(f"Test aborted: {e}")
    finally:
        att.disconnect()