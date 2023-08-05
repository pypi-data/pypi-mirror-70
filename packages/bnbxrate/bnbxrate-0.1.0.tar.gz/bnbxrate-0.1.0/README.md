# bnbxrate

Provides historical exchange rates USD/BGN for a given date. The main source of the data is Bulgarian National Bank - ![bnb.bg](http://bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm?toLang=_EN).

## Usage
``` bash
bnbxrate '01.01.2020'
```
In this case the provided date was a national holiday, so the result is for the last working day:

```
{'31.12.2019': '1.74099'}
```
The date format should be in '%d.%m.%Y'.

## Installation
Create a virtual environment with python3.6+, before running the code.
```bash
git clone https://github.com/hristo-mavrodiev/bnbxrate.git
cd bnbxrate
pip install -r requirements.txt
python setup.py install
```

## License
MIT
