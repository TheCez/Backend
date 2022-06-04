from typing import List
from datetime import datetime
from app.models import Episode
from dateutil.parser import isoparse


class Season:
    def __init__(self, file_metadata, media_metadata):
        # File Info
        self.id: str = file_metadata.get("id") or ""
        self.file_name: str = file_metadata.get("name") or ""
        self.path: str = file_metadata.get("path") or ""
        self.parent: dict = file_metadata.get("parent") or {}
        self.modified_time: datetime = isoparse(
            file_metadata.get("modified_time", "1900-03-27T00:00:00.000+00:00")
        )

        # Media Info
        self.tmdb_id: int = media_metadata.get("id") or 0
        self.name: str = media_metadata.get("name") or ""
        self.overview: str = media_metadata.get("overview") or ""
        air_date: str = media_metadata.get("air_date") or "1900-03-27"
        self.air_date: datetime = datetime.strptime(air_date, "%Y-%m-%d")
        self.episode_count: int = media_metadata.get("episode_count") or 0
        self.season_number: int = media_metadata.get("season_number") or 0

        # Media Resources
        self.poster_path: str = media_metadata.get("poster_path") or ""

        # Episodes
        index: int = len(file_metadata.get("episodes", []))
        self.episodes: List[Episode] = []
        for episode in file_metadata.get("episodes", []):
            self.episodes.append(Episode(episode, media_metadata, index).__dict__)
            index -= 1