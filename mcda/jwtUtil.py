import jwt
import mcda.settings as settings
from base64 import b64decode

class JwtUtil:
    @staticmethod
    def get_user(token):
        decoded_data = jwt.decode(token,
                                  settings.JWT_KEY,
                                  algorithms=[settings.JWT_ALG])
        return decoded_data['user_id']
