from .game_state import GameState
from ..my_agent import Agent
import asyncio
import os

uri = os.environ.get(
    'GAME_CONNECTION_STRING') or "ws://127.0.0.1:3000/?role=agent&agentId=agentId&name=defaultName"


class Client:
    def __init__(self):
        self._client = GameState(uri)
        self.agent = Agent()

        self._client.set_game_tick_callback(self._on_game_tick)
        loop = asyncio.get_event_loop()
        connection = loop.run_until_complete(self._client.connect())
        tasks = [
            asyncio.ensure_future(self._client._handle_messages(connection)),
        ]
        loop.run_until_complete(asyncio.wait(tasks))

    async def _on_game_tick(self, tick_number, game_state):
        next_action = self.agent.next_move(tick_number, game_state)
        await self.handle_next_action(next_action, game_state)

    def get_bomb_to_detonate(self, game_state) -> tuple[int, int] or None:
        if 'detonation_target' in game_state:
            return game_state['detonation_target']
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
            if bomb_coordinates is not None:
                x, y = bomb_coordinates
                await self._client.send_detonate(x, y)
        else:
            print(f"Unhandled action: {action}")
        pass
