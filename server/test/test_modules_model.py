import pytest

xfail = pytest.mark.xfail


from modules.model import Model
from modules.validations import is_required, is_email, has_min_length
from datetime import datetime


def encrypt_password(value):
    if value and not value.startswith('$2a$'):
        return '$2a$' + value


class User(Model):
    tablename = 'users'

    schema = dict(Model.schema.copy(), **{
        'name': {
            'validate': (is_required,),
            'unique': True,
        },
        'email': {
            'validate': (is_required, is_email),
            'unique': True,
            'access': ('private',),
        },
        'password': {
            'validate': (is_required, (has_min_length, 8)),
            'access': (),
            'bundle': encrypt_password
        }
    })


def test_table_class(db_conn, users_table):
    """
    Expect the model to have a table as a class.
    """
    assert User.tablename == 'users'
    assert User.table == users_table


def test_create_instance(db_conn, users_table):
    """
    Expect to create a model instance. Be able to pass in data too...
    """
    user = User({'name': 'Test'})
    assert user.data['name'] == 'Test'


def test_table_instance(db_conn, users_table):
    """
    Expect the model to have a table as an instance.
    """
    user = User()
    assert user.tablename == 'users'
    assert user.table == users_table


def test_get_item(db_conn, users_table):
    """
    Expect to get an item from the model.
    """
    user = User()
    user.data['name'] = 'Test'
    assert user['name'] == 'Test'


def test_set_item(db_conn, users_table):
    """
    Expect to set an item in the model.
    """
    user = User()
    user['name'] = 'Test'
    assert user.data['name'] == 'Test'


def test_del_item(db_conn, users_table):
    """
    Expect to remove an item in the model.
    """
    user = User()
    user['name'] = 'Test'
    assert user.data['name'] == 'Test'
    del user['name']
    assert 'name' not in user.data


def test_has_item(db_conn, users_table):
    """
    Expect to test if model has an item.
    """
    user = User()
    assert 'name' not in user
    user['name'] = 'Test'
    assert 'name' in user


def test_get_id(db_conn, users_table):
    """
    Expect to be able to retrieve a model by ID.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(db_conn, id='abcdefgh12345678')
    assert user['name'] == 'test'


def test_get_params(db_conn, users_table):
    """
    Expect a model to retrieve by params.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(db_conn, name='test', email='test@example.com')
    assert user['id'] == 'abcdefgh12345678'


def test_get_none(db_conn, users_table):
    """
    Expect a no model when `get` with no match.
    """
    users_table.insert({
        'id': 'abcdefgh12345678',
        'name': 'test',
        'email': 'test@example.com',
    }).run(db_conn)
    user = User.get(db_conn, id='87654321hgfedcba')
    assert user is None


def test_list(db_conn, users_table):
    """
    Expect to get a list of models.
    """
    users_table.insert([
        {
            'id': '1',
            'name': 'test1',
            'email': 'test1@example.com',
        },
        {
            'id': '2',
            'name': 'test2',
            'email': 'test2@example.com',
        },
        {
            'id': '3',
            'name': 'test3',
            'email': 'test3@example.com',
        },
    ]).run(db_conn)
    users = User.list(db_conn)
    assert len(users) == 3
    assert isinstance(users[0], User)
    assert users[2]['id'] in ('1', '2', '3')


def test_list_params(db_conn, users_table):
    """
    Expect to get a list of models by params.
    """
    users_table.insert([
        {
            'id': '1',
            'name': 'test1',
            'email': 'test1@example.com',
        },
        {
            'id': '2',
            'name': 'test2',
            'email': 'test2@example.com',
        },
        {
            'id': '3',
            'name': 'test3',
            'email': 'test3@example.com',
        },
    ]).run(db_conn)
    users = User.list(db_conn, id='1', name='test1')
    assert len(users) == 1
    assert users[0]['email'] == 'test1@example.com'


def test_list_none(db_conn, users_table):
    """
    Expect to get an empty list of models when none.
    """
    users = User.list(db_conn)
    assert len(users) == 0


def test_generate_id(db_conn, users_table):
    """
    Expect to automatically generate an ID.
    """
    user = User({'password': 'abcd1234'})
    d = user.bundle()
    assert isinstance(d['id'], str)
    assert len(d['id']) == 24


def test_validate(db_conn, users_table):
    """
    Expect to validate a model.
    """

    user = User({
        'name': 'Test',
        'email': 'test@example.com',
        'password': 'abcd'
    })
    errors = user.validate(db_conn)
    assert isinstance(errors, list)
    assert errors[0]['name'] == 'password'
    assert errors[0]['message']


def test_enforce_strict(db_conn, users_table):
    """
    Expect to enforce strict mode.
    """
    user = User({'extra': True})
    assert user.data['extra']
    user.enforce_strict_mode()
    assert 'extra' not in user.data


