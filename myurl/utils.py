from littleurl.settings import SECRET_KEY


def get_shortend_url(longid):
    secret_key = SECRET_KEY
    littleurl = ""
    while longid > 0:
        littleurl += secret_key[longid % 62]
        longid //= 62
    return littleurl
