from sinaapi.fetch.shared import error_code


def is_error(resp):
    return u"error_code" in resp


def check_error(resp):

    error_code_key = u"error_code"
    error_key = u"error"

    code = resp[error_code_key]

    if error_key in resp:
        res = resp[error_key]
    else:
        if code not in error_code:
            res = "unknown error!"
        else:
            res = error_code[code]


    return code, res