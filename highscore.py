import os

HIGHSCORE_FILE = "assets/highscore.txt"

def get_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r") as f:
        return int(f.read().strip())

def save_highscore(score):
    highscore = get_highscore()
    if score > highscore:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))