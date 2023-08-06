==============
Ercoin reactor
==============

`ern_reactor` is a Python library that allows performing arbitrary actions in reaction to `Ercoin <https://ercoin.tech>`_ transfers, with live synchronization and catching up after coming back online. Licensed under `Apache License 2.0 <https://apache.org/licenses/LICENSE-2.0>`_. Python 3.8 or newer is required.

How to use
----------

See the help for ``ern_reactor.ErcoinReactor``:

.. code:: python

   import ern_reactor
   help(ern_reactor.ErcoinReactor)

You need to implement the ``get_namespace`` and ``process_tx`` methods. To inspect the structure of the transaction dictionary which is passed to ``process_tx``, see ``ern_reactor.TransferTx.__annotations__``.

A basic example
---------------

This scripts connects to a local Ercoin node and live prints transaction values for transfers received by an Ercoin address (Base64-encoded) specified on the command line:


.. code:: python

   import asyncio
   import decimal
   import sys

   from ern_reactor import ErcoinReactor


   class DummyReactor(ErcoinReactor):
       def get_namespace(self):
           return 'dummy'

       async def process_tx(self, tx):
           amount_in_ern = decimal.Decimal(tx['value']) / 10**6
           print(f'Received {amount_in_ern} ERN')


   if __name__ == '__main__':
       reactor = DummyReactor(
           node='127.0.0.1',
           address=sys.argv[1],
           ssl=False,
       )
       try:
           asyncio.run(reactor.start())
       except KeyboardInterrupt:
           sys.exit(0)
