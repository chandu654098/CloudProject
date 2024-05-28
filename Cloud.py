import random
from google.cloud import storage
from google.cloud import firestore

# Set up GCP credentials
client = storage.Client()
db = firestore.Client()

# Define the game board size
board_size = 100

# Define the snakes and ladders
snakes_ref = db.collection('snakes').document('snakes')
snakes = snakes_ref.get().to_dict()
ladders_ref = db.collection('ladders').document('ladders')
ladders = ladders_ref.get().to_dict()

# Define the player starting position
player_position_ref = db.collection('players').document('player1')
player_position = player_position_ref.get().to_dict()['position']

print("Welcome to Snake and Ladder game!")
print("You are at position", player_position)

while True:
    # Ask for user input to roll the dice
    input("Press Enter to roll the dice...")
    
    # Roll the dice
    dice = random.randint(1, 6)
    print("You rolled a", dice)
    
    # Move the player
    new_position = player_position + dice
    
    # Check for snakes and ladders
    if new_position in snakes:
        print("Oh no! You landed on a snake at position", new_position)
        player_position = snakes[new_position]
        print("You have been moved to position", player_position)
    elif new_position in ladders:
        print("Yay! You landed on a ladder at position", new_position)
        player_position = ladders[new_position]
        print("You have been moved to position", player_position)
    else:
        player_position = new_position
        print("You are now at position", player_position)
    
    # Update the player position in Firestore
    player_position_ref.set({'position': player_position})
    
    # Check for win
    if player_position >= board_size:
        print("Congratulations, you won!")
        break