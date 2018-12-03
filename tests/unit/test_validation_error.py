from src.utilities.exceptions.ValidationError import ValidationError


class TestValidationError:
    """Class for ValidationError handler tests"""

    def test_to_dict_will_return_dict(self):
        """ Test that to_dict method return expected dict containing message passed
        """
        message = 'something went wrong'
        val_error = ValidationError(message)
        assert val_error.to_dict() == {'status': 'error', 'message': message}
