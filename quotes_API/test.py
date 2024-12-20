import requests

url = "https://quotes15.p.rapidapi.com/quotes/random/"

querystring = {"language_code":"en"}

headers = {
	"x-rapidapi-key": "0974a2807cmshde98edf62b3d3bbp1cfd55jsne336b98e3057",
	"x-rapidapi-host": "quotes15.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())