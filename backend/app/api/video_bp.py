from flask import Blueprint, request, jsonify, g
from app.services import VideoService
from .middlewares import token_required

video_bp = Blueprint("video", __name__, url_prefix="/api/videos")

@video_bp.route("/", methods=["GET"])
@token_required
def list_videos():
    creator_id = str(g.current_user.id)
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 20))
    videos = VideoService.list_videos_by_creator(creator_id, skip, limit)
    return jsonify([v.to_dict() for v in videos]), 200

@video_bp.route("/<video_id>", methods=["GET"])
@token_required
def get_video(video_id):
    video = VideoService.get_video_by_id(video_id)
    return jsonify(video.to_dict()), 200

@video_bp.route("/", methods=["POST"])
@token_required
def create_video():
    data = request.get_json()
    title = data.get("title")
    topic = data.get("topic")
    script = data.get("script")
    tags = data.get("tags", [])
    video = VideoService.create_video(title, topic, script, g.current_user, tags)
    return jsonify(video.to_dict()), 201

@video_bp.route("/<video_id>", methods=["PATCH"])
@token_required
def update_video(video_id):
    data = request.get_json()
    video = VideoService.update_video(video_id, data)
    return jsonify(video.to_dict()), 200

@video_bp.route("/<video_id>/view", methods=["PATCH"])
@token_required
def update_view(video_id):
    data = request.get_json()
    views = data.get("views")
    if views is None:
        return jsonify({"error": "Thiếu số views"}), 400
    VideoService.update_views(video_id, views)
    return jsonify({"message": "Đã cập nhật lượt xem"}), 200

@video_bp.route("/<video_id>/like", methods=["PATCH"])
@token_required
def update_like(video_id):
    data = request.get_json()
    likes = data.get("likes")
    if likes is None:
        return jsonify({"error": "Thiếu số likes"}), 400
    VideoService.update_likes(video_id, likes)
    return jsonify({"message": "Đã cập nhật lượt thích"}), 200

@video_bp.route("/<video_id>", methods=["DELETE"])
@token_required
def delete_video(video_id):
    VideoService.delete_video(video_id)
    return jsonify({"message": "Xóa video thành công"}), 200