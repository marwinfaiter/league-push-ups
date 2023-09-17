from lcu_driver.connection import Connection, logger
from lcu_driver.utils import _return_ux_process
import time
import asyncio

async def start(self) -> None:
    """Starts the connector. This method should be overridden if different behavior is required.

    :rtype: None
    """
    try:
        async def wrapper():
            process = next(_return_ux_process(), None)
            while not process:
                process = next(_return_ux_process(), None)
                time.sleep(0.5)

            connection = Connection(self, process)
            self.register_connection(connection)
            await connection.init()

            if self._repeat_flag and len(self.ws.registered_uris) > 0:
                logger.debug('Repeat flag=True. Looking for new clients.')
                wrapper()

        await wrapper()
    except KeyboardInterrupt:
        logger.info('Event loop interrupted by keyboard')
    except asyncio.exceptions.CancelledError:
        pass
