import requests

url = "http://127.0.0.1:5000/getResult"
payload = {
    "candidates": ["Pizza", "Burger", "Pasta", "Salad", "Sandwich"],
    "ballots": [
        [1, 2, 3, 4, 5], 
        [2, 1, 4, 3, 5], 
        [3, 4, 1, 2, 5], 
        [1, 3, 2, 5, 4], 
        [4, 3, 1, 5, 2], 
        [2, 1, 3, 5, 4], 
        [3, 2, 1, 4, 5], 
        [5, 4, 3, 2, 1]  
    ]
}

# Sending POST request
response = requests.post(url, json=payload)

# Printing the response
print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())
