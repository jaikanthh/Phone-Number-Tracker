# Phone Tracker Project

A Python-based tool to track phone number details and geolocation information. This project uses the **phonenumbers** library to parse phone numbers and extract location and carrier details, and **OpenCageGeocode** to retrieve geographic information.

## Features

- **Phone Number Parsing:**  
  Extracts location and carrier information from phone numbers.
  
- **Geocoding:**  
  Retrieves latitude, longitude, timezone, currency, and flag data using the OpenCageGeocode API.
  
- **Mapping Integration:**  
  Opens the location in Google Maps (or Apple Maps, if desired) directly from your terminal.
  
- **Robust Error Handling & Logging:**  
  Captures errors and logs important events in `app.log` for easier debugging.
  
- **Data Persistence:**  
  Saves lookup history with timestamps in `lookup_history.txt`.

## Prerequisites

- Python 3.6 or higher

## Installation

1. **Clone the Repository**  
   Clone the repository and install the dependencies using the provided `requirements.txt`:

   ```bash
   git clone https://github.com/jaikanthh/phone-tracker.git
   cd phone-tracker
   ```

2. **Create a Virtual Environment** (Optional but recommended)  
   Set up a virtual environment to manage dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**  
   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
4. **Run The FIle**
   Run Tracker.py file

## Setup

### Configure Your API Key

Obtain an API key from [OpenCage Geocoder](https://opencagedata.com/api) and create a file named `API.py` in the project directory with the following content:

```python
# API.py
key = "YOUR_OPENCAGE_API_KEY"
```

## Usage

Run the main script:

```bash
python main.py
```

**When prompted, enter the phone number (with country code). The tool will then:**
- Display the phone number's location and carrier information.
- Retrieve and display detailed geographic information.
- Open the corresponding location in your default web browser via Google Maps (or Apple Maps).
