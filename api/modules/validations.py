import re
from modules.content import get as _


def is_required(value):
    """
    Ensure the value is present.
    """

    if value is None:
        return _('error', 'required')


def is_boolean(value):
    """
    Ensure the given value is a boolean.
    """

    if value is None:
        return

    if not isinstance(value, bool):
        return _('error', 'boolean')


def is_string(value):
    """
    Ensure the given value is a string.
    """

    if value is None:
        return

    if not isinstance(value, str):
        return _('error', 'string')


def is_number(value):
    """
    Ensure the given value is a number.
    """

    if value is None:
        return

    if not isinstance(value, (int, long, float, complex)):
        return _('error', 'number')


def is_language(value):
    """
    Entity must be ISO 639-1 code.
    """

    if value is None:
        return

    if not (isinstance(value, basestring) or len(value) != 2):
        return _('error', 'language')


def is_list(value):
    """
    Ensure the given value is a list.
    """

    if value is None:
        return

    if not isinstance(value, list):
        return _('error', 'list')


def is_email(value):
    """
    Ensure the given value is formatted as an email.
    """

    if value is None:
        return

    if not re.match(r'\S+@\S+\.\S+', value):
        return _('error', 'email')


def has_min_length(value, ln):
    """
    Ensure the given value is a minimum length.
    """
    if value is None:
        return

    if not value or len(value) < ln:
        return _('error', 'minlength').replace('{length}', str(ln))


def is_one_of(value, *options):
    """
    Ensure the value is within an enumerated set.
    """
    if value is None:
        return

    if value not in options:
        str_options = [str(o) for o in options]
        return (_('error', 'options')
                .replace('{options}', ', '.join(str_options)))


def is_entity_dict(value):
    """
    Ensure the value is a dict refering to an entity.
    """

    if value is None:
        return

    if not isinstance(value, dict):
        return _('error', 'entity_id')

    if 'id' not in value or not isinstance(value['id'], str):
        return _('error', 'entity_id')

    if 'kind' not in value or value['kind'] not in ('card', 'unit', 'set'):
        return _('error', 'entity_kind')


def is_entity_list_dict(value):
    """
    Ensure the value is a list of dicts refering to entities.
    """

    if value is None:
        return

    errors = []

    for i, v in enumerate(value):
        error = is_entity_dict(v)
        if error:
            errors.append({
                'name': i,
                'message': error,
            })

    if len(errors):
        return errors


def is_list_of_strings(value):
    """
    Ensure the number is a list of strings.
    """

    if value is None:
        return

    if not isinstance(value, list):
        return _('error', 'list')

    for v in value:
        if not isinstance(v, basestring):
            return _('error', 'string')
