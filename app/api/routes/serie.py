from typing import Any, Dict
from fastapi import APIRouter
from time import perf_counter


router = APIRouter(
    prefix="/movie",
    tags=["internals"],
)


@router.get("/{id}", response_model=Dict[str, Any], status_code=200)
def movie(id: int) -> Dict[str, Any]:
    start = perf_counter()
    from main import mongo

    results = {}
    for category in mongo.config["categories"]:
        if category["type"] == "movies":
            result = mongo.movies_col.find({"tmdb_id": id}, {"_id": 0})
            for item in result:
                if results == {}:
                    results = item
                    results["id"] = [results["id"]]
                    results["file_name"] = [results["file_name"]]
                    results["modified_time"] = [results["modified_time"]]
                else:
                    results["id"].append(item["id"])
                    results["file_name"].append(item["file_name"])
                    results["modified_time"].append(item["modified_time"])

    return {
        "ok": True,
        "message": "success",
        "results": results,
        "time_taken": perf_counter() - start,
    }
