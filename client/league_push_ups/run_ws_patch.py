from json import loads, JSONDecodeError
from lcu_driver.connection import Connection, logger
import aiohttp
import asyncio

async def run_ws(self: Connection) -> None:
    """Start the websoocket connection. This is responsible to raise Connector close event and
    handling the websocket events.

    :return: None
    """
    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth('riot', self._auth_key), # pylint: disable=protected-access
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
    ) as session:
        async with session.ws_connect(self.ws_address, ssl=False) as ws:
            await ws.send_json([5, 'OnJsonApiEvent'])
            await ws.receive()

            async for msg in ws:
                await asyncio.sleep(0)
                logger.debug('Websocket frame received')

                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        data = loads(msg.data)[2]
                        self._connector.ws.match_event(self._connector, self, data)               # pylint: disable=protected-access
                    except JSONDecodeError:
                        logger.warning('Error decoding the following JSON: %s', msg.data)

                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break
