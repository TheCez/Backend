import time
from fastapi import APIRouter
from typing import Any, Dict, Optional


router = APIRouter(
    prefix="/browse",
    tags=["internals"],
)

unwanted_keys = {
    "_id": 0,
    "cast": 0,
    "crew": 0,
    "seasons": 0,
    "file_name": 0,
    "subtitles": 0,
    "external_ids": 0,
    "videos": 0,
    "reviews": 0,
    "collection": 0,
    "homepage": 0,
    "last_episode_to_air": 0,
    "next_episode_to_air": 0,
    "path": 0,
    "parent": 0,
    "revenue": 0,
    "tagline": 0,
    "imdb_id": 0,
}


@router.get("/{rclone_index}/{page}", response_model=Dict[str, Any])
def browse(
    rclone_index: int,
    page: int = 0,
    limit: Optional[int] = 20,
    sort: Optional[str] = "title:1",
    media_type: Optional[str] = "movies",
) -> Dict[str, Any]:
    start = time.perf_counter()
    from main import mongo, rclone

    sort_split = sort.split(":")
    sort_dict = {sort_split[0]: int(sort_split[1])}
    if rclone_index == -1:
        category_cols = []
        for category in rclone:
            if media_type == category.data.get("type", "movies"):
                category_cols.append(mongo.metadata[category.id])
    else:
        category_id = rclone[rclone_index].id
        category_cols = [mongo.metadata[category_id]]
    browse_result = []
    for category_col in category_cols:
        result = list(
            category_col.aggregate(
                [
                    {"$sort": sort_dict},
                    {"$skip": page * 20},
                    {"$limit": limit},
                    {"$project": unwanted_keys},
                ]
            )
        )
        browse_result.extend(result)

    end = time.perf_counter()
    return {
        "ok": True,
        "message": "success",
        "result": result,
        "time_taken": end - start,
    }