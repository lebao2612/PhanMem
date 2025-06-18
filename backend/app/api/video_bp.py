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

@video_bp.route("/<video_id>", methods=["PUT"])
@token_required
def update_video(video_id):
    data = request.get_json()
    video = VideoService.update_video(video_id, data)
    return jsonify(video.to_dict()), 200

@video_bp.route("/<video_id>", methods=["DELETE"])
@token_required
def delete_video(video_id):
    VideoService.delete_video(video_id)
    return jsonify({"message": "Xóa video thành công"}), 200

@video_bp.route("/<video_id>/view", methods=["POST"])
def increment_view(video_id):
    VideoService.increment_view(video_id)
    return jsonify({"message": "Đã tăng lượt xem"}), 200

@video_bp.route("/<video_id>/like", methods=["POST"])
def increment_like(video_id):
    VideoService.increment_like(video_id)
    return jsonify({"message": "Đã tăng lượt thích"}), 200