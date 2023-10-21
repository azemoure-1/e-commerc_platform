import requests
import json
import re
import csv

# Define your eBay API Sandbox keys
app_id = "amineaze-Amine-SBX-30d6926e7-d6b90072"
dev_id = "924404a8-b3f2-4b58-8265-d28a2717475c"

# The eBay Finding API Sandbox endpoint
api_endpoint = "https://svcs.sandbox.ebay.com/services/search/FindingService/v1"

# Define your query parameters
keywords = "laptop"  # Your search query

# Replace non-breaking spaces with regular spaces
keywords = re.sub(r'\xa0', ' ', keywords)

api_payload = {
    "OPERATION-NAME": "findItemsByKeywords",
    "SERVICE-VERSION": "1.0.0",
    "SECURITY-APPNAME": app_id,
    "RESPONSE-DATA-FORMAT": "JSON",
    "keywords": keywords,
}

# Make the API request
response = requests.get(api_endpoint, params=api_payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse and work with the response data (usually in JSON format)
    data = response.json()

    # Create a list to store the structured data
    structured_data = []

    # Extract more information from the response
    search_results = data.get("findItemsByKeywordsResponse", [])[0]
    if "ack" in search_results and search_results["ack"] == ["Success"]:
        # Iterate over the search results and extract additional information
        for item in search_results.get("searchResult", [])[0].get("item", []):
            structured_data_item = {
                "item_id": item.get("itemId", ["N/A"])[0],
                "title": item.get("title", ["N/A"])[0],
                "global_id": item.get("globalId", ["N/A"])[0],
                "primary_category": item["primaryCategory"][0].get("categoryName", ["N/A"])[0],
                "gallery_url": item.get("galleryURL", ["N/A"])[0],
                "view_item_url": item.get("viewItemURL", ["N/A"])[0],
                "auto_pay": item.get("autoPay", ["N/A"])[0],
                "postal_code": item.get("postalCode", ["N/A"])[0],
                "location": item.get("location", ["N/A"])[0],
                "country": item.get("country", ["N/A"])[0],
                "shipping_cost": item["shippingInfo"][0].get("shippingServiceCost", [{}])[0].get("__value__", "N/A"),
                "shipping_type": item["shippingInfo"][0].get("shippingType", ["N/A"])[0],
                "ship_to_locations": item["shippingInfo"][0].get("shipToLocations", ["N/A"])[0],
                "expedited_shipping": item["shippingInfo"][0].get("expeditedShipping", ["N/A"])[0],
                "current_price": item["sellingStatus"][0].get("currentPrice", [{}])[0].get("__value__", "N/A"),
                "converted_price": item["sellingStatus"][0].get("convertedCurrentPrice", [{}])[0].get("__value__", "N/A"),
                "selling_state": item["sellingStatus"][0].get("sellingState", ["N/A"])[0],
                "time_left": item["sellingStatus"][0].get("timeLeft", ["N/A"])[0],
                "best_offer_enabled": item["listingInfo"][0].get("bestOfferEnabled", ["N/A"])[0],
                "buy_it_now_available": item["listingInfo"][0].get("buyItNowAvailable", ["N/A"])[0],
                "start_time": item["listingInfo"][0].get("startTime", ["N/A"])[0],
                "end_time": item["listingInfo"][0].get("endTime", ["N/A"])[0],
                "gift": item["listingInfo"][0].get("gift", ["N/A"])[0],
                "returns_accepted": item.get("returnsAccepted", ["N/A"])[0],
                "is_multi_variation_listing": item.get("isMultiVariationListing", ["N/A"])[0],
                "top_rated_listing": item.get("topRatedListing", ["N/A"])[0],
            }

            # Handle the case where "condition" is not present in the response
            if "condition" in item:
                structured_data_item["condition_id"] = item["condition"][0].get("conditionId", ["N/A"])[0]
                structured_data_item["condition_display_name"] = item["condition"][0].get("conditionDisplayName", ["N/A"])[0]
            else:
                structured_data_item["condition_id"] = "N/A"
                structured_data_item["condition_display_name"] = "N/A"

            # Append the structured data item to the list
            structured_data.append(structured_data_item)

        # Save the data as a CSV file
        with open("ebay_data4.csv", "w", newline="") as csvfile:
            fieldnames = structured_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in structured_data:
                writer.writerow(row)

        print("Data has been saved to ebay_data.csv")
    else:
        print("No Acknowledgment (Ack) found in the response.")
else:
    # Handle the error if the request was not successful
    print("Error: Failed to retrieve data from eBay API")
