import logging
import datetime
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import webbrowser
from API import key  # Ensure your API key is stored securely in this module
from colorama import init, Fore, Style

# Initialize Colorama for colorful terminal output
init(autoreset=True)

# Set up logging to record errors and events
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def print_banner():
    """Print a colorful ASCII art banner."""
    banner = f"""{Fore.GREEN}
██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
   ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        Version: 1.5 by @jaikanthh                 
{Style.RESET_ALL}"""
    print(banner)


def get_phone_number():
    """Prompt the user for a phone number and parse it."""
    try:
        number = input(Fore.CYAN + "Enter phone number with country code: " + Style.RESET_ALL)
        parsed = phonenumbers.parse(number)
        return number, parsed
    except Exception as e:
        logging.error("Error parsing phone number", exc_info=True)
        print(Fore.RED + "Invalid phone number format. Please try again." + Style.RESET_ALL)
        return None, None


def lookup_number(parsed_number):
    """Lookup location and service provider information from the phone number."""
    try:
        number_location = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        return number_location, service_provider
    except Exception as e:
        logging.error("Error looking up phone number details", exc_info=True)
        print(Fore.RED + "Error during phone number lookup." + Style.RESET_ALL)
        return None, None


def get_location_details(query):
    """Retrieve detailed geographic information using OpenCageGeocode."""
    try:
        geocoder_obj = OpenCageGeocode(key)
        results = geocoder_obj.geocode(query)
        if results and len(results) > 0:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            timezone = results[0]['annotations']['timezone']['name']
            currency_name = results[0]['annotations']['currency']['name']
            currency_symbol = results[0]['annotations']['currency']['symbol']
            flag = results[0]['annotations']['flag']
            return lat, lng, timezone, currency_name, currency_symbol, flag
        else:
            logging.warning("No location details found for query: %s", query)
            print(Fore.RED + "No location details found." + Style.RESET_ALL)
            return None
    except Exception as e:
        logging.error("Error retrieving location details", exc_info=True)
        print(Fore.RED + "Error retrieving location details." + Style.RESET_ALL)
        return None


def save_lookup_history(phone_number, location, lat, lng):
    """Save the lookup details with a timestamp to a local file."""
    try:
        now = datetime.datetime.now()
        history_line = f"{now} - Phone: {phone_number}, Location: {location}, Lat: {lat}, Lng: {lng}\n"
        with open("lookup_history.txt", "a") as f:
            f.write(history_line)
    except Exception as e:
        logging.error("Error saving lookup history", exc_info=True)


def choose_map_service():
    """Allow the user to choose a mapping service."""
    try:
        print("\n" + Fore.YELLOW + "Choose map service to view location:" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Google Maps")
        print(Fore.YELLOW + "2. Apple Maps" + Style.RESET_ALL)
        choice = input(Fore.CYAN + "Enter 1 or 2: " + Style.RESET_ALL).strip()
        if choice == "2":
            return "apple"
        else:
            return "google"
    except Exception as e:
        logging.error("Error choosing mapping service", exc_info=True)
        return "google"


def open_map(lat, lng, service):
    """Open the map in the default browser using the chosen service."""
    try:
        if service == "apple":
            map_url = f"http://maps.apple.com/?ll={lat},{lng}"
        else:
            map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
        print(Fore.GREEN + "Opening map in your web browser..." + Style.RESET_ALL)
        webbrowser.open_new(map_url)
    except Exception as e:
        logging.error("Error opening map", exc_info=True)
        print(Fore.RED + "Error opening map." + Style.RESET_ALL)


def main():
    print_banner()

    # Get and validate phone number input
    phone_number, parsed_number = get_phone_number()
    if not parsed_number:
        return

    # Lookup basic phone number details
    number_location, service_provider = lookup_number(parsed_number)
    if not number_location:
        return

    # Display the phone number lookup details
    print(Fore.YELLOW + f"{phone_number} : {number_location}" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Service provider :" + Fore.GREEN, service_provider, Style.RESET_ALL)

    # Retrieve geographic location details
    details = get_location_details(number_location)
    if not details:
        return
    lat, lng, timezone, currency_name, currency_symbol, flag = details

    # Print additional location details
    print(Fore.CYAN + "Time-Zone :" + Fore.GREEN, timezone)
    print(Fore.CYAN + "Currency :" + Fore.GREEN, currency_name)
    print(Fore.CYAN + "Symbol   :" + Fore.GREEN, currency_symbol)
    print(Fore.CYAN + "Latitude :" + Fore.GREEN, lat)
    print(Fore.CYAN + "Longitude:" + Fore.GREEN, lng, Style.RESET_ALL)

    # Save lookup history to file
    save_lookup_history(phone_number, number_location, lat, lng)

    # Let user choose mapping service and open the map
    mapping_service = choose_map_service()
    open_map(lat, lng, mapping_service)


if __name__ == '__main__':
    main()
