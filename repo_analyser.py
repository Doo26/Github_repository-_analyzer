class Repository:
    # Models a single Github repository from raw JSON.

    def __init__(self, raw_data: dict):
        self.name = raw_data.get("name", "Unnamed")
        self.stars = raw_data.get("stargazers_count", 0)
        self.forks = raw_data.get("forks_count", 0)
        self.language =  raw_data.get("language") or "Unknown"

    def is_popular(self) -> bool:
        return self.stars >= 100
    
    def summary(self) -> str:
        stars = format_large_number(self.stars)
        flag = "fire" if self.is_popular() else " "

        return f"{flag} {self.name} |  {stars}  | {self.language}"
    
# A function to calculate the average number of stars a git hub user has 
def format_large_number(number: int) ->str:
    # for instance the 24000 becomes 24K
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.2f}K"
    return str(number)


## This function helps to calculate the average number of stars that a user has 

def calc_avg_stars(stars: list) -> float:
    if not stars:
        return 0.0
    return round(sum(stars) / len(stars), 2)


# This function is going to help us to look for the language with the most use in the persons github repository
def get_top_lang(languages: list) -> str:
    counts = {}

    for lang in languages:
        counts[lang] = counts.get(lang, 0) + 1
    return max(counts, key=counts.get)


# This is the funtion to handle the api calls 

import requests

def get_user_repos(username: str) ->list:
    url = f"https://api.github.com/users/{username}/repos"
    params = {"sort": "updated", "per_page": 10}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"X Http error: (e)")
    except requests.exceptions.ConnectionError:
        print("X connection error.")
    except requests.exceptions.Timeout:
        print("X Request timed out. ")

    return []






def main():
    username = input("Enter a Github username: ").strip()
    raw_repos = get_user_repos(username)

    if not raw_repos:
        print("No data to display.")
        return
    # This is the bridge between raw dict and repository objects
    
    repos = [Repository(item) for item in raw_repos]
    repos.sort(key=lambda r: r.stars, reverse= True)

    for repo in repos:
        print(repos.summary())

    avg = calc_avg_stars(repos)
    top_lang = get_top_lang(repos)
    print(f" Average stars: {avg}")
    print(f" Top language: {top_lang}")

if __name__ == "__main__":
    main()
