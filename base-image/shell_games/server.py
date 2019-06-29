import asyncio
from .user import User
from .cursor import Cursor


class Controller:
    def __init__(self, *users):
        self._users = users
        self.setUp(*users)
    
    def setUp(self, *users):
        pass

    async def start(self):
        try:
            await self.run()
        except (BrokenPipeError, ConnectionResetError) as e:
            await self.on_disconnect(e)
            await self.teardown()

    async def run(self):
        raise NotImplementedError

    async def on_disconnect(self, error):
        pass
    
    async def teardown(self):
        await asyncio.gather(*[
            u.close() for u in self._users
        ])
    
    async def send_to_users(self, msg):
        return await asyncio.gather(*[
            u.send(msg) for u in self._users
        ])


class Server:
    HOST = "0.0.0.0"
    PORT = 3000
    controller_class = None
    player_count = 1
    
    def start(self):
        """ Start listening for connections and starting games.
        Should not be overridden
        """
        try:
            asyncio.run(self._start_serving())
        except KeyboardInterrupt:
            print("user shutdown\n")

    async def user_connected(self, user):
        """ First read/write opportunity for a connected user. Good
        place to send initial welcome messages, etc.
        """
        pass

    async def should_accept_user(self, user):
        """ Any logic to determine if the user is allowed to play
        """
        return True
    
    async def on_user_accepted(self, user):
        """ First read/write opportunity after a user is accepted
        """
        pass
    
    def get_controller_class(self):
        return self.controller_class

    async def launch_game(self, *users):
        """ create an instance of game_controller and call it's run
        method
        """
        controller_class = self.get_controller_class()
        controller = controller_class(*users)
        asyncio.create_task(controller.start())        

    async def _start_serving(self):
        """ start a self._server_task which acts as a producer of users, and
        a self._start_games_task which is a consumer of users. Should not be
        overridden.
        """
        self._player_queue = asyncio.Queue()
        server_task = asyncio.create_task(
            self._server_task()
        )
        start_games_task = asyncio.create_task(
            self._start_game_task()
        )
        await asyncio.gather(
            server_task,
            start_games_task
        )

    async def _on_connection(self, reader, writer):
        """ Queue a newly connected user after calling appropriate hooks.
        """
        print("connection")
        user = User(reader, writer)
        try:
            await self.user_connected(user)
            if await self.should_accept_user(user):
                await self.on_user_accepted(user)
                await self._player_queue.put(user)
            else:
                await user.close()
        except ConnectionResetError:
            print("user disconnected")

    async def _start_game_task(self):
        """ Block until self.player_count users have connected, then call run.
        """
        while True:
            asyncio.create_task(self.launch_game(*[
                await self._player_queue.get() for _ in range(self.player_count)
            ]))

    async def _server_task(self):
        """ Start the async server.
        """
        server = await asyncio.start_server(
            self._on_connection,
            host=self.HOST,
            port=self.PORT,
            reuse_port=True
        )
        async with server:
            await server.serve_forever()


class RequireTokenServer(Server):
    """ Only accept user's if they provide a valid, signed JWT
    """
    enter_token_prompt = "Enter your token: "

    async def should_accept_user(self, user):
        await user.send(self.enter_token_prompt)
        token = await user.readline()
        return self.verify_token(token)
    
    async def on_user_accepted(self, user):
        await user.send(
            f"{Cursor.up(1)}"
            f"{Cursor.move_to_column(len(self.enter_token_prompt))}"
            f"{Cursor.ERASE_TO_LINE_END}"
            f"{Cursor.green(' accepted')}\n"
        )
        return await super().on_user_accepted(user)

    def verify_token(self, token):
        return token == "shellgames" # will verify jwt, this for now

