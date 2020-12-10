"""This module contains a function to validate JSON fields"""

import re
from .errors import ValidationError

# Validation Config structure
# {
#     'field': {
#         'required': True,
#         'type': int,
#         'pattern': re.compile(r'regex'),
#         'range': (0, 1),
#         'custom_validator': lambda val: True
#     }
# }


def validate_input(validation_config, data, check_required=True):
    """Validates `data` based on the validation config"""

    if type(data) != dict:
        raise ValidationError('data must be JSON')

    for key in validation_config:
        config = validation_config[key]

        if check_required and config.get('required', False) and key not in data:
            raise ValidationError(f'{key} is required')

        if key in data:
            value = data[key]

            if 'type' in config and type(value) != config['type']:
                typename = config['type'].__name__
                raise ValidationError(f'the type of {key} must be {typename})')

            if 'pattern' in config and not config['pattern'].match(value):
                raise ValidationError(f'incorrect format of {key}')

            if 'range' in config:
                start, end = config['range']
                if value < start or value > end:
                    raise ValidationError(
                        f'{key} must be between {start} and {end}')

            if 'custom_validator' in config and not config['custom_validator'](value):
                raise ValidationError(f'{key} is incorrect')
