import logging
from flask import jsonify
from app.exceptions import HandledException

# Cấu hình logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(HandledException)
    def handle_service_error(error):
        return jsonify({
            "error": error.message,
            "code": error.code
        }), error.code

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "error": "Tài nguyên không tồn tại hoặc đường dẫn sai",
            "code": 404
        }), 404

    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({
            "error": "Phương thức HTTP không được hỗ trợ",
            "code": 405
        }), 405

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        return jsonify({
            "error": "Lỗi hệ thống, vui lòng thử lại sau",
            "code": 500
        }), 500