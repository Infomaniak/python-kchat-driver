import json
import asyncio
import logging
import pysher
import time

log = logging.getLogger("kchat.websocket")
log.setLevel(logging.INFO)


class Websocket:
    def __init__(self, options, token, team_id, team_user_id):
        self.options = options
        if options["debug"]:
            log.setLevel(logging.DEBUG)
        self._token = token
        self._team_id = team_id
        self._team_user_id = team_user_id
        self._alive = True
        self.pusher = False
        self.event_handler = False

    def status_change_callback(self, data):
        data = json.loads(data)
        data["event"] = "status_change"
        asyncio.run(self.event_handler(json.dumps(data)))

    def posted_callback(self, data):
        data = json.loads(data)
        data["event"] = "posted"
        asyncio.run(self.event_handler(json.dumps(data)))

    def hello_callback(self, data):
        asyncio.run(self.event_handler(json.dumps({"event": "pusher_internal:subscription_succeeded"})))

    def connect_handler(self, data, *args):

        channel = self.pusher.subscribe("private-team.{}".format(self._team_id))
        channel.bind("status_change", self.status_change_callback)

        channel = self.pusher.subscribe("private-teamUser.{}".format(self._team_user_id))
        channel.bind("pusher_internal:subscription_succeeded", self.hello_callback)
        channel.bind("posted", self.posted_callback)

    async def connect(self, event_handler):

        """
        Connect to the websocket and authenticate it.
        When the authentication has finished, start the loop listening for messages,
        sending a ping to the server to keep the connection alive.

        :param event_handler: Every websocket event will be passed there. Takes one argument.
        :type event_handler: Function(message)
        :return:
        """
        self._alive = True
        self.event_handler = event_handler

        try:
            self.pusher = pysher.Pusher(
                key="kchat-key",
                custom_host=self.options["websocket_url"],
                auth_endpoint="https://{}/broadcasting/auth".format(self.options["url"]),
                auth_endpoint_headers={"Authorization": f"Bearer {self._token}"},
                log_level=logging.INFO,
                auto_sub=True,
            )

            self.pusher.connection.bind("pusher:connection_established", self.connect_handler)
            self.pusher.connect()

            await self._start_loop()

        except Exception as e:
            log.warning(f"Failed to establish websocket connection: {e}")
            await asyncio.sleep(self.options["keepalive_delay"])

    async def _start_loop(self):
        """
        We will listen for websockets events, sending a heartbeat/pong everytime
        we react a TimeoutError. If we don't the webserver would close the idle connection,
        forcing us to reconnect.
        """
        log.warning("Starting websocket loop")
        while self._alive:
            time.sleep(10)
            self.pusher.connection.send_ping()
