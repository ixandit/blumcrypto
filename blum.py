import argparse
import requests
import time
import random
from datetime import datetime

def get_headers(authorization_token):
    """Generate headers for requests."""
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'authorization': authorization_token
    }

def fetch_tasks(authorization_token):
    """Fetch available tasks."""
    url = 'https://game-domain.blum.codes/api/v1/tasks'
    response = requests.get(url, headers=get_headers(authorization_token))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch tasks. {response.json().get('message')}")
        return []

def claim_task(authorization_token):
    """Claim available tasks and their subtasks."""
    base_url = 'https://game-domain.blum.codes/api/v1/tasks/'
    tasks = fetch_tasks(authorization_token)
    for task in tasks:
        task_id = task['id']
        start_url = f"{base_url}{task_id}/start"
        claim_url = f"{base_url}{task_id}/claim"
        start = requests.post(start_url, headers=get_headers(authorization_token))
        if start.status_code == 200:
            print(f"Started task {task.get('title', 'Unknown Title')}")
        response = requests.post(claim_url, headers=get_headers(authorization_token))
        if response.status_code == 200:
            claimed_task = response.json().get('title', 'Unknown Task')
            print(f"Claimed task: {claimed_task}")
        else:
            print(f"Failed to claim task {task.get('title', 'Unknown Title')}. {response.json().get('message')}")
        # Check for subtasks and claim them if they exist
        if 'subTasks' in task:
            for subtask in task['subTasks']:
                subtask_id = subtask['id']
                subtask_claim_url = f"{base_url}{subtask_id}/claim"
                subtask_response = requests.post(subtask_claim_url, headers=get_headers(authorization_token))
                if subtask_response.status_code == 200:
                    claimed_subtask = subtask_response.json().get('title', 'Unknown Subtask')
                    print(f"Claimed subtask: {claimed_subtask}")
                else:
                    print(f"Failed to claim subtask {subtask.get('title', 'Unknown Title')}. {subtask_response.json().get('message')}")


def claim_game_points(authorization_token, game_id, points):
    """Claim points for a game."""
    url = 'https://game-domain.blum.codes/api/v1/game/claim'
    data = {'gameId': game_id, 'points': points}
    response = requests.post(url, headers=get_headers(authorization_token), json=data)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to claim game points. {response.json().get('message')}"

def claim_fren_points(authorization_token):
    """Claim points from friends"""
    url = "https://gateway.blum.codes/v1/friends/claim"
    response = requests.post(url, headers=get_headers(authorization_token))
    if response.status_code == 200:
        print(f" Claimed {response.json().get('claimBalance')} points")
    else:
        print(f"Failed to claim fren points. {response.json().get('message')}")

def generate_game_id(authorization_token):
    """Generate a new game ID."""
    url = 'https://game-domain.blum.codes/api/v1/game/play'
    response = requests.post(url, headers=get_headers(authorization_token))
    if response.status_code == 200:
        return response.json().get("gameId")
    else:
        print(f"Failed to generate game ID. {response.json().get('message')}")
        return None

def get_balance(authorization_token):
    """Get the current user balance."""
    url = "https://game-domain.blum.codes/api/v1/user/balance"
    response = requests.get(url, headers=get_headers(authorization_token))
    if response.status_code == 200:
        return response.json().get("availableBalance")
    else:
        print(f"Failed to get balance. {response.json().get('message')}")
        return None

def play_game(authorization_token, num_games):
    """Play a specified number of games."""
    for _ in range(num_games):
        initial_balance = get_balance(authorization_token)
        if initial_balance is None:
            return

        game_id = generate_game_id(authorization_token)
        if game_id is None:
            continue

        points = random.randint(280, 500)
        print(f"Generated Game ID: {game_id} for {points} points")

        while True:
            result = claim_game_points(authorization_token, game_id, points)
            if result.lower() == 'ok':
                final_balance = get_balance(authorization_token)
                if final_balance is not None:
                    generated_points = float(final_balance) - float(initial_balance)
                    print(f"Initial balance: {initial_balance}\nInput points: {points}\nFinal balance: {final_balance}\nGenerated points: {generated_points}")
                break
            else:
                time.sleep(0.5)

def start_farming(authorization_token):
    """Claim farming points and start farming tasks."""
    url = 'https://game-domain.blum.codes/api/v1/farming/start'
    response = requests.post(url, headers=get_headers(authorization_token))
    if response.status_code == 200:
        data = response.json()
        start_time = datetime.fromtimestamp(data['startTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.fromtimestamp(data['endTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f'Started at: {start_time}\nEnding at: {end_time}\nEarning Rate: {data['earningsRate']}\nBalance: {data['balance']}')

    else:
        print(f"Failed to start farming. {response.json().get('message')}")
    claim = "https://game-domain.blum.codes/api/v1/farming/claim"
    claim_points = requests.post(claim, headers=get_headers(authorization_token))
    if not claim_points.status_code == 200:
        print(f"Failed to claim farming points. {claim_points.json().get('message')}")


def main():
    """Main function to parse arguments and execute the appropriate function."""
    parser = argparse.ArgumentParser(description='BLUM interaction script.')
    parser.add_argument('token', type=str, help='Authorization token')
    parser.add_argument('--play-games', type=int, help='Number of games to play')
    parser.add_argument('--check-balance', action='store_true', help='Check balance')
    parser.add_argument('--claim-tasks', action='store_true', help='Claim tasks')
    parser.add_argument('--claim-friends', action='store_true', help='Claim friends points')
    parser.add_argument('--start-farming', action='store_true', help='Start farming')

    args = parser.parse_args()

    if args.check_balance:
        balance = get_balance(args.token)
        if balance is not None:
            print(f"Available Balance: {balance}")

    if args.claim_tasks:
        claim_task(args.token)

    if args.start_farming:
        start_farming(args.token)

    if args.play_games:
        play_game(args.token, args.play_games)

    if args.claim_friends:
        claim_fren_points(args.token)

if __name__ == "__main__":
    main()
