# 📡 Meraki MT10 IoT Monitoring Dashboard (Azure + Streamlit)

## 📘 Overview
This project creates a full-stack monitoring solution for the Meraki MT10 sensor. It collects temperature and humidity readings via the Meraki API, stores them in Azure Table Storage, and displays them in a live dashboard built with Streamlit.

This lab demonstrates how to create a hybrid observability pipeline using cloud-native services and real-time data from on-prem IoT sensors.

---

## 🧱 Architecture

```plaintext
+-------------------+       Meraki API        +-----------------------------+
| Meraki MT10       | ---------------------> | Python Poller (Azure client)|
| IoT Sensor        |                        | - poll_mt10_updated.py       |
+-------------------+                        | - Scheduled via schedule     |
                                             +-------------+---------------+
                                                           |
                                                           v
                                       +-------------------------------+
                                       | Azure Table Storage           |
                                       +-------------------------------+
                                                           |
                                                           v
                                      +-------------------------------+
                                      | Streamlit Dashboard           |
                                      | - dashboard_final.py          |
                                      +-------------------------------+
```

---

## ⚙️ Prerequisites

- Meraki MT10 sensor (online in Dashboard)
- Meraki API key with read permissions
- Azure Storage Account (with Table support)
- Python 3.8+
- A working site-to-site VPN if accessing Azure privately (optional)

---

## 🧑‍💻 Setup Steps (Simplified)

### 1. Clone the repo
```bash
git clone https://github.com/your-repo/mt10-iot-dashboard.git
cd mt10-iot-dashboard
```

### 2. Configure your `.env` file
Copy the example:
```bash
cp .env.example .env
```
Edit it to include:
```env
MERAKI_API_KEY=your_meraki_api_key
MERAKI_ORG_ID=your_org_id
MT10_SERIAL=your_mt10_serial
AZURE_STORAGE_CONN=your_azure_storage_connection_string
```

---

### 3. Install dependencies
```bash
pip install meraki azure-data-tables schedule python-dotenv streamlit pandas
```

---

### 4. Run the poller (sensor fetcher)
```bash
python poll_mt10_updated.py
```
✅ This collects and logs MT10 data to Azure Table Storage.

---

### 5. Launch the dashboard
```bash
streamlit run dashboard_final.py
```
✅ This opens a local web dashboard to visualize temperature and humidity with time filtering and live metrics.

---

## ✅ Validation Checklist

- Azure Table Storage receives new sensor entries
- Temperature and humidity charts update with new data
- `.env` variables are correctly loaded
- Time filtering and UTC timestamps work correctly in the dashboard

---

## 🧠 Skills Demonstrated

- IoT API data polling and transformation
- Azure cloud storage integration (NoSQL Table)
- Real-time dashboarding with Streamlit
- Secure .env-based configuration
- Time-series filtering and visualization