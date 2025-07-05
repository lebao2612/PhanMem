class YoutubeVideo:
    def __init__(self, raw: dict):
        self.raw = raw or {}

    def to_metadata(self) -> dict:
        snippet: dict = self.raw.get("snippet", {})
        stats: dict = self.raw.get("statistics", {})

        return {
            "id": self.raw.get("id"),
            "title": snippet.get("title"),
            "tags": snippet.get("tags", []),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
        }