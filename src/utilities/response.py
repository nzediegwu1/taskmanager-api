"""Module for parsing custom responses"""


def success(message, data=None, code=200):
    """Return custom success message

    Args:
        message(string): message to return to the user
        data(dict): response data
        code(number): status code of the response
    Returns:
        tuple: custom success REST response
    """
    response = {'status': 'success', 'data': data, 'message': message}
    return {key: value for key, value in response.items() if value}, code
