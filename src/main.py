from weather_scaper import MAX_NWS_VERSION, scrape_nws_climate
from datetime import datetime
import pandas as pd
from pathlib import Path

DEFAULT_OUTPUT_PATH = Path('data/')

class WeatherScaper:
    _data: pd.DataFrame 
    def __init__(self, output_path=DEFAULT_OUTPUT_PATH):
        self._output_path = output_path
        self._date = datetime.today().date()
        self._output_filename = f"NWS_SCRAPE_{self._date.isoformat()}.csv"
        
        
    def get_data(self):
        list_of_data_scaped = []
        for version in range(1,2+1):
            list_of_data_scaped.append(pd.DataFrame(scrape_nws_climate(version=version), index=[version]))
        return pd.concat(list_of_data_scaped)
                
    def save_data(self, data: pd.DataFrame):
        data.to_csv(self._output_path / self._output_filename)
        
    def run(self):
        self._data = self.get_data()
        self.save_data(self._data)    
                
def main():
    weather_scaper = WeatherScaper()
    weather_scaper.run()
    print(f"Last Data: TMAX: {weather_scaper._data['TMAX'][1]} TMIN: {weather_scaper._data['TMIN'][1]}")
    
if __name__ == "__main__":
    main()