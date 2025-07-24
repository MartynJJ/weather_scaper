from weather_scaper import MAX_NWS_VERSION, scrape_nws_climate

from datetime import datetime, date
import pandas as pd
from pathlib import Path
from typing import Optional

DEFAULT_OUTPUT_PATH = Path('data/')

class WeatherScaper:
    def __init__(self, output_path: Path = DEFAULT_OUTPUT_PATH, scrape_date: Optional[date] = None) -> None:
        self._output_path = output_path
        self._date = scrape_date or datetime.today().date()
        self._output_filename = f"NWS_SCRAPE_{self._date.isoformat()}.csv"
        self._data: Optional[pd.DataFrame] = None

    def get_data(self) -> pd.DataFrame:
        data_frames = []
        for version in range(1, MAX_NWS_VERSION + 1):
            try:
                data = scrape_nws_climate(version=version)
                df = pd.DataFrame(data, index=[version])
                data_frames.append(df)
            except Exception as e:
                print(f"Warning: Failed to scrape version {version}: {e}")
        if data_frames:
            return pd.concat(data_frames)
        else:
            raise RuntimeError("No data was scraped.")

    def save_data(self, data: pd.DataFrame) -> None:
        self._output_path.mkdir(parents=True, exist_ok=True)
        file_path = self._output_path / self._output_filename
        try:
            data.to_csv(file_path)
            print(f"Data saved to {file_path}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def run(self) -> None:
        self._data = self.get_data()
        self.save_data(self._data)

def main() -> None:
    weather_scaper = WeatherScaper()
    weather_scaper.run()
    if weather_scaper._data is not None and not weather_scaper._data.empty:
        first_row = weather_scaper._data.iloc[0]
        print(f"Last Data: TMAX: {first_row.get('TMAX', 'N/A')} TMIN: {first_row.get('TMIN', 'N/A')}")
    else:
        print("Last Data: No data to display.")

if __name__ == "__main__":
    main()
