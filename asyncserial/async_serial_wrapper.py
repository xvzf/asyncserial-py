import asyncio
import serial

class Serial(object):
    """
    aioserial is a simple wrapper for the pyserial library to provide async functionallity.
    It is transparent to the pyserial interface and supports all parameters.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, *args, **kwargs):
        """
        Initializes the async wrapper and Serial interface
        :param loop: The main eventloop
        :param *args: Arguments passed through to serial.Serial()
        :param **kwargs: Keyword arguments passed through to serial.Serial()
        """
        self._loop                  = loop
        self._serial_instance       = serial.Serial(*args, **kwargs)
        self._asyncio_sleep_time    = 0.0005 

        #Setup for async
        self._init()


    def _init(self):
        """
        Setups the serial connection for use with async (Setting both read and writetimeouts to 0)
        """
        # Set the serial instance to non blocking
        self._serial_instance.timeout = 0
        self._serial_instance.write_timeout = 0

    
    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """
        Returns the eventloop
        :return: Eventloop
        """
        return self._loop

    
    @property
    def is_open(self) -> bool:
        """
        Connection is open or closed
        :return: True if the connection is open, false otherwise
        """
        return self._serial_instance.isOpen()


    @property
    def serial_instance(self) -> serial.Serial:
        """
        Returns the serial instance
        :return: Serial instance
        """
        return self._serial_instance
    

    @property
    def out_waiting(self) -> int:
        """
        Returns the number of bytes which are in queue to get written
        :return: Number of not yet written bytes
        """
        return self._serial_instance.out_waiting


    @property
    def in_waiting(self) -> int:
        """
        Returns the length of the input queue
        :return: Number of bytes available to be read
        """
        return self._serial_instance.in_waiting


    async def close(self):
        """
        Closes the serial connection gratefully, flushes output buffer
        """
        await self.flush()
        self.is_open = False
    

    async def abort(self):
        """
        Closes the serial connection immediately, output queue will be discarded
        """
        self._serial_instance.close()
    

    async def flush(self):
        """
        Flushes output queue
        """
        while self.out_waiting > 0:
            await asyncio.sleep(self._asyncio_sleep_time)

    async def write(self, bytes:bytes, await_blocking=False):
        """
        Writes a bytestring
        :param bytestring:      Write buffer
        :param await_blocking:  wait for everything to be written
        """
        self._serial_instance.write(bytes)
        return await self.flush()
    

    async def read(self, bytecount=0) -> bytes:
        """
        Reads a given number of bytes
        :param bytecount: How many bytes to read, leave it at default to read everything that is available
        :return: bytestring
        """
        if bytecount < 1:
            bytecount = self.in_waiting or 1

        while True:
            
            if self.in_waiting < bytecount:
                await asyncio.sleep(self._asyncio_sleep_time)

            else:
                # Try to read bytes
                inbytes = self._serial_instance.read(bytecount)

                # Just for safety, should never happen
                if not inbytes:
                    await asyncio.sleep(self._asyncio_sleep_time)
                else:
                    return inbytes
    

    async def readline(self):
        """
        Reads one line
        :return: bytestring of the line
        """
        while True:
            line = self._serial_instance.readline()
            if not line:
                await asyncio.sleep(self._asyncio_sleep_time)
            else:
                return line