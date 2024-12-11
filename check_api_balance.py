import requests
import json

# File containing API keys (one key per line)
API_KEYS_FILE = "api.txt"

# Output file for saving the results
OUTPUT_FILE = "api_credits.txt"

# WhoisXML API endpoint for account balance
API_URL = "https://user.whoisxmlapi.com/user-service/account-balance"

def check_api_credits(api_key):
    """
    Function to check credits for a given API key.
    """
    response = requests.get(API_URL, params={"apiKey": api_key})
    if response.status_code == 200:
        try:
            data = response.json()
            api_products = data.get("data", [])
            results = []
            for product in api_products:
                product_name = product["product"]["name"]
                credits = product["credits"]
                results.append(f"{product_name}: {credits} credits")
            return "\n".join(results)
        except json.JSONDecodeError:
            return f"Invalid JSON response for API key {api_key}. Raw Response: {response.text}"
    else:
        return f"Failed to retrieve data for API key {api_key}. HTTP Status Code: {response.status_code}"

def main():
    # Read API keys from file
    try:
        with open(API_KEYS_FILE, "r") as file:
            api_keys = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{API_KEYS_FILE}' not found.")
        return

    # Open output file for writing
    with open(OUTPUT_FILE, "w") as output_file:
        for api_key in api_keys:
            output_file.write(f"Results for API Key: {api_key}\n")
            print(f"Checking credits for API Key: {api_key}...")
            results = check_api_credits(api_key)
            output_file.write(results + "\n\n")
            print(results)
    
    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
