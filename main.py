import argparse
import sys

import requests

API_URL = "https://www.vehicleservices.gov.ie/api/v1/public-cmv/cmv/vehicles/lookup"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.vehicleservices.gov.ie",
    "Referer": "https://www.vehicleservices.gov.ie/cmv",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
}


def lookup_reg(reg: str) -> dict:
    resp = requests.post(
        API_URL, json={"registrationNumber": reg}, headers=HEADERS, timeout=10
    )
    resp.raise_for_status()
    return resp.json()


def print_result(reg: str, data: dict) -> None:
    vehicle = data.get("vehicleDetails", {})
    tax = data.get("motorTaxDetails", {})

    print(f"Registration: {reg}")
    print(f"Make/Model:   {vehicle.get('vehicleMake', '?')} {vehicle.get('vehicleModel', '?')}")
    print(f"Colour:       {vehicle.get('vehicleColourEn', '?')}")
    print(f"Tax status:   {tax.get('statusEn', '?')}")
    print(f"Tax expiry:   {tax.get('motorTaxExpiryDate', '?')}")
    print(f"Tax class:    {tax.get('taxClassEn', '?')}")
    print(f"Annual rate:  €{tax.get('annualMotorRate', '?')}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Look up Irish vehicle registration and motor tax details."
    )
    parser.add_argument(
        "registration", nargs="?", help="Vehicle registration number, e.g. 241D38103"
    )
    args = parser.parse_args()

    registration = args.registration or input("Enter vehicle registration: ")
    reg = registration.strip().upper()

    if not reg:
        print("No registration provided.", file=sys.stderr)
        return 1

    try:
        data = lookup_reg(reg)
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            print(f"No vehicle found for registration '{reg}'.", file=sys.stderr)
        else:
            print(f"Request failed: {e}", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return 1

    print_result(reg, data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
