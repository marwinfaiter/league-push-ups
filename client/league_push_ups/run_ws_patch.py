from json import loads, JSONDecodeError
from lcu_driver.connection import Connection, logger
import aiohttp
import asyncio

async def run_ws(self: Connection) -> None:
    """Start the websoocket connection. This is responsible to raise Connector close event and
    handling the websocket events.

    :return: None
    """
    local_session = aiohttp.ClientSession(auth=aiohttp.BasicAuth('riot', self._auth_key), # pylint: disable=protected-access
                                            headers={'Content-Type': 'application/json',
                                                    'Accept': 'application/json'})
    self._ws = await local_session.ws_connect(self.ws_address, ssl=False)                 # pylint: disable=protected-access
    await self._ws.send_json([5, 'OnJsonApiEvent'])                                       # pylint: disable=protected-access
    _ = await self._ws.receive()                                                          # pylint: disable=protected-access

    while self.closed is False:
        await asyncio.sleep(0)
        msg = await self._ws.receive()                                                    # pylint: disable=protected-access
        logger.debug('Websocket frame received')

        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                data = loads(msg.data)[2]
                self._connector.ws.match_event(self._connector, self, data)               # pylint: disable=protected-access
            except JSONDecodeError:
                logger.warning('Error decoding the following JSON: %s', msg.data)

        elif msg.type == aiohttp.WSMsgType.CLOSED:
            break
    await self._ws.close()                                                                # pylint: disable=protected-access
    await local_session.close()
