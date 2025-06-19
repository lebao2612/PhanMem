from flask import Blueprint, request, jsonify, g
from app.services.generator_service import GeneratorService
from app.api.middlewares import token_required

generator_bp = Blueprint("generators", __name__, url_prefix="/api/generators")

@generator_bp.route("/topic/suggestions", methods=["GET"])
@token_required
def get_suggestions():
    query = request.args.get("query", "")
    suggestions = GeneratorService.get_suggestions(query)
    return jsonify(suggestions), 200

@generator_bp.route("/topic/trending", methods=["GET"])
@token_required
def get_trending():
    trending = GeneratorService.get_trending()
    return jsonify(trending), 200

@generator_bp.route("/script", methods=["POST"])
@token_required
def generate_script():
    data = request.get_json()
    topic = data.get("topic")
    script = GeneratorService.generate_script_from_topic(topic)
    return jsonify({"topic": topic, "script": script}), 200

@generator_bp.route("/voice", methods=["POST"])
@token_required
def generate_voice():
    data = request.get_json()
    video_id = data.get("video_id")
    video = GeneratorService.generate_voice(video_id, str(g.current_user.id))
    return jsonify(video.to_dict()), 200

@generator_bp.route("/video", methods=["POST"])
@token_required
def generate_video():
    data = request.get_json()
    video_id = data.get("video_id")
    video = GeneratorService.generate_video(video_id, str(g.current_user.id))
    return jsonify(video.to_dict()), 200