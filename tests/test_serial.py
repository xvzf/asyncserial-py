"""
    A USB Serial converter is needed for testing, simply short RxD and TxD
    and run the test suite with tox
"""

import random
import asyncio
import unittest
import pytest
from asyncserial import Serial

try:
    import uvloop
    test_uvloop = True
except ImportError:
    pass

PORT = "/dev/ttyUSB0"
# Max baudrate of the FTDI UART converter, greatly decreases test time
BAUD = 921600 


test_bytes = bytearray(range(256))


def generate_random_input(n):
    """
    Helper to generate random input
    """
    return bytes(random.sample(test_bytes, k=n))


class Test_serial_asyncio(unittest.TestCase):
    """
    Tests with standard asyncio loop
    """
    
    def setUp(self):
        """
        Initializes eventloop and serial
        """
        self.setup_loop()
        self._serial = Serial(self._loop, PORT, baudrate=BAUD)
    

    def setup_loop(self):
        """
        Setup asyncio eventloop
        """
        self._loop = asyncio.get_event_loop()
    

    def run_async(self, test_async):
        """
        Helper to test async code
        
        :param test_async: async coroutine to run
        """
        self._loop.run_until_complete(test_async)


    def test_await_write(self):
        """
        Test if flush is working correctly
        """
        async def await_write(n):
            tmp = generate_random_input(n)
            # Waits until the output queue is flushed
            await self._serial.write(tmp, await_blocking=True)
            assert self._serial.out_waiting == 0
            # Cleanup for th next tests
            await self._serial.read()
        
        
        for n in [100, 200, 256]:
            self.run_async(await_write(n))


    def test_n_write_n_out_async(self):
        """
        Test if every a random bytesequence of length from 1 to 256
        gets written and received correctly
        """
        
        async def n_write_n_out(n):
            tmp = generate_random_input(n)
            await self._serial.write(tmp)
            assert tmp == await self._serial.read(n)
            
        for n in [100, 200, 256]:
            self.run_async(n_write_n_out(n))
    

    def test_read_all(self):
        """
        Test if read automatically detemines how many bytes are in the input
        queue
        """

        async def read_auto(n):
            tmp = generate_random_input(n)
            await self._serial.write(tmp, await_blocking=True)
            # Giving the input buffer some time to refresh
            await asyncio.sleep(0.1)
            # Automaticall determines how many bytes to read
            assert tmp == await self._serial.read()

        for n in [100, 200, 256]:
            self.run_async(read_auto(n))
    

    def test_flush(self):
        """
        Test if flush is working
        """

        async def flush_2048():
            # write 4096 bytes
            await self._serial.write(("a" * 2048).encode("ASCII"), await_blocking=False)
            await self._serial.flush()
            # Output queue should be cleared by now
            assert self._serial.out_waiting == 0
            # Give the input queue some time to keep up
            await asyncio.sleep(0.2)
            assert self._serial.in_waiting == 2048
            # Clear input queue for the next test 
            await self._serial.read()

        self.run_async(flush_2048())
    

    def test_readline(self):
        """
        Test if readline is working
        """

        async def readline_async(line):
            line += b"\r\n"
            await self._serial.write(line, await_blocking=True)

            # Readline should be equal to the line
            assert line == await self._serial.readline()
        
        lines = [
            "Hello World!",
            "This is ASYNCSERIAL",
            "\x13\x17 LEET \xbe\xef"
        ]

        for line in lines:
            self.run_async(readline_async(line.encode()))


@pytest.mark.skipif(not test_uvloop, reason="UVLOOP is not available, skipping test")
class Test_serial_uvloop(Test_serial_asyncio):
    """
    Tests with uvloop
    """

    def setup_loop(self):
        """
        Setup uvloop eventloop
        """
        self._loop = uvloop.new_event_loop()