============================
Asyncio wrapper for pyserial
============================

.. image:: https://badge.fury.io/py/asyncserial.svg
   :target: https://badge.fury.io/py/asyncserial
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/asyncserial.svg
   :target: https://pypi.org/project/asyncserial/
   :alt: Python Versions

.. image:: https://readthedocs.org/projects/asyncserial/badge/?version=latest
   :target: http://asyncserial.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


`asyncserial` is a a wrapper for the `pyserial` library providing an async interface based on `async def` and `await`.


Installation
============

.. code-block:: sh
  pip install asyncserial


Documentation
=============
https://asyncserial.readthedocs.io


Examples
========
.. code-block:: python

   import asyncio
   from asyncserial import Serial

   loop = asyncio.get_event_loop()

   test_serial = Serial(loop, "/dev/ttyACM0", baudrate=115200)

   async def test():
       await test_serial.read() # Drop anything that was already received
       while True:
           line = await test_serial.readline() # Read a line
           print("[+] Serial read: {}".format(line))
           await asyncio.sleep(0) # Let's be a bit greedy, should be adjust to your needs


   asyncio.ensure_future(test())

   print("[+] Starting eventloop")
   loop.run_forever()
