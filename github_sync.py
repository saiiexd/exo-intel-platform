"""
github_sync.py
==============
Automated Repository Synchronization Utility.

Manages the Git lifecycle for the ExoIntel platform, providing automated 
staging, commitment, and synchronization with remote repositories. 
Includes support for semantic version tagging.
"""

import subprocess
import sys
import argparse
from datetime import datetime

def run_command(command, description):
    """Executes a shell command and prints progress."""
    print(f"Executing: {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error during '{description}':")
        print(e.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="ExoIntel GitHub Sync Utility")
    parser.add_argument("-m", "--message", help="Commit message")
    parser.add_argument("-t", "--tag", help="Create and push a version tag (e.g., v1.0.0)")
    args = parser.parse_args()

    # 1. Check for changes
    status = run_command(["git", "status", "--short"], "Checking repository status")
    if status is None:
        return

    if not status and not args.tag:
        print("Repository is already synchronized. Nothing to commit.")
        return

    # 2. Stage changes
    if status:
        run_command(["git", "add", "."], "Staging repository changes")

        # 3. Create commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = args.message if args.message else f"Automated ExoIntel Platform Update - {timestamp}"
        run_command(["git", "commit", "-m", commit_msg], "Creating commit")

        # 4. Push updates
        run_command(["git", "push", "origin", "main"], "Pushing updates to GitHub")

    # 5. Handle Tagging
    if args.tag:
        print(f"Tagging version: {args.tag}")
        run_command(["git", "tag", args.tag], f"Creating tag {args.tag}")
        run_command(["git", "push", "origin", args.tag], f"Pushing tag {args.tag} to GitHub")

    print("\nSynchronization complete!")

if __name__ == "__main__":
    main()