@xfail
def test_enforce_strict_embed():
    """
    Expect
    """

    assert False


@xfail
def test_enforce_strict_embed_many():
    """
    Expect
    """

    assert False


def test_validate_fields(db_conn, users_table):
    """
    Expect to validate a model's fields.
    """

    user = User({
        'name': 'Test',
        'email': 'test@example.com',
        'password': 'abcd'
    })
    errors = user.validate_fields()
    assert isinstance(errors, list)
    assert errors[0]['name'] == 'password'
    assert errors[0]['message']


@xfail
def test_validate_fields_embed():
    """
    Expect
    """

    assert False


@xfail
def test_validate_fields_embed_many():
    """
    Expect
    """

    assert False


def test_bundle(db_conn, users_table):
    """
    Expect to...
    """
    user = User({
        'name': 'Test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    data = user.bundle()
    assert data['password'].startswith('$2a$')
    assert user['password'] == 'abcd1234'


@xfail
def test_bundle_embed():
    """
    Expect
    """

    assert False


@xfail
def test_bundle_embed_many():
    """
    Expect
    """

    assert False


def test_default(db_conn, users_table):
    """
    Expect to set a default value for fields.
    """
    user = User()
    assert isinstance(user['id'], str)


@xfail
def test_default_embed():
    """
    Expect
    """

    assert False


@xfail
def test_default_embed_many():
    """
    Expect
    """

    assert False


def test_deliver(db_conn, users_table):
    """
    Expect to...
    """
    user = User({
        'name': 'Test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    data = user.deliver()
    assert 'email' not in data
    assert 'password' not in data
    data = user.deliver(access='private')
    assert 'email' in data
    assert 'password' not in data


@xfail
def test_deliver_embed():
    """
    Expect
    """

    assert False


@xfail
def test_deliver_embed_many():
    """
    Expect
    """

    assert False


def test_insert(db_conn, users_table):
    """
    Expect to create a new model instance.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert user['id']
    assert user['name'] == 'test'
    assert record['email'] == 'test@example.com'


def test_insert_fail(db_conn, users_table):
    """
    Expect to error on failed create model.
    """
    assert len(list(users_table.run(db_conn))) == 0
    user, errors = User.insert(db_conn, {
        'email': 'test@example.com'
    })
    assert user['name'] is None
    assert user['password'] is None
    assert isinstance(user, User)
    assert isinstance(errors, (list, tuple))
    assert len(errors) == 2
    assert errors[0]['message']


def test_update(db_conn, users_table):
    """
    Expect to update a model instance.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user, errors = user.update(db_conn, {
        'email': 'open@example.com'
    })
    assert len(errors) == 0
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert user['email'] == 'open@example.com'
    assert record['email'] == 'open@example.com'


def test_update_fail(db_conn, users_table):
    """
    Expect to error on failed update model instance.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user, errors = user.update(db_conn, {
        'email': 'open'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert isinstance(user, User)
    assert isinstance(errors, (list, tuple))
    assert user['email'] == 'open'
    assert record['email'] == 'test@example.com'


def test_save(db_conn, users_table):
    """
    Expect a model to be able to save at any time.
    """
    user = User({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    user, errors = user.save(db_conn)
    assert len(errors) == 0
    records = list(users_table.filter({'name': 'test'}).run(db_conn))
    assert len(records) == 1


def test_delete(db_conn, users_table):
    """
    Expect to delete a model.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    user.delete(db_conn)
    records = list(users_table.filter({'name': 'test'}).run(db_conn))
    assert len(records) == 0


def test_id_keep(db_conn, users_table):
    """
    Expect a model to maintain an ID.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    id = user['id']
    user.update(db_conn, {
        'name': 'other'
    })
    assert user['id'] == id


def test_created(db_conn, users_table):
    """
    Expect a model to add created time.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert record['created'] == user['created']


def test_transform(db_conn, users_table):
    """
    Expect a model to call transform before going into DB.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) == 0
    assert user['password'].startswith('$2a$')


def test_modified(db_conn, users_table):
    """
    Expect to sync fields with database.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    user, errors = user.update(db_conn, {
        'email': 'other@example.com'
    })
    record = list(users_table.filter({'name': 'test'}).run(db_conn))[0]
    assert isinstance(user['modified'], datetime)
    assert record['modified'] == user['modified']
    assert user['created'] != user['modified']


def test_unique(db_conn, users_table):
    """
    Expect a validation to test uniqueness.
    """
    user, errors = User.insert(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    })
    user2, errors2 = User.insert(db_conn, {
        'name': 'test',
        'email': 'coin@example.com',
        'password': '1234abcd',
    })
    assert len(errors) == 0
    assert len(errors2) == 1
    assert errors2[0]['name'] == 'name'


# TODO-3 test_unique_embed
# TODO-3 test_unique_embed_many
