import requests
from crewai.tools import tool

@tool("GitHub Health Check Tool")
def github_health_check_tool(query: str) -> str:
    """
    Searches GitHub REST API for open source repositories and checks project health:
    - Stars count (popularity)
    - Last updated date (abandonware check)
    - Open source license (MIT/Apache vs GPL compliance)
    """
    try:
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=4"
        headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "TSI-Idea-Validator"}
        
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code != 200:
            return f"GitHub API query failed with status {res.status_code}."
        
        data = res.json()
        items = data.get("items", [])
        if not items:
            return f"No GitHub repositories found for '{query}'."

        formatted_repos = []
        for repo in items:
            name = repo.get("full_name")
            html_url = repo.get("html_url")
            stars = repo.get("stargazers_count", 0)
            pushed_at = repo.get("pushed_at", "Unknown")[:10]
            license_info = repo.get("license") or {}
            license_name = license_info.get("spdx_id") or "No License"
            description = repo.get("description") or "No description."

            # Determine health status
            abandoned_warning = ""
            if pushed_at.startswith("2021") or pushed_at.startswith("2022") or pushed_at.startswith("2023"):
                abandoned_warning = "⚠️ [WARNING: Inactive/Abandoned project - No recent commits]"

            formatted_repos.append(
                f"### Repo: {name}\n"
                f"- URL: {html_url}\n"
                f"- Stars ⭐: {stars}\n"
                f"- Last Commit Date 📅: {pushed_at} {abandoned_warning}\n"
                f"- License 📜: {license_name}\n"
                f"- Description: {description}\n"
            )

        return "\n---\n".join(formatted_repos)

    except Exception as e:
        return f"Error executing GitHub health check for '{query}': {str(e)}"
