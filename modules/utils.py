from typing import List

def get_posts_for_case(db, case_id: str, limit: int = None) -> List[dict]:
    """Return list of posts for a given case_id."""
    query = {'case_id': case_id}
    cursor = db.posts.find(query)
    if limit:
        cursor = cursor.limit(limit)
    return list(cursor)
