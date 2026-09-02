# GOV-REG-API

A small CLI tool to look up Irish vehicle registration and motor tax details using the public [vehicleservices.gov.ie](https://www.vehicleservices.gov.ie/cmv) lookup API.

## Requirements

- Python 3
- `requests` (`pip install requests`)

## Usage

Pass the registration number as an argument:

```
python3 main.py 241D38103
```

Or run with no argument and you'll be prompted for it:

```
python3 main.py
Enter vehicle registration: 241D38103
```

## Example output

```
Registration: 241D38103
Make/Model:   BMW X1
Colour:       GREEN
Tax status:   Motor Tax up to date
Tax expiry:   2027-03-31
Tax class:    PRIVATE CO2
Annual rate:  €140.0
```

If the registration isn't found, an error is printed and the tool exits with a non-zero status code.
