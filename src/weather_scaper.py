import requests
import re
from datetime import datetime

MAX_NWS_VERSION = 50

def scrape_nws_climate(version=1):
    url = f"https://forecast.weather.gov/product.php?site=OKX&issuedby=NYC&product=CLI&format=TXT&version={version}&glossary=0"
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text

        data = {
            "STATION": "CLINYC",         # Station identifier (e.g., CLINYC for Central Park, NY)
            "NAME": "Central Park NY",   # Name of the weather station location
            "DATE": None,                # Observation date (YYYY-MM-DD, typically the day before the release date)
            "RELEASE_DATE": None,        # Issuance date of the report (YYYY-MM-DD, e.g., date the report was published)
            "TIME": None,                # Issuance time of the report (HH:MM in 24-hour format, e.g., 02:17)
            "AWND": None,                # Average daily wind speed (mph, two-minute sustained wind)
            "PGTM": None,                # Time of peak wind gust (HHMM in 24-hour format, e.g., 1500 for 3:00 PM)
            "PRCP": None,                # Daily precipitation (inches, total for the day; T for trace amounts)
            "SNOW": None,                # Daily snowfall (inches; T for trace amounts)
            "SNWD": None,                # Snow depth at observation time (inches; T for trace amounts)
            "TAVG": None,                # Average daily temperature (degrees Fahrenheit, mean of TMAX and TMIN)
            "TMAX": None,                # Maximum daily temperature (degrees Fahrenheit)
            "TMIN": None,                # Minimum daily temperature (degrees Fahrenheit)
            "WDF2": None,                # Direction of highest wind speed (degrees, e.g., 220 for SW)
            "WDF5": None,                # Direction of highest wind gust (degrees, e.g., 240 for SW)
            "WSF2": None,                # Highest wind speed (mph, two-minute sustained wind)
            "WSF5": None,                # Highest wind gust speed (mph)
            "WT01": 0,                   # Fog indicator (1 if fog observed, 0 otherwise)
            "WT02": 0,                   # Heavy fog indicator (1 if heavy fog observed, 0 otherwise)
            "WT03": 0,                   # Thunder indicator (1 if thunder observed, 0 otherwise)
            "WT06": 0,                   # Rain or shower indicator (1 if rain or showers observed, 0 otherwise)
            "WT08": 0                    # Haze indicator (1 if haze observed, 0 otherwise)
        }

        issuance_match = re.search(r"(\d{1,2}:?\d{0,2}\s+(?:AM|PM))\s+EDT\s+\w+\s+(\w+\s+\d{1,2}\s+\d{4})", text)
        if issuance_match:
            time_str = issuance_match.group(1)
            release_date_str = issuance_match.group(2)
            # Handle both "2:17 AM" and "217 AM" formats for time
            time_str = re.sub(r"(\d{1,2})(\d{2})\s+(AM|PM)", r"\1:\2 \3", time_str) if ":" not in time_str else time_str
            time_dt = datetime.strptime(time_str, "%I:%M %p")
            data["TIME"] = time_dt.strftime("%H:%M")
            # Parse and format release date
            release_date_dt = datetime.strptime(release_date_str, "%b %d %Y")
            data["RELEASE_DATE"] = release_date_dt.strftime("%Y-%m-%d")

        # observation date (e.g., "JULY 18 2025")
        date_match = re.search(r"CLIMATE SUMMARY FOR (\w+ \d{1,2} \d{4})", text)
        if date_match:
            date_str = date_match.group(1)
            data["DATE"] = datetime.strptime(date_str, "%B %d %Y").strftime("%Y-%m-%d")

        # temperature data
        tmax_match = re.search(r"MAXIMUM\s+(\d+)\s+\d{1,2}:?\d*\s+(?:AM|PM)", text)
        tmin_match = re.search(r"MINIMUM\s+(\d+)\s+\d{1,2}:?\d*\s+(?:AM|PM)", text)
        tavg_match = re.search(r"AVERAGE\s+(\d+)", text)
        if tmax_match:
            data["TMAX"] = int(tmax_match.group(1))
        if tmin_match:
            data["TMIN"] = int(tmin_match.group(1))
        if tavg_match:
            data["TAVG"] = int(tavg_match.group(1))

        # precipitation
        prcp_match = re.search(r"PRECIPITATION \(IN\)\s+YESTERDAY\s+(\d+\.\d+|T)", text)
        if prcp_match:
            data["PRCP"] = 0.0 if prcp_match.group(1) == "T" else float(prcp_match.group(1))

        # snowfall and snow depth
        snow_match = re.search(r"SNOWFALL \(IN\)\s+YESTERDAY\s+(\d+\.\d+|T)", text)
        snwd_match = re.search(r"SNOW DEPTH\s+(\d+|T)", text)
        if snow_match:
            data["SNOW"] = 0.0 if snow_match.group(1) == "T" else float(snow_match.group(1))
        if snwd_match:
            data["SNWD"] = 0.0 if snwd_match.group(1) == "T" else float(snwd_match.group(1))

        # wind data
        awnd_match = re.search(r"AVERAGE WIND SPEED\s+(\d+\.\d+)", text)
        wsf2_match = re.search(r"HIGHEST WIND SPEED\s+(\d+)", text)
        wdf2_match = re.search(r"HIGHEST WIND DIRECTION\s+\w+\s+\((\d+)\)", text)
        wsf5_match = re.search(r"HIGHEST GUST SPEED\s+(\d+)", text)
        wdf5_match = re.search(r"HIGHEST GUST DIRECTION\s+\w+\s+\((\d+)\)", text)
        if awnd_match:
            data["AWND"] = float(awnd_match.group(1))
        if wsf2_match:
            data["WSF2"] = int(wsf2_match.group(1))
        if wdf2_match:
            data["WDF2"] = int(wdf2_match.group(1))
        if wsf5_match:
            data["WSF5"] = int(wsf5_match.group(1))
        if wdf5_match:
            data["WDF5"] = int(wdf5_match.group(1))

        # peak gust time (PGTM)
        pgtm_match = re.search(r"HIGHEST GUST SPEED\s+\d+\s+HIGHEST GUST DIRECTION\s+\w+\s+\(\d+\)\s+(\d{1,2}:?\d*\s+(?:AM|PM))", text)
        if pgtm_match:
            time_str = pgtm_match.group(1)
            # Handle both "5:34 PM" and "534 PM" formats
            time_str = re.sub(r"(\d{1,2})(\d{2})\s+(AM|PM)", r"\1:\2 \3", time_str)  # Add colon if missing
            pgtm_dt = datetime.strptime(time_str, "%I:%M %p")
            data["PGTM"] = pgtm_dt.strftime("%H%M")

        # weather conditions
        weather_conditions = re.search(r"WEATHER CONDITIONS\s+THE FOLLOWING WEATHER WAS RECORDED YESTERDAY\.\s+(.+?)\s+\.", text, re.DOTALL)
        if weather_conditions:
            conditions = weather_conditions.group(1).lower()
            if "fog" in conditions:
                data["WT01"] = 1
            if "heavy fog" in conditions:
                data["WT02"] = 1
            if "thunder" in conditions:
                data["WT03"] = 1
            if "rain" in conditions or "shower" in conditions:
                data["WT06"] = 1
            if "haze" in conditions:
                data["WT08"] = 1
        else:
            # If "NO SIGNIFICANT WEATHER" is present, keep weather types as 0
            if "NO SIGNIFICANT WEATHER" in text:
                pass

        return data

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None


