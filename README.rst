Python kChat Driver (APIv4)
================================

Installation
------------

.. inclusion-marker-start-install

``pip install kchatdriver``

.. inclusion-marker-end-install

Documentation
-------------
Documentation can be found at https://vaelor.github.io/python-mattermost-driver/ .

Usage
-----

.. inclusion-marker-start-usage

.. code:: python

    from kchatdriver import Driver

    foo = Driver({
        """
        Required options

        """
        'url': 'myteam.kchat.infomaniak.com',
        'token': 'YourBotAccessToken',

        Be careful. This SHOULD NOT be active in production, because this logs a lot!
        Even the password for your account when doing driver.login()!
        """
        'debug': False
        """
    })

    """
    Most of the requests need you to be logged in, so calling login()
    should be the first thing you do after you created your Driver instance.
    login() returns the raw response.
    If using a personal access token, you still need to run login().
    In this case, does not make a login request, but a `get_user('me')`
    and sets everything up in the client.
    """
    foo.login()
    foo.users.get_user_by_username('another.name')

    """
    If the api request needs additional parameters
    you can pass them to the function in the following way:
    - Path parameters are always simple parameters you pass to the function
    """
    foo.users.get_user(user_id='me')

    # - Query parameters are always passed by passing a `params` dict to the function
    foo.teams.get_teams(params={...})

    # - Request Bodies are always passed by passing an `options` dict or array to the function
    foo.channels.create_channel(options={...})

    # See the mattermost api documentation to see which parameters you need to pass.
    foo.channels.create_channel(options={
        'team_id': 'some_team_id',
        'name': 'awesome-channel',
        'display_name': 'awesome channel',
        'type': 'O'
    })

    """
    If you want to make a websocket connection to the kChat server
    you can call the init_websocket method, passing an event_handler.
    Every Websocket event send by kChat will be send to that event_handler.
    See the API documentation for which events are available.
    """
    foo.init_websocket(event_handler)

    # Use `disconnect()` to disconnect the websocket
    foo.disconnect()

    # To upload a file you will need to pass a `files` dictionary
    channel_id = foo.channels.get_channel_by_name_and_team_name('team', 'channel')['id']
    file_id = foo.files.upload_file(
        channel_id=channel_id,
        files={'files': (filename, open(filename, 'rb'))}
    )['file_infos'][0]['id']


    # track the file id and pass it in `create_post` options, to attach the file
    foo.posts.create_post(options={
        'channel_id': channel_id,
        'message': 'This is the important file',
        'file_ids': [file_id]})

    # If needed, you can make custom requests by calling `make_request`
    foo.client.make_request('post', '/endpoint', options=None, params=None, data=None, files=None, basepath=None)

    # If you want to call a webhook/execute it use the `call_webhook` method.
    # This method does not exist on the mattermost api AFAIK, I added it for ease of use.
    foo.webhooks.call_webhook('myHookId', options) # Options are optional


.. inclusion-marker-end-usage
