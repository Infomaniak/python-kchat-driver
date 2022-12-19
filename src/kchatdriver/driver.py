import asyncio
import logging
import warnings

from .client import Client
from .websocket import Websocket
from .endpoints.channels import Channels
from .endpoints.commands import Commands
from .endpoints.files import Files
from .endpoints.posts import Posts
from .endpoints.preferences import Preferences
from .endpoints.reactions import Reactions
from .endpoints.system import System
from .endpoints.teams import Teams
from .endpoints.users import Users
from .endpoints.webhooks import Webhooks
from .endpoints.emoji import Emoji
from .endpoints.roles import Roles
from .endpoints.status import Status
from .endpoints.bots import Bots
from .endpoints.integration_actions import IntegrationActions

log = logging.getLogger("kchatdriver.api")
log.setLevel(logging.INFO)


class Driver:
    """
    Contains the client, api and provides you with functions for
    login, logout and initializing a websocket connection.
    """

    default_options = {
        "scheme": "https",
        "url": "kchat.infomaniak.com",
        "websocket_url": "websocket.kchat.infomaniak.com",
        "port": 443,
        "basepath": "/api/v4",
        "verify": True,
        "timeout": 30,
        "request_timeout": None,
        "token": None,
        "auth": None,
        "keepalive": False,
        "keepalive_delay": 5,
        "websocket_kw_args": None,
        "debug": False,
    }
    """
	Required options
		- url

	token (https://docs.mattermost.com/developer/personal-access-tokens.html)
	"""

    def __init__(self, options=None, client_cls=Client):
        """
        :param options: A dict with the values from `default_options`
        :type options: dict
        """
        if options is None:
            options = self.default_options
        self.options = self.default_options.copy()
        self.options.update(options)
        self.driver = self.options
        if self.options["debug"]:
            log.setLevel(logging.DEBUG)
            log.warning(
                "Careful!!\nSetting debug to True, will reveal your password in the log output if you do driver.login()!\nThis is NOT for production!"
            )  # pylint: disable=line-too-long
        self.client = client_cls(self.options)
        self._api = {
            "users": Users(self.client),
            "teams": Teams(self.client),
            "channels": Channels(self.client),
            "posts": Posts(self.client),
            "files": Files(self.client),
            "preferences": Preferences(self.client),
            "status": Status(self.client),
            "emoji": Emoji(self.client),
            "reactions": Reactions(self.client),
            "system": System(self.client),
            "webhooks": Webhooks(self.client),
            "commands": Commands(self.client),
            "roles": Roles(self.client),
            "bots": Bots(self.client),
            "integration_actions": IntegrationActions(self.client),
        }
        self.websocket = None

    def init_websocket(self, event_handler, team_id: str, team_user_id: str, websocket_cls=Websocket):
        """
        Will initialize the websocket connection to the kChat server.

        This should be run after login(), because the websocket needs to make
        an authentification.

        See https://api.mattermost.com/v4/#tag/WebSocket for which
        websocket events kChat sends.

        Example of a really simple event_handler function

        .. code:: python

                async def my_event_handler(message):
                        print(message)


        :param event_handler: The function to handle the websocket events. Takes one argument.
        :type event_handler: Function(message)
        :return: The event loop
        """
        self.websocket = websocket_cls(self.options, self.client.token, team_id, team_user_id)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.websocket.connect(event_handler))
        return loop

    def disconnect(self):
        """Disconnects the driver from the server, stopping the websocket event loop."""
        self.websocket.disconnect()

    def login(self):
        self.client.token = self.options["token"]
        result = self.users.get_user("me")

        log.debug(result)

        if "id" in result:
            self.client.userid = result["id"]
        if "username" in result:
            self.client.username = result["username"]

        return result

    def logout(self):
        """
        Log the user out.

        :return: The JSON response from the server
        """
        result = self.users.logout_user()
        self.client.token = ""
        self.client.userid = ""
        self.client.username = ""
        self.client.cookies = None
        return result

    @property
    def api(self):
        """
        .. deprecated:: 4.0.2

        Use the endpoints directly instead.

        :return: dictionary containing the endpoints
        :rtype: dict
        """
        warnings.warn("Deprecated for 5.0.0. Use the endpoints directly instead.", DeprecationWarning)
        return self._api

    @property
    def users(self):
        """
        Api endpoint for users

        :return: Instance of :class:`~endpoints.users.Users`
        """
        return Users(self.client)

    @property
    def teams(self):
        """
        Api endpoint for teams

        :return: Instance of :class:`~endpoints.teams.Teams`
        """
        return Teams(self.client)

    @property
    def channels(self):
        """
        Api endpoint for channels

        :return: Instance of :class:`~endpoints.channels.Channels`
        """
        return Channels(self.client)

    @property
    def posts(self):
        """
        Api endpoint for posts

        :return: Instance of :class:`~endpoints.posts.Posts`
        """
        return Posts(self.client)

    @property
    def files(self):
        """
        Api endpoint for files

        :return: Instance of :class:`~endpoints.files.Files`
        """
        return Files(self.client)

    @property
    def preferences(self):
        """
        Api endpoint for preferences

        :return: Instance of :class:`~endpoints.preferences.Preferences`
        """
        return Preferences(self.client)

    @property
    def emoji(self):
        """
        Api endpoint for emoji

        :return: Instance of :class:`~endpoints.emoji.Emoji`
        """
        return Emoji(self.client)

    @property
    def reactions(self):
        """
        Api endpoint for posts' reactions

        :return: Instance of :class:`~endpoints.reactions.Reactions`
        """
        return Reactions(self.client)

    @property
    def system(self):
        """
        Api endpoint for system

        :return: Instance of :class:`~endpoints.system.System`
        """
        return System(self.client)

    @property
    def webhooks(self):
        """
        Api endpoint for webhooks

        :return: Instance of :class:`~endpoints.webhooks.Webhooks`
        """
        return Webhooks(self.client)

    @property
    def status(self):
        """
        Api endpoint for status

        :return: Instance of :class:`~endpoints.status.Status`
        """
        return Status(self.client)

    @property
    def commands(self):
        """
        Api endpoint for commands

        :return: Instance of :class:`~endpoints.commands.Commands`
        """
        return Commands(self.client)

    @property
    def roles(self):
        """
        Api endpoint for roles

        :return: Instance of :class:`~endpoints.roles.Roles`
        """
        return Roles(self.client)

    @property
    def integration_actions(self):
        """
        Api endpoint for integration actions

        :return: Instance of :class:`~endpoints.integration_actions.IntegrationActions`
        """
        return IntegrationActions(self.client)
