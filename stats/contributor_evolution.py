#!/usr/bin/env python3
"""
Git Contributors Evolution Analyzer

This script analyzes the evolution of contributors in a Git repository over time,
providing both yearly and monthly breakdowns of contributor counts.
"""

import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import argparse
import os
import sys
from collections import defaultdict
from aquarel import load_theme



class GitContributorAnalyzer:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.commits_data = []

    def get_git_log_data(self):
        """Extract commit data from git log."""
        try:
            # Get all commits with author info and dates
            cmd = [
                "git",
                "log",
                "--pretty=format:%H|%an|%ae|%ad|%s",
                "--date=iso",
                # "--all",  # Include all branches
            ]

            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, check=True
            )

            commits = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("|", 4)
                    if len(parts) >= 4:
                        commit_hash, author_name, author_email, date_str = parts[:4]
                        subject = parts[4] if len(parts) > 4 else ""

                        # Parse the date
                        try:
                            commit_date = datetime.strptime(
                                date_str.split()[0], "%Y-%m-%d"
                            )
                            commits.append(
                                {
                                    "hash": commit_hash,
                                    "author_name": author_name.strip(),
                                    "author_email": author_email.strip().lower(),
                                    "date": commit_date,
                                    "subject": subject,
                                }
                            )
                        except ValueError:
                            continue

            self.commits_data = commits
            print(f"Extracted {len(commits)} commits from the repository")
            return commits

        except subprocess.CalledProcessError as e:
            print(f"Error running git command: {e}")
            return []
        except FileNotFoundError:
            print("Git not found. Please ensure git is installed and in your PATH.")
            return []

    def normalize_contributors(self, commits):
        """Normalize contributor identities by email."""
        # Group by email to handle name variations
        email_to_names = defaultdict(set)
        for commit in commits:
            email_to_names[commit["author_email"]].add(commit["author_name"])

        # Use the most common name for each email
        email_to_preferred_name = {}
        for email, names in email_to_names.items():
            if len(names) == 1:
                email_to_preferred_name[email] = list(names)[0]
            else:
                # Choose the longest name (usually most complete)
                email_to_preferred_name[email] = max(names, key=len)

        # Update commits with normalized names
        for commit in commits:
            commit["normalized_name"] = email_to_preferred_name[commit["author_email"]]

        return commits

    def analyze_contributors_over_time(self, period="monthly"):
        """Analyze contributor evolution over time."""
        if not self.commits_data:
            print("No commit data available. Run get_git_log_data() first.")
            return None

        # Normalize contributors
        commits = self.normalize_contributors(self.commits_data.copy())

        # Create DataFrame
        df = pd.DataFrame(commits)
        df["date"] = pd.to_datetime(df["date"])

        # Define grouping based on period
        if period == "yearly":
            df["period"] = df["date"].dt.year
        elif period == "monthly":
            df["period"] = df["date"].dt.to_period("M")
        else:
            raise ValueError("Period must be 'yearly' or 'monthly'")

        # Calculate statistics for each period
        results = []
        all_contributors = set()

        for period_val in sorted(df["period"].unique()):
            period_commits = df[df["period"] == period_val]
            period_contributors = set(period_commits["author_email"].unique())

            # Update cumulative contributors
            all_contributors.update(period_contributors)

            # New contributors in this period
            existing_contributors = set()
            for prev_period in sorted(df["period"].unique()):
                if prev_period >= period_val:
                    break
                prev_commits = df[df["period"] == prev_period]
                existing_contributors.update(prev_commits["author_email"].unique())

            new_contributors = period_contributors - existing_contributors

            results.append(
                {
                    "period": period_val,
                    "new_contributors": len(new_contributors),
                    "active_contributors": len(period_contributors),
                    "cumulative_contributors": len(all_contributors),
                    "total_commits": len(period_commits),
                }
            )

        return pd.DataFrame(results)

    def get_contributor_details(self):
        """Get detailed information about all contributors."""
        if not self.commits_data:
            return None

        commits = self.normalize_contributors(self.commits_data.copy())
        df = pd.DataFrame(commits)

        contributor_stats = (
            df.groupby(["author_email", "normalized_name"])
            .agg({"hash": "count", "date": ["min", "max"]})
            .round(2)
        )

        contributor_stats.columns = ["total_commits", "first_commit", "last_commit"]
        contributor_stats = contributor_stats.reset_index()
        contributor_stats["active_period_days"] = (
            contributor_stats["last_commit"] - contributor_stats["first_commit"]
        ).dt.days

        return contributor_stats.sort_values("total_commits", ascending=False)

    def plot_evolution(self, data, period="monthly", save_path=None):
        """Create visualizations of contributor evolution."""
        if data is None or data.empty:
            print("No data to plot")
            return

        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(
            f"Git Repository Contributor Evolution ({period.title()})", fontsize=16
        )

        # Convert period to string for plotting if it's a Period object
        plot_data = data.copy()
        plot_data["period_str"] = plot_data["period"].astype(str)

        # Plot 1: Cumulative contributors over time
        axes[0, 0].plot(
            plot_data["period_str"],
            plot_data["cumulative_contributors"],
            marker="o",
            linewidth=2,
            markersize=4,
        )
        axes[0, 0].set_title("All Contributors (Cumulative)")
        axes[0, 0].set_ylabel("Total Contributors")
        axes[0, 0].tick_params(axis="x", rotation=45)
        axes[0, 0].grid(True, alpha=0.3)

        # Plot 2: New contributors per period
        axes[0, 1].bar(
            plot_data["period_str"], plot_data["new_contributors"], alpha=0.7
        )
        axes[0, 1].set_title("New Contributors Per Period")
        axes[0, 1].set_ylabel("New Contributors")
        axes[0, 1].tick_params(axis="x", rotation=45)
        axes[0, 1].grid(True, alpha=0.3)

        # Plot 3: Active contributors per period
        axes[1, 0].plot(
            plot_data["period_str"],
            plot_data["active_contributors"],
            marker="s",
            color="green",
            linewidth=2,
            markersize=4,
        )
        axes[1, 0].set_title("Active Contributors Per Period")
        axes[1, 0].set_ylabel("Active Contributors")
        axes[1, 0].tick_params(axis="x", rotation=45)
        axes[1, 0].grid(True, alpha=0.3)

        # Plot 4: Commits per period
        axes[1, 1].bar(
            plot_data["period_str"],
            plot_data["total_commits"],
            alpha=0.7,
            color="orange",
        )
        axes[1, 1].set_title("Commits Per Period")
        axes[1, 1].set_ylabel("Number of Commits")
        axes[1, 1].tick_params(axis="x", rotation=45)
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Plot saved to {save_path}")

        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Git repository contributor evolution"
    )
    parser.add_argument(
        "--repo",
        "-r",
        default=".",
        help="Path to git repository (default: current directory)",
    )
    parser.add_argument(
        "--period",
        "-p",
        choices=["monthly", "yearly"],
        default="yearly",
        help="Analysis period (default: monthly)",
    )
    parser.add_argument("--output", "-o", help="Output CSV file path")
    parser.add_argument("--plot", help="Save plot to file")
    parser.add_argument(
        "--contributors",
        action="store_true",
        help="Show detailed contributor information",
    )

    args = parser.parse_args()

    # Check if the specified path is a git repository
    if not os.path.exists(os.path.join(args.repo, ".git")):
        print(f"Error: {args.repo} is not a git repository")
        sys.exit(1)

    # Initialize analyzer
    analyzer = GitContributorAnalyzer(args.repo)

    # Extract data
    print("Extracting commit data from repository...")
    commits = analyzer.get_git_log_data()

    if not commits:
        print("No commits found or error occurred")
        sys.exit(1)

    # Analyze evolution
    print(f"Analyzing contributor evolution ({args.period})...")
    evolution_data = analyzer.analyze_contributors_over_time(args.period)

    if evolution_data is not None:
        print(f"\n{args.period.title()} Contributor Evolution Summary:")
        print(evolution_data.to_string(index=False))

        # Save to CSV if requested
        if args.output:
            evolution_data.to_csv(args.output, index=False)
            print(f"\nData saved to {args.output}")

        # Create plots
        analyzer.plot_evolution(evolution_data, args.period, args.plot)

    # Show contributor details if requested
    if args.contributors:
        print("\nDetailed Contributor Information:")
        contributor_details = analyzer.get_contributor_details()
        if contributor_details is not None:
            print(contributor_details.to_string(index=False))


if __name__ == "__main__":
    with load_theme("gruvbox_dark"):
        main()
