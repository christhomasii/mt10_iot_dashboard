import os
import meraki
import schedule
import time
from azure.data.tables import TableServiceClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("MERAKI_API_KEY")
STORAGE_CONN = os.getenv("AZURE_STORAGE_CONN")
ORG_ID = os.getenv("MERAKI_ORG_ID")
MT10_SERIAL = os.getenv("MT10_SERIAL")

dashboard = meraki.DashboardAPI(API_KEY)
table_service = TableServiceClient.from_connection_string(STORAGE_CONN)
table_client = table_service.get_table_client("SensorData")

def fetch_and_log():
    try:
        result = dashboard.sensor.getOrganizationSensorReadingsLatest(
            organizationId=ORG_ID,
            serials=[MT10_SERIAL]
        )
        print("Collecting data")

        if result and "readings" in result[0]:
            readings = result[0]["readings"]

            temperature = None
            humidity = None
            timestamp = None

            for r in readings:
                if r["metric"] == "temperature":
                    temperature = r["temperature"]["fahrenheit"]
                    timestamp = r["ts"]
                elif r["metric"] == "humidity":
                    humidity = r["humidity"]["relativePercentage"]

            if temperature is None or humidity is None:
                print("Temperature or humidity reading not found.")
                return

            entity = {
                'PartitionKey': 'MT10',
                'RowKey': timestamp,
                'Temperature': temperature,
                'Humidity': humidity
            }
            table_client.create_entity(entity=entity)
            print(f"Logged reading at {timestamp}")
        else:
            print("No sensor readings found.")
    except Exception as e:
        print(f"Error fetching or logging data: {e}")

schedule.every(5).minutes.do(fetch_and_log)
fetch_and_log()

while True:
    schedule.run_pending()
    time.sleep(1)