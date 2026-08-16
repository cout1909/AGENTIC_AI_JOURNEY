import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GitHub Server")


@mcp.tool()
def get_repo_info(owner: str, repo: str) -> dict:
    """Get basic information about a GitHub repository."""

    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Repository not found"}

    data = response.json()

    return {
        "name": data["name"],
        "description": data["description"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "language": data["language"],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")