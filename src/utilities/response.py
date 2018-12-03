"""Module for parsing custom responses"""


def success(message, data=None, code=200):
    """
    Return custom reusable success message

    Parameters:
        message(string): message to return to the user
        data(dict): response data
        code(number): status code of the response
    Returns:
        response(tuple): custom success REST response
    """
    response = {'status': 'success', 'data': data, 'message': message}
    data = data or response.pop('data')
    return response, code
