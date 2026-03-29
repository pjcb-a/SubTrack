from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.subscription_routes import subscription_bp
from routes.user_routes import user_bp
from utils.seed_data import seed_default_categories


# FOR CREATING AND CONFIGURING THE FLASK APPLICATION
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # FOR CONNECTING FLASK TO THE DATABASE
    db.init_app(app)

    # FOR ALLOWING THE VUE FRONTEND TO CALL THIS API
    CORS(
        app,
        supports_credentials=True,
        origins=app.config["CORS_ORIGINS"],
    )

    # FOR REGISTERING THE API ROUTE FILES
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(subscription_bp)

    # FOR RETURNING A JSON RESPONSE WHEN A ROUTE DOES NOT EXIST
    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found"}), 404

    # FOR RETURNING A JSON RESPONSE WHEN THE HTTP METHOD IS WRONG
    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"error": "Method not allowed"}), 405

    # FOR RETURNING A JSON RESPONSE FOR SERVER ERRORS
    @app.errorhandler(500)
    def internal_server_error(_error):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    # FOR CREATING TABLES AND SEEDING DEFAULT CATEGORIES
    with app.app_context():
        db.create_all()
        seed_default_categories()

    return app


app = create_app()


# FOR STARTING THE BACKEND LOCALLY
if __name__ == "__main__":
    app.run(debug=True)
