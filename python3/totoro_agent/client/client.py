from .game_state import GameState
import asyncio

class Client:
    def __init__(self, uri, get_next_action):
        self._client = GameState(uri)
        self.get_next_action = get_next_action

        self._client.set_game_tick_callback(self._on_game_tick)
        loop = asyncio.get_event_loop()
        connection = loop.run_until_complete(self._client.connect())
        tasks = [
            asyncio.ensure_future(self._client._handle_messages(connection)),
        ]
        loop.run_until_complete(asyncio.wait(tasks))

    async def _on_game_tick(self, tick_number, game_state):
        next_action = self.get_next_action(tick_number, game_state)
        await self.handle_next_action(next_action, game_state)

    def get_bomb_to_detonate(self, game_state) -> [int, int] or None:
        agent_number = game_state.get("connection").get("agent_number")
        entities = self._client._state.get("entities")
        bombs = list(filter(lambda entity: entity.get(
            "owner") == agent_number and entity.get("type") == "b", entities))
        bomb = next(iter(bombs or []), None)
        if bomb != None:
            return [bomb.get("x"), bomb.get("y")]
        else:
            return None

    async def handle_next_action(self, action, game_state):
        print("Next action", action)
        if action in ["up", "left", "right", "down"]:
            await self._client.send_move(action)
        elif action == "bomb":
            await self._client.send_bomb()
        elif action == "detonate":
            bomb_coordinates = self.get_bomb_to_detonate(game_state)
            if bomb_coordinates != None:
                x, y = bomb_coordinates
                await self._client.send_detonate(x, y)
        else:
            print(f"Unhandled action: {action}")
        pass
