import asyncio
import json
import logging
from azure.iot.device.aio import IoTHubModuleClient

# Logger'ı yapılandırın
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# IoT Hub bağlantısı için ModuleClient oluşturun
client = IoTHubModuleClient.create_from_edge_environment()

def save_data_to_file(data):
    try:
        # Open the file in append mode and write the data
        with open("modbus_data.json", "a") as file:
            file.write(data + "\n")
        logger.info("Data saved to file.")
    except Exception as ex:
        logger.error("Error saving data to file: %s", ex)

# Set the message handler
async def message_handler(message):
    if message.input_name == "Input1":
        data = message.data.decode("utf-8")
        logger.info("Received data from ModbusClientModule: %s", data)

        # Save data to file
        save_data_to_file(data)

async def main():
    try:
        # Connect to IoT Edge
        await client.connect()

        logger.info("Analytic module connected to IoT Edge.")

        # Set the message handler
        client.on_message_received = message_handler

        # Keep the module alive
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Analytic module stopped by the user.")
    except Exception as ex:
        logger.error("Error: %s", ex)

if __name__ == "__main__":
    asyncio.run(main())
