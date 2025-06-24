#!/usr/bin/env python3
"""
Git Lines of Code and Language Evolution Analyzer

This script analyzes the evolution of lines of code and programming language
composition in a Git repository over time.
"""

import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import argparse
import os
import sys
import tempfile
import shutil
from collections import defaultdict
import re
import json
from aquarel import load_theme



class GitLOCAnalyzer:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.language_extensions = {
            # Programming languages
            "Python": [".py", ".pyx", ".pxd", ".pxi", ".pyw"],
            "JavaScript": [".js", ".mjs", ".cjs"],
            "TypeScript": [".ts"],
            "React": [".jsx", ".tsx"],
            "PHP": [".php", ".php3", ".php4", ".php5", ".phtml"],
            "Shell": [".sh", ".bash", ".zsh", ".fish", ".ksh"],
            "PowerShell": [".ps1", ".psm1", ".psd1"],
            # Web technologies
            "Jinja": [".html", ".htm", ".xhtml"],
            "CSS": [".css", ".scss", ".sass", ".less"],
            # Data and config
            "JSON": [".json"],
            "XML": [".xml", ".xsl", ".xsd"],
            "YAML": [".yml", ".yaml"],
            "TOML": [".toml"],
            "SQL": [".sql"],
            # Documentation
            "Markdown": [".md", ".markdown", ".mdown", ".mkd"],
            "reStructuredText": [".rst"],
            "LaTeX": [".tex", ".latex"],
            # Other
            "Dockerfile": ["dockerfile", "Dockerfile"],
            "Makefile": ["makefile", "Makefile", "GNUmakefile"],
        }

        # Reverse mapping for quick lookup
        self.ext_to_language = {}
        for lang, exts in self.language_extensions.items():
            for ext in exts:
                self.ext_to_language[ext.lower()] = lang

        # Files to ignore
        self.ignore_patterns = [
            r"\.git/",
            r"\.svn/",
            r"\.hg/",
            r"node_modules/",
            r"\.venv/",
            r"__pycache__/",
            r"\.pyc$",
            r"\.pyo$",
            r"\.class$",
            r"\.o$",
            r"\.so$",
            r"\.dll$",
            r"\.exe$",
            r"\.bin$",
            r"\.img$",
            r"\.iso$",
            r"\.dmg$",
            r"\.pkg$",
            r"\.deb$",
            r"\.rpm$",
            r"\.tar",
            r"\.zip$",
            r"\.rar$",
            r"\.7z$",
            r"\.gz$",
            r"\.bz2$",
            r"\.xz$",
            r"\.(jpg|jpeg|png|gif|bmp|tiff|svg|ico)$",
            r"\.(mp3|wav|flac|ogg|mp4|avi|mkv|mov|wmv)$",
            r"\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
            r"\.min\.(js|css)$",
            r"dist/",
            r"build/",
            r"target/",
            r"\.DS_Store$",
            r"thumbs\.db$",
        ]

    def get_commits_timeline(self, sample_commits=50):
        """Get a timeline of commits to analyze."""
        try:
            # Get all commit hashes with dates
            cmd = ["git", "log", "--pretty=format:%H|%ad", "--date=iso", "--all"]
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, check=True
            )

            commits = []
            for line in result.stdout.strip().split("\n"):
                if line and "|" in line:
                    commit_hash, date_str = line.split("|", 1)
                    try:
                        commit_date = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
                        commits.append({"hash": commit_hash, "date": commit_date})
                    except ValueError:
                        continue

            # Sort by date
            commits.sort(key=lambda x: x["date"])

            if len(commits) <= sample_commits:
                return commits

            # Sample commits evenly across the timeline
            step = len(commits) // sample_commits
            sampled = [commits[i] for i in range(0, len(commits), step)]

            # Always include the latest commit
            if commits[-1] not in sampled:
                sampled.append(commits[-1])

            print(f"Selected {len(sampled)} commits from {len(commits)} total commits")
            return sampled

        except subprocess.CalledProcessError as e:
            print(f"Error getting commit timeline: {e}")
            return []

    def should_ignore_file(self, filepath):
        """Check if a file should be ignored based on patterns."""
        filepath_lower = filepath.lower()
        for pattern in self.ignore_patterns:
            if re.search(pattern, filepath_lower):
                return True
        return False

    def get_language_from_file(self, filepath):
        """Determine programming language from file path."""
        if self.should_ignore_file(filepath):
            return None

        # Handle special cases first
        filename = os.path.basename(filepath).lower()
        if filename in ["dockerfile", "makefile", "gnumakefile"]:
            return self.ext_to_language.get(filename, "Other")

        # Check file extension
        _, ext = os.path.splitext(filepath)
        if ext:
            return self.ext_to_language.get(ext.lower(), "Other")

        return "Other"

    def count_lines_in_file(self, filepath):
        """Count lines in a file, handling encoding issues."""
        try:
            # Try UTF-8 first
            with open(filepath, "r", encoding="utf-8") as f:
                return len(f.readlines())
        except UnicodeDecodeError:
            try:
                # Try latin-1 as fallback
                with open(filepath, "r", encoding="latin-1") as f:
                    return len(f.readlines())
            except:
                # If all else fails, try binary mode and count newlines
                try:
                    with open(filepath, "rb") as f:
                        return f.read().count(b"\n")
                except:
                    return 0
        except:
            return 0

    def analyze_commit(self, commit_hash):
        """Analyze lines of code and languages for a specific commit."""
        temp_dir = None
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()

            # Check out the commit to temporary directory
            cmd = ["git", "archive", commit_hash]
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, check=True
            )

            # Extract to temp directory
            extract_cmd = ["tar", "-xf", "-", "-C", temp_dir]
            subprocess.run(extract_cmd, input=result.stdout, check=True)

            # Analyze files
            language_stats = defaultdict(lambda: {"files": 0, "lines": 0})
            total_files = 0
            total_lines = 0

            for root, dirs, files in os.walk(temp_dir):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith(".")]

                for file in files:
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, temp_dir)

                    if self.should_ignore_file(rel_path):
                        continue

                    language = self.get_language_from_file(rel_path)
                    if language and language != "Other":
                        lines = self.count_lines_in_file(filepath)
                        if lines > 0:
                            language_stats[language]["files"] += 1
                            language_stats[language]["lines"] += lines
                            total_files += 1
                            total_lines += lines

            return dict(language_stats), total_files, total_lines

        except subprocess.CalledProcessError as e:
            print(f"Error analyzing commit {commit_hash[:8]}: {e}")
            return {}, 0, 0
        except Exception as e:
            print(f"Unexpected error analyzing commit {commit_hash[:8]}: {e}")
            return {}, 0, 0
        finally:
            # Cleanup
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def analyze_repository_evolution(self, sample_commits=5):
        """Analyze the evolution of LOC and languages over time."""
        print("Getting commit timeline...")
        commits = self.get_commits_timeline(sample_commits)

        if not commits:
            print("No commits found")
            return None

        results = []
        total_commits = len(commits)

        for i, commit_info in enumerate(commits, 1):
            commit_hash = commit_info["hash"]
            commit_date = commit_info["date"]

            print(
                f"Analyzing commit {i}/{total_commits}: {commit_hash[:8]} ({commit_date.strftime('%Y-%m-%d')})"
            )

            language_stats, total_files, total_lines = self.analyze_commit(commit_hash)

            # Prepare row data
            row_data = {
                "commit_hash": commit_hash,
                "date": commit_date,
                "total_files": total_files,
                "total_lines": total_lines,
                "languages_count": len(language_stats),
            }

            # Add language-specific data
            for language, stats in language_stats.items():
                row_data[f"{language}_files"] = stats["files"]
                row_data[f"{language}_lines"] = stats["lines"]

            results.append(row_data)

        df = pd.DataFrame(results).fillna(0)

        # Ensure all numeric columns are properly typed
        numeric_columns = [
            col for col in df.columns if col not in ["commit_hash", "date"]
        ]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        return df

    def plot_evolution(self, df, save_path=None):
        """Create visualizations of LOC and language evolution."""
        if df is None or df.empty:
            print("No data to plot")
            return

        # Prepare data
        df = df.sort_values("date")
        df["date_str"] = df["date"].dt.strftime("%Y-%m")

        # Get language columns
        language_cols = [
            col
            for col in df.columns
            if col.endswith("_lines") and not col.startswith("total_")
        ]
        languages = [col.replace("_lines", "") for col in language_cols]

        # Create subplots
        fig, axes = plt.subplots(2, 1, figsize=(16, 12))
        # fig.suptitle("Repository Lines of Code and Language Evolution", fontsize=16)

        # Plot 1: Total lines over time
        axes[0].plot(
            df["date"], df["total_lines"], marker="o", linewidth=2, markersize=4
        )
        axes[0].set_title("Total Lines of Code Over Time")
        axes[0].set_ylabel("Lines of Code")
        axes[0].tick_params(axis="x", rotation=45)
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Language composition over time (stacked area)
        if languages:
            # Get top languages by final count
            final_counts = df.iloc[-1][[f"{lang}_lines" for lang in languages]]
            # Convert to numeric and handle any non-numeric values
            final_counts = pd.to_numeric(final_counts, errors="coerce").fillna(0)
            top_languages = final_counts.nlargest(6).index
            top_languages = [col.replace("_lines", "") for col in top_languages]

            language_data = df[[f"{lang}_lines" for lang in top_languages]]
            language_data.columns = top_languages
            # Ensure all data is numeric
            language_data = language_data.apply(pd.to_numeric, errors="coerce").fillna(
                0
            )

            # Sum all languages for percentage calculation
            total_sum = language_data.sum(axis=1)

            for dt, perc, tot in zip(df["date"], language_data['React'], total_sum):
                print(f"({dt.strftime('%Y-%m-%d')}, {perc}, {tot}),")

            axes[1].stackplot(
                df["date"],
                *[language_data[lang] for lang in top_languages],
                labels=top_languages,
                alpha=0.7,
            )
            axes[1].set_title("Language Composition Over Time")
            axes[1].set_ylabel("Lines of Code")
            axes[1].legend(loc="upper left", bbox_to_anchor=(1, 1))
            axes[1].tick_params(axis="x", rotation=45)

        # Plot 3: Number of files over time
        # axes[1, 0].plot(
        #     df["date"],
        #     df["total_files"],
        #     marker="s",
        #     color="green",
        #     linewidth=2,
        #     markersize=4,
        # )
        # axes[1, 0].set_title("Total Files Over Time")
        # axes[1, 0].set_ylabel("Number of Files")
        # axes[1, 0].tick_params(axis="x", rotation=45)
        # axes[1, 0].grid(True, alpha=0.3)

        # Plot 4: Language diversity
        # axes[1, 1].plot(
        #     df["date"],
        #     df["languages_count"],
        #     marker="^",
        #     color="red",
        #     linewidth=2,
        #     markersize=4,
        # )
        # axes[1, 1].set_title("Programming Language Diversity")
        # axes[1, 1].set_ylabel("Number of Languages")
        # axes[1, 1].tick_params(axis="x", rotation=45)
        # axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()

        # if save_path:
        plt.savefig('../assets/slides/stats/languages.png', dpi=300, bbox_inches="tight")

        plt.show()

    # def plot_language_pie_chart(self, df, save_path=None):
    #     """Create a pie chart of current language composition."""
    #     if df is None or df.empty:
    #         return

    #     # Get latest data
    #     latest = df.iloc[-1]
    #     language_cols = [
    #         col
    #         for col in df.columns
    #         if col.endswith("_lines") and not col.startswith("total_")
    #     ]

    #     language_data = {}
    #     for col in language_cols:
    #         lang = col.replace("_lines", "")
    #         lines = pd.to_numeric(latest[col], errors="coerce")
    #         if pd.notna(lines) and lines > 0:
    #             language_data[lang] = int(lines)

    #     if not language_data:
    #         print("No language data to plot")
    #         return

    #     # Sort and get top languages
    #     sorted_langs = sorted(language_data.items(), key=lambda x: x[1], reverse=True)

    #     # Group smaller languages as "Others"
    #     if len(sorted_langs) > 10:
    #         top_langs = sorted_langs[:9]
    #         others_total = sum(count for _, count in sorted_langs[9:])
    #         if others_total > 0:
    #             top_langs.append(("Others", others_total))
    #         sorted_langs = top_langs

    #     languages, lines = zip(*sorted_langs)

    #     plt.figure(figsize=(10, 8))
    #     colors = plt.cm.Set3(range(len(languages)))

    #     wedges, texts, autotexts = plt.pie(
    #         lines, labels=languages, autopct="%1.1f%%", colors=colors, startangle=90
    #     )

    #     plt.title("Current Language Composition (Lines of Code)", fontsize=14)

    #     # Add total info
    #     total_lines = sum(lines)
    #     plt.figtext(0.02, 0.02, f"Total Lines: {total_lines:,}", fontsize=10)

    #     if save_path:
    #         plt.savefig(save_path, dpi=300, bbox_inches="tight")
    #         print(f"Pie chart saved to {save_path}")

    #     plt.show()

    def generate_summary_report(self, df):
        """Generate a text summary of the analysis."""
        if df is None or df.empty:
            return "No data available for summary"

        latest = df.iloc[-1]
        earliest = df.iloc[0]

        # Calculate growth
        lines_growth = latest["total_lines"] - earliest["total_lines"]
        files_growth = latest["total_files"] - earliest["total_files"]

        # Get top languages
        language_cols = [
            col
            for col in df.columns
            if col.endswith("_lines") and not col.startswith("total_")
        ]
        current_langs = {}
        for col in language_cols:
            lang = col.replace("_lines", "")
            lines = pd.to_numeric(latest[col], errors="coerce")
            if pd.notna(lines) and lines > 0:
                current_langs[lang] = int(lines)

        top_languages = sorted(current_langs.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]

        # Time span
        time_span = (latest["date"] - earliest["date"]).days

        report = f"""
Repository Code Analysis Summary
================================

Analysis Period: {earliest["date"].strftime("%Y-%m-%d")} to {latest["date"].strftime("%Y-%m-%d")} ({time_span} days)
Commits Analyzed: {len(df)}

Current State (Latest Commit):
- Total Lines of Code: {latest["total_lines"]:,}
- Total Files: {latest["total_files"]:,}
- Programming Languages: {latest["languages_count"]}

Growth Over Time:
- Lines Added: {lines_growth:,} ({lines_growth / time_span * 365:.0f} lines/year average)
- Files Added: {files_growth:,}

Top 5 Languages by Lines of Code:
"""

        for i, (lang, lines) in enumerate(top_languages, 1):
            percentage = (lines / latest["total_lines"]) * 100
            report += f"{i}. {lang}: {lines:,} lines ({percentage:.1f}%)\n"

        return report


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Git repository LOC and language evolution"
    )
    parser.add_argument(
        "--repo",
        "-r",
        default=".",
        help="Path to git repository (default: current directory)",
    )
    parser.add_argument(
        "--commits",
        "-c",
        type=int,
        default=50,
        help="Number of commits to sample (default: 50)",
    )
    parser.add_argument("--output", "-o", help="Output CSV file path")
    parser.add_argument("--plot", help="Save evolution plot to file")
    parser.add_argument("--pie", help="Save language pie chart to file")
    parser.add_argument("--summary", action="store_true", help="Show summary report")

    args = parser.parse_args()

    # Check if the specified path is a git repository
    if not os.path.exists(os.path.join(args.repo, ".git")):
        print(f"Error: {args.repo} is not a git repository")
        sys.exit(1)

    # Initialize analyzer
    analyzer = GitLOCAnalyzer(args.repo)

    # Analyze repository
    print("Starting repository analysis...")
    df = analyzer.analyze_repository_evolution(args.commits)

    if df is None:
        print("Analysis failed")
        sys.exit(1)

    # Save to CSV if requested
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nData saved to {args.output}")

    # Create plots
    analyzer.plot_evolution(df, args.plot)
    # analyzer.plot_language_pie_chart(df, args.pie)

    # Show summary if requested
    if args.summary:
        print(analyzer.generate_summary_report(df))


if __name__ == "__main__":
    with load_theme("gruvbox_dark"):
        main()
