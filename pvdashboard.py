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
    data = response.json()
    
    email = data.get('email', 'No email provided')
    username = data['profile']['username']
    balance = data['spendablePoints'].get('amount', 0)
    formatted_balance = f"{balance:,.0f}".replace(',', '.')  # Format balance with dot as thousands separator
    referral_code = data.get('referralCode', 'No referral code')
    is_cheater = data.get('isCheater', 'Unknown')
    
    active_pet_data = data.get('pet', {})
    active_pet_name = active_pet_data.get('customName', 'Belum ada pet')
    active_pet_level = active_pet_data.get('level', '0')
    active_pet = f"{active_pet_name} | Level {active_pet_level}"
    
    connected_wallets = data.get('connectedWallets', [])
    wallet_provider = next((wallet.get('provider', 'No wallet') for wallet in connected_wallets), 'No wallet')

    telegram_info = 'Not connected to Telegram'
    twitter_info = 'Not connected to Twitter'
    discord_info = 'Not connected to Discord'
    for social in data.get('connectedSocials', []):
        social_name = social.get('social', {}).get('name', '')
        social_data = social.get('socialData', {})
        if social_name == 'Telegram':
            telegram_first_name = social_data.get('firstName', '')
            telegram_last_name = social_data.get('lastName', '')
            telegram_username = social_data.get('username', '')
            telegram_info = f"{telegram_first_name} {telegram_last_name} | @{telegram_username}"
        elif social_name == 'Twitter':
            twitter_name = social_data.get('name', '')
            twitter_username = social_data.get('username', '')
            twitter_info = f"{twitter_name} | @{twitter_username}"
        elif social_name == 'Discord':
            discord_username = social_data.get('username', '')
            discord_info = f"{discord_username}"
    
    print(f"{Fore.WHITE + Style.BRIGHT}======[ {username} ]======{Style.RESET_ALL}")
    print(f"{Fore.CYAN + Style.BRIGHT}Balance        : {formatted_balance}{Style.RESET_ALL}")
    print(f"{Fore.CYAN + Style.BRIGHT}Email          : {email}{Style.RESET_ALL}")
    print(f"{Fore.CYAN + Style.BRIGHT}Referral       : {referral_code}{Style.RESET_ALL}")
    print(f"{Fore.GREEN + Style.BRIGHT}Cheater Status : {is_cheater}{Style.RESET_ALL}")
    print(f"{Fore.GREEN + Style.BRIGHT}Active Pet     : {active_pet}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW + Style.BRIGHT}Wallet         : {wallet_provider}{Style.RESET_ALL}")
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
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
    pets = response.json()
    
    print(f"{Fore.WHITE + Style.BRIGHT}======[ List Pet ]======{Style.RESET_ALL}")
    for pet in pets:
        pet_name = pet.get('name', 'Belum ada pet')
        user_pet_data = pet.get('userPet', {})
        pet_level = user_pet_data.get('level', 0)
        pet_id = user_pet_data.get('id', 0)
        
        print(f"{Fore.CYAN + Style.BRIGHT}{pet_name} Level: {pet_level}{Style.RESET_ALL}")
        level_up_pet(pet_id, init_data_line)
        select_pet(pet_id, init_data_line)

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
        print(f"{Fore.RED}Gagal memilih hewan peliharaan {pet_id}. Error: {response.json()}{Style.RESET_ALL}")

