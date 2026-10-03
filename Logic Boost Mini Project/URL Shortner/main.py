import re

class URLShortener:
    def __init__(self):
        self.url_map = {}
        self.current_id = 1000
        self.base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def base62_encode(self, number):
        if number == 0:
            return self.base62[0]

        encoded_string = ""
        while number > 0:
            encoded_string = self.base62[number % 62] + encoded_string
            number //= 62
        return encoded_string

    def shorten_url(self, long_url):
        unique_id = self.current_id
        self.current_id += 1
        short_code = self.base62_encode(unique_id)
        self.url_map[short_code] = long_url
        return short_code

    def get_long_url(self, short_code):
        return self.url_map.get(short_code, "URL not found")

def get_validated_url():
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

    while True:
        user_input = input("Please enter a valid URL (e.g., https://example.com): ")
        if url_pattern.match(user_input):
            return user_input
        else:
            print("Invalid URL format. Please start with 'http://' or 'https://'.")

# --- Execution ---
shortener = URLShortener()

print("--- URL Shortener Demo ---")

# 1. Get validated URL from user
url_to_shorten = get_validated_url()

# 2. Shorten the URL
short_code = shortener.shorten_url(url_to_shorten)

# 3. Display results
print(f"\nOriginal URL: {url_to_shorten}")
print(f"Generated Short Code: **{short_code}**")

# 4. Test Retrieval
retrieved_url = shortener.get_long_url(short_code)
print(f"Retrieving {short_code} -> {retrieved_url}")