import digitalio
import board
import busio
import adafruit_rfm9x
from adafruit_bmp280 import Adafruit_BMP280_I2C

# Initialize SPI for the RFM9x module
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP6)
reset = digitalio.DigitalInOut(board.GP7)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)
print("RFM9x radio ready")

# Initialize I2C for the BMP280 sensor at address 0x76
i2c = busio.I2C(scl=board.GP9, sda=board.GP8)
bmp280 = Adafruit_BMP280_I2C(i2c, address=0x76)

# Optional: Set sea level pressure in hPa for accurate altitude readings
bmp280.sea_level_pressure = 1013.25

def send(message):
    """Send a message using the LoRa module."""
    rfm9x.send(message)

while True:
    # Read temperature and pressure from the BMP280
    temperature = bmp280.temperature  # in degrees Celsius
    pressure = bmp280.pressure  # in hPa

    # Format the message
    message = f"Temp: {temperature:.2f} C, Pressure: {pressure:.2f} hPa"

    # Send the message over LoRa
    send(message)
    print(f"Sent: {message}")
