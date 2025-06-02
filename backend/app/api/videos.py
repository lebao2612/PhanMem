from flask import Blueprint, jsonify, request
from app.models.videos import get_all_videos, get_videos_by_tag

video_bp = Blueprint('video', __name__, url_prefix='/api')

@video_bp.route("/videos", methods=["GET"])
def list_videos():
    tag = request.args.get("tag")
    
    if tag:
        videos = get_videos_by_tag(tag)
    else:
        videos = get_all_videos()

    for video in videos:
        video["_id"] = str(video["_id"])
    return jsonify(videos)
