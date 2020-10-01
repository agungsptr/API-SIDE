from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_raw_jwt

import models as md
import resources as res

url_prefix = '/api/v1'

# Init Flask App
app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("config.Production")
else:
    app.config.from_object("config.Development")


# Error to json
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(403)
def server_forbidden(e):
    return jsonify(error=str(e)), 403


@app.errorhandler(410)
def gone(e):
    return jsonify(error=str(e)), 410


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


# Register Blueprints
app.register_blueprint(res.user_api, url_prefix=url_prefix)
app.register_blueprint(res.kartu_keluarga_api, url_prefix=url_prefix)
app.register_blueprint(res.penduduk_api, url_prefix=url_prefix)
app.register_blueprint(res.prog_desa_api, url_prefix=url_prefix)
app.register_blueprint(res.inf_unggulan_api, url_prefix=url_prefix)
app.register_blueprint(res.inf_sarana_api, url_prefix=url_prefix)
app.register_blueprint(res.inf_dusun_api, url_prefix=url_prefix)
app.register_blueprint(res.inf_administrasi_api, url_prefix=url_prefix)
app.register_blueprint(res.inf_penduduk_api, url_prefix=url_prefix)
app.register_blueprint(res.inf_perangkat_api, url_prefix=url_prefix)
app.register_blueprint(res.inf_umum_api, url_prefix=url_prefix)
app.register_blueprint(res.geo_api, url_prefix=url_prefix)

# Set blacklist token for loging out
jwt = JWTManager(app)
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('{}/user/logout'.format(url_prefix))
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return 'loged out'


if __name__ == '__main__':
    md.init()
    app.run()
