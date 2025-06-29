#!/usr/bin/env python3
"""
Git Tech Debt Analyzer
Analyzes git repository history to measure various tech debt metrics
"""

import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict, Counter
import os
import sys
from pathlib import Path
from aquarel import load_theme


class GitTechDebtAnalyzer:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.file_extensions = {
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".html",
            ".css",
            ".scss",
            ".tex",
            ".txt",
            ".rst",
        }

    def run_git_command(self, command):
        """Run a git command and return the output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {command}")
            print(f"Error: {e.stderr}")
            return ""

    def get_file_history(self, file_path):
        """Get the commit history for a specific file"""
        cmd = (
            f'git log --follow --pretty=format:"%H|%ad|%an" --date=iso -- "{file_path}"'
        )
        output = self.run_git_command(cmd)

        commits = []
        for line in output.split("\n"):
            if line.strip():
                parts = line.split("|")
                if len(parts) == 3:
                    hash_val, date_str, author = parts
                    try:
                        date = datetime.fromisoformat(
                            date_str.replace(" ", "T", 1).rsplit(" ", 1)[0]
                        )
                        commits.append(
                            {
                                "hash": hash_val,
                                "date": date,
                                "author": author,
                                "file": file_path,
                            }
                        )
                    except ValueError:
                        continue
        return commits

    def get_all_tracked_files(self):
        """Get all tracked files with relevant extensions"""
        cmd = "git ls-files"
        output = self.run_git_command(cmd)

        files = []
        for file_path in output.split("\n"):
            if file_path.strip():
                path_obj = Path(file_path)
                if path_obj.suffix.lower() in self.file_extensions:
                    files.append(file_path)
        return files

    def analyze_line_survival(self):
        """Analyze how long lines of code survive before being changed"""
        files = self.get_all_tracked_files()

        # Limit analysis to avoid overwhelming the system
        # if len(files) > max_files:
        #     files = files[:max_files]
        #     print(
        #         f"Analyzing sample of {max_files} files out of {len(self.get_all_tracked_files())} total files"
        #     )

        line_lifespans = []
        file_stats = []

        for i, file_path in enumerate(files):
            print(f"Analyzing {file_path} ({i + 1}/{len(files)})")

            # Get blame information to see when each line was last changed
            cmd = f'git blame --line-porcelain "{file_path}"'
            blame_output = self.run_git_command(cmd)

            if not blame_output:
                continue

            commit_dates = {}
            current_commit = None

            for line in blame_output.split("\n"):
                if re.match(r"^[a-f0-9]{40}", line):
                    current_commit = line.split()[0]
                elif line.startswith("committer-time "):
                    timestamp = int(line.split()[1])
                    commit_dates[current_commit] = datetime.fromtimestamp(timestamp)

            # Calculate line ages
            now = datetime.now()
            ages = []
            for commit_hash, commit_date in commit_dates.items():
                age_days = (now - commit_date).days
                ages.append(age_days)
                line_lifespans.append(
                    {
                        "file": file_path,
                        "age_days": age_days,
                        "commit_date": commit_date,
                    }
                )

            if ages:
                file_stats.append(
                    {
                        "file": file_path,
                        "avg_line_age": np.mean(ages),
                        "median_line_age": np.median(ages),
                        "max_line_age": max(ages),
                        "total_lines": len(ages),
                    }
                )

        return pd.DataFrame(line_lifespans), pd.DataFrame(file_stats)

    def create_visualizations(self, line_data):
        """Create comprehensive visualizations of tech debt metrics"""
        fig = plt.figure(figsize=(16, 9))

        # 1. Line Age Distribution
        # ax1 = plt.subplot(1, 2, 1)
        if not line_data.empty:
            plt.hist(line_data["age_days"], bins=50, alpha=0.7, edgecolor="black")
            plt.axvline(
                line_data["age_days"].mean(),
                color="red",
                linestyle="--",
                label=f"Mean: {line_data['age_days'].mean():.0f} days",
            )
            plt.xlabel("Line Age (days)")
            plt.ylabel("Frequency")
            plt.title("Line Age Distribution")
            plt.legend()
            plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(
            "../assets/slides/stats/tech_debt.png", dpi=300, bbox_inches="tight"
        )
        plt.show()


def main():
    print("Git Tech Debt Analyzer")
    print("=" * 50)

    # Initialize analyzer
    # repo_path = input(
    #     "Enter repository path (or press Enter for current directory): "
    # ).strip()
    # if not repo_path:
    repo_path = "/home/tomas/dev/indico"

    analyzer = GitTechDebtAnalyzer(repo_path)

    # Check if it's a git repository
    if not analyzer.run_git_command("git rev-parse --git-dir"):
        print("Error: Not a git repository!")
        return

    print("\n1. Analyzing line survival rates...")
    line_data, file_stats = analyzer.analyze_line_survival()

    print("\n4. Creating visualizations...")
    analyzer.create_visualizations(line_data)

    print("\nAnalysis complete! Check 'tech_debt_analysis.png' for visualizations.")

    # Print some key insights
    print("\nKey Insights:")
    print("-" * 30)

    if not line_data.empty:
        avg_age = line_data["age_days"].mean()
        print(f"• Average line age: {avg_age:.0f} days ({avg_age / 365:.1f} years)")

        old_lines = (line_data["age_days"] > 365 * 2).sum()
        total_lines = len(line_data)
        print(
            f"• Lines older than 2 years: {old_lines:,} ({old_lines / total_lines * 100:.1f}%)"
        )


if __name__ == "__main__":
    with load_theme("gruvbox_dark"):
        main()
