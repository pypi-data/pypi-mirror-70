"""Custom validators for :mod:`attrs`."""

from attr.validators import instance_of


def str_of_length(length):
    """Validate that the value is a string of the given length."""

    def validator(instance, attribute, value):
        instance_of(str)(instance, attribute, value)
        if len(value) != length:
            raise ValueError(
                '{0.name} must be exactly {1} chars, got {2!r}'.format(
                    attribute, length, value
                )
            )

    return validator


def str_of_max_length(length):
    """Validate that the value is a string with a max length."""

    def validator(instance, attribute, value):
        instance_of(str)(instance, attribute, value)
        if len(value) > length:
            raise ValueError(
                '{0.name} must be at most {1} chars, '
                'got {2!r} which is {3} chars'.format(
                    attribute, length, value, len(value)
                )
            )

    return validator
