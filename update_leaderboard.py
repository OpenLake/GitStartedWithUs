import json
import os
from github import Github

repository_owner = "sk-pathak"
repository_name = "GitStartedWithUs"
github_token = os.getenv("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")

leaderboard_file = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as f:
            leaderboard = json.load(f)
    else:
        leaderboard = {}
    return leaderboard

def update_leaderboard(leaderboard, contributor, points):
    if contributor in leaderboard:
        leaderboard[contributor] += points
    else:
        leaderboard[contributor] = points

def save_leaderboard(leaderboard):
    with open(leaderboard_file, "w") as f:
        json.dump(leaderboard, f, indent=4)

def main():
    g = Github(github_token)
    repo = g.get_repo(f"{repository_owner}/{repository_name}")

    pull_requests = repo.get_pulls(state="closed", sort="updated", direction="desc")
    for pr in pull_requests:
        if pr.merged:
            contributor = pr.user.login
            points = 1
            leaderboard = load_leaderboard()
            update_leaderboard(leaderboard, contributor, points)
            save_leaderboard(leaderboard)
            print(f"{contributor} has been awarded {points} points for merging a pull request.")

if __name__ == "__main__":
    main()
