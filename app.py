import datetime

from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_raw_jwt

import models as md
import resources as res

url_prefix = '/api/v1'

app = Flask(__name__)
app.register_blueprint(res.user_api, url_prefix=url_prefix)

# JWT CONFIG
app.config['SECRET_KEY'] = "7Bs6vcBuoJQ97XnKNUbO2C4wvdwGPIzj14JQE3k2fdDdt0ihTJcbA" \
                           "PuDtyxmzbL_SIfaStBM3lUyFN0SJxdGwJ4hoZd-UjVsDWmmtU4Yot" \
                           "uSg_hMUz5DRJKtDiRLo0LQghjwQpqveot9w8G5as7JR7ppvVdZfcM" \
                           "wYYAtgDltJa8"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECK'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

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
    app.run(debug=True)
