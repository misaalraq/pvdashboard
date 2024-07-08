import requests
from colorama import Fore, Style

def get_user_info(init_data_line):
    url = 'https://api.pixelverse.xyz/api/users/@me'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'authorization': init_data_line,
        'origin': 'https://dashboard.pixelverse.xyz',
        'pragma': 'no-cache',
        'referer': 'https://dashboard.pixelverse.xyz/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"{Fore.RED}Failed to fetch user info. Status Code: {response.status_code}{Style.RESET_ALL}")
        return
    
    data = response.json()
    
    # Handle missing 'profile' or 'username' gracefully
    username = data.get('profile', {}).get('username', 'Unknown')
    
    balance = data.get('spendablePoints', {}).get('amount', 0)
    formatted_balance = f"{balance:,.0f}".replace(',', '.')  # Format balance with dot as thousands separator
    email = data.get('email', 'No email provided')
    referral_code = data.get('referralCode', 'No referral code')
    is_cheater = data.get('isCheater', 'Unknown')
    active_pet = f"{data.get('pet', {}).get('customName', 'Belum ada pet')} | Level {data.get('pet', {}).get('level', '0')}"
    
    wallet = next((wallet['provider'] for wallet in data.get('connectedWallets', [])), 'No wallet')
    
    telegram_info = 'Not connected to Telegram'
    twitter_info = 'Not connected to Twitter'
    discord_info = 'Not connected to Discord'
    for social in data.get('connectedSocials', []):
        if social['social']['name'] == 'Telegram':
            telegram_info = f"{social['socialData']['firstName']} {social['socialData']['lastName']} | @{social['socialData']['username']}"
        elif social['social']['name'] == 'Twitter':
            twitter_info = f"{social['socialData']['name']} | @{social['socialData']['username']}"
        elif social['social']['name'] == 'Discord':
            discord_info = f"{social['socialData']['username']}"
    
    print(f"{Fore.WHITE + Style.BRIGHT}======[ {username} ]======{Style.RESET_ALL}")
    print(f"{Fore.CYAN + Style.BRIGHT}Balance        : {formatted_balance}{Style.RESET_ALL}")
    print(f"{Fore.CYAN + Style.BRIGHT}Email          : {email}{Style.RESET_ALL}")
    print(f"{Fore.CYAN + Style.BRIGHT}Referral       : {referral_code}{Style.RESET_ALL}")
    print(f"{Fore.GREEN + Style.BRIGHT}Cheater Status : {is_cheater}{Style.RESET_ALL}")
    print(f"{Fore.GREEN + Style.BRIGHT}Active Pet     : {active_pet}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW + Style.BRIGHT}Wallet         : {wallet}{Style.RESET_ALL}")
    print(f"{Fore.BLUE + Style.BRIGHT}Telegram       : {telegram_info}{Style.RESET_ALL}")
    print(f"{Fore.WHITE + Style.BRIGHT}Twitter        : {twitter_info}{Style.RESET_ALL}")
    print(f"{Fore.BLUE + Style.BRIGHT}Discord        : {discord_info}{Style.RESET_ALL}")

def level_up_pet(pet_id, init_data_line):
    url = f'https://api.pixelverse.xyz/api/pets/user-pets/{pet_id}/level-up'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': init_data_line,
        'cache-control': 'no-cache',
        'content-length': '0',
        'origin': 'https://dashboard.pixelverse.xyz',
        'pragma': 'no-cache',
        'referer': 'https://dashboard.pixelverse.xyz/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Your_User_Agent'
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 201:
        print(f"{Fore.GREEN}Pet {pet_id} leveled up successfully!{Style.RESET_ALL}")
    else:   
        if response.status_code == 400:
            if response.json().get('message') == 'You can level up a pet only once in 24 hours':
                print(f"{Fore.RED}Sudah di upgrade.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Failed to level up pet {pet_id}. Error {response.json()}.{Style.RESET_ALL}")

def get_pet_list(init_data_line):
    url = 'https://api.pixelverse.xyz/api/pets'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'authorization': init_data_line,
        'origin': 'https://dashboard.pixelverse.xyz',
        'pragma': 'no-cache',
        'referer': 'https://dashboard.pixelverse.xyz/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"{Fore.RED}Failed to fetch pet list. Status Code: {response.status_code}{Style.RESET_ALL}")
        return
    
    try:
        pets = response.json()
        if not isinstance(pets, list):
            print(f"{Fore.RED}Unexpected response format. Expected a list of pets.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.WHITE + Style.BRIGHT}======[ List Pet ]======{Style.RESET_ALL}")
        for pet in pets:
            name = pet.get('name', 'Belum ada pet')
            level = pet.get('userPet', {}).get('level', 0)
            id_pet = pet.get('userPet', {}).get('id', 0)
            print(f"{Fore.CYAN + Style.BRIGHT}{name} Level: {level}{Style.RESET_ALL}")
            level_up_pet(id_pet, init_data_line)
            select_pet(id_pet, init_data_line)
    except Exception as e:
        print(f"{Fore.RED}Error processing pet list: {e}{Style.RESET_ALL}")

def select_pet(pet_id, init_data_line):
    url = f'https://api.pixelverse.xyz/api/pets/user-pets/{pet_id}/select'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': init_data_line,
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://dashboard.pixelverse.xyz',
        'pragma': 'no-cache',
        'referer': 'https://dashboard.pixelverse.xyz/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers, json={})
    
    if response.status_code == 201:
        print(f"{Fore.GREEN}Pet selected!{Style.RESET_ALL}")
        daily_check_in(init_data_line)
    else:
        print(f"{Fore.RED}Failed to select pet {pet_id}. Error: {response.json()}{Style.RESET_ALL}")

def daily_check_in(init_data_line):
    url = 'https://api.pixelverse.xyz/api/daily-reward/complete'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': init_data_line,
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://dashboard.pixelverse.xyz',
        'pragma': 'no-cache',
        'referer': 'https://dashboard.pixelverse.xyz/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers, json={})
    if response.status_code == 400:
        print(f"{Fore.RED + Style.BRIGHT}Sudah Daily !{Style.RESET_ALL}")
    else:
        data = response.json()
        print(f"{Fore.GREEN + Style.BRIGHT}Day {data['currentStreak']} | {data['dailyUserActions'][0]['daily_action']['name']} | {data['dailyUserActions'][0]['daily_action']['reward']}")

# Call the function to perform daily check-in

with open('tokens.txt', 'r') as file:
    init_data_lines = file.readlines()

for init_data_line in init_data_lines:
        init_data_line = init_data_line.strip()   
        get_user_info(init_data_line)
        get_pet_list(init_data_line)
