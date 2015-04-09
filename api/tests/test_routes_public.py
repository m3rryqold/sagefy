import routes.public


def test_welcome():
    """
    Ensure the API returns a welcome message.
    """

    code, response = routes.public.index_route({})
    assert code == 200
    assert 'Welcome' in response['message']
