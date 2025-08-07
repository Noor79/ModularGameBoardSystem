import serial
import threading
import time
from typing import Optional

class SerialCommunication:
    """Handles communication with Arduino board"""
    
    def __init__(self, port: str, baud_rate: int = 115200):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_conn: Optional[serial.Serial] = None
        self.running = False
        self.message_callback = None
    
    def set_message_callback(self, callback):
        """Set callback function for received messages"""
        self.message_callback = callback
    
    def start(self) -> bool:
        """Start serial connection"""
        try:
            self.serial_conn = serial.Serial(self.port, self.baud_rate, timeout=1)
            self.running = True
            threading.Thread(target=self._read_loop, daemon=True).start()
            print(f"Serial connected on {self.port}")
            return True
        except Exception as e:
            print(f"Serial connection failed: {e}")
            return False
    
    def stop(self):
        """Stop serial connection"""
        self.running = False
        if self.serial_conn:
            self.serial_conn.close()
    
    def send_command(self, command: str):
        """Send command to Arduino"""
        if self.serial_conn and self.serial_conn.writable():
            try:
                self.serial_conn.write((command + "\n").encode())
            except Exception as e:
                print(f"Serial send error: {e}")
    
    def _read_loop(self):
        """Read loop for incoming serial data"""
        while self.running:
            try:
                if self.serial_conn and self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode("utf-8").strip()
                    if line and self.message_callback:
                        self.message_callback(line)
            except Exception as e:
                print(f"Serial read error: {e}")
                self.running = False
            time.sleep(0.01) # Small delay to prevent busy-waiting


