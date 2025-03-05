import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import webbrowser
from API import key  # Ensure your API key is correctly imported
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

# Print the banner
banner = f"""{Fore.GREEN}
██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
   ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        Version: 1.0 by @jaikanthh                 
{Style.RESET_ALL}"""
print(banner)

# Get the phone number input with a colored prompt
number = input(Fore.CYAN + "Enter phone number with country code: " + Style.RESET_ALL)
parsed_number = phonenumbers.parse(number)

# Get and display phone number location in yellow
number_location = geocoder.description_for_number(parsed_number, "en")
print(Fore.YELLOW + f"{number} : {number_location}" + Style.RESET_ALL)

# Display service provider details in magenta and green
service_provider = carrier.name_for_number(parsed_number, "en")
print(Fore.MAGENTA + "Service provider :" + Fore.GREEN, service_provider, Style.RESET_ALL)

# Use OpenCageGeocode API to get location details
geocoder_obj = OpenCageGeocode(key)
results = geocoder_obj.geocode(number_location)

lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
timezone = results[0]['annotations']['timezone']['name']
currency_name = results[0]['annotations']['currency']['name']
currency_symbol = results[0]['annotations']['currency']['symbol']
flag = results[0]['annotations']['flag']

# Print additional location details in color
print(Fore.CYAN + "Time-Zone :" + Fore.GREEN, timezone)
print(Fore.CYAN + "Currency :" + Fore.GREEN, currency_name)
print(Fore.CYAN + "Symbol   :" + Fore.GREEN, currency_symbol)
print(Fore.CYAN + "Latitude :" + Fore.GREEN, lat)
print(Fore.CYAN + "Longitude:" + Fore.GREEN, lng, Style.RESET_ALL)

# Directly open Google Maps with the coordinates (without any additional menu)
map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
print(Fore.GREEN + "Opening map in your web browser..." + Style.RESET_ALL)
webbrowser.open_new(map_url)
