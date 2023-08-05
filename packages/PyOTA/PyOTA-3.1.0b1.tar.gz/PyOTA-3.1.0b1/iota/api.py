from typing import Dict, Iterable, Optional

from iota import AdapterSpec, Address, BundleHash, ProposedTransaction, Tag, \
    TransactionHash, TransactionTrytes, TryteString, TrytesCompatible
from iota.crypto.addresses import AddressGenerator
from iota.api_async import AsyncStrictIota, AsyncIota
import asyncio

__all__ = [
    'InvalidCommand',
    'Iota',
    'StrictIota',
]


class InvalidCommand(ValueError):
    """
    Indicates that an invalid command name was specified.
    """
    pass


# There is a compact and easy way to create the synchronous version of the async
# classes:

# import inspect
# def make_synchronous(new_name, async_class: type):
#   def make_sync(method):
#     def sync_version(*args, **kwargs):
#       return asyncio.get_event_loop().run_until_complete(method(*args, **kwargs))
#     return sync_version

#   return type(new_name, (async_class,), {
#     name: make_sync(method) if inspect.iscoroutinefunction(method) else method
#     for name, method in inspect.getmembers(async_class)
#   })

# # create the sync version of the class
# Iota = make_synchronous('Iota', AsyncIota)

# While this approach would work, no IDE static analysis would pick up the
# method definitions or docstrings for the new `Iota` class, meaning no
# suggestions, intellisense, code completion, etc. for the user.
# Therefore we keep the manual approach.


class StrictIota(AsyncStrictIota):
    """
    Synchronous API to send HTTP requests for communicating with an IOTA node.

    This implementation only exposes the "core" API methods.  For a more
    feature-complete implementation, use :py:class:`Iota` instead.

    References:

    - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference

    :param AdapterSpec adapter:
        URI string or BaseAdapter instance.

    :param Optional[bool] devnet:
        Whether to use devnet settings for this instance.
        On the devnet, minimum weight magnitude is set to 9, on mainnet
        it is 1 by default.

    :param Optional[bool] local_pow:
        Whether to perform proof-of-work locally by redirecting all calls
        to :py:meth:`attach_to_tangle` to
        `ccurl pow interface <https://pypi.org/project/PyOTA-PoW/>`_.

            See :ref:`README:Optional Local Pow` for more info and
            :ref:`find out<pow-label>` how to use it.

    """

    def __init__(
            self,
            adapter: AdapterSpec,
            devnet: bool = False,
            local_pow: bool = False
    ) -> None:
        """
        :param AdapterSpec adapter:
            URI string or BaseAdapter instance.

        :param bool devnet:
            Whether to use devnet settings for this instance.
            On the devnet, minimum weight magnitude is set to 9, on mainnet
            it is 1 by default.

        :param Optional[bool] local_pow:
            Whether to perform proof-of-work locally by redirecting all calls
            to :py:meth:`attach_to_tangle` to
            `ccurl pow interface <https://pypi.org/project/PyOTA-PoW/>`_.

                See :ref:`README:Optional Local Pow` for more info and
                :ref:`find out<pow-label>` how to use it.
        """
        super().__init__(adapter, devnet, local_pow)

    def add_neighbors(self, uris: Iterable[str]) -> dict:
        """
        Add one or more neighbors to the node.  Lasts until the node is
        restarted.

        :param Iterable[str] uris:
            Use format ``<protocol>://<ip address>:<port>``.
            Example: ``add_neighbors(['udp://example.com:14265'])``

            .. note::
                These URIs are for node-to-node communication (e.g.,
                weird things will happen if you specify a node's HTTP
                API URI here).

        :return:
            ``dict`` with the following structure::

                {
                    'addedNeighbors': int,
                        Total number of added neighbors.
                    'duration': int,
                        Number of milliseconds it took to complete the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#addneighbors
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().add_neighbors(uris)
        )

    def attach_to_tangle(
            self,
            trunk_transaction: TransactionHash,
            branch_transaction: TransactionHash,
            trytes: Iterable[TryteString],
            min_weight_magnitude: Optional[int] = None,
    ) -> dict:
        """
        Attaches the specified transactions (trytes) to the Tangle by
        doing Proof of Work. You need to supply branchTransaction as
        well as trunkTransaction (basically the tips which you're going
        to validate and reference with this transaction) - both of which
        you'll get through the :py:meth:`get_transactions_to_approve` API call.

        The returned value is a different set of tryte values which you
        can input into :py:meth:`broadcast_transactions` and
        :py:meth:`store_transactions`.

        :param TransactionHash trunk_transaction:
            Trunk transaction hash.

        :param TransactionHash branch_transaction:
            Branch transaction hash.

        :param Iterable[TransactionTrytes] trytes:
            List of transaction trytes in the bundle to be attached.

        :param Optional[int] min_weight_magnitude:
            Minimum weight magnitude to be used for attaching trytes.
            14 by default on mainnet, 9 on devnet/devnet.

        :return:
            ``dict`` with the following structure::

                {
                    'trytes': List[TransactionTrytes],
                        Transaction trytes that include a valid nonce field.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#attachtotangle
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().attach_to_tangle(
                        trunk_transaction,
                        branch_transaction,
                        trytes,
                        min_weight_magnitude,
                )
        )

    def broadcast_transactions(self, trytes: Iterable[TryteString]) -> dict:
        """
        Broadcast a list of transactions to all neighbors.

        The input trytes for this call are provided by
        :py:meth:`attach_to_tangle`.

        :param Iterable[TransactionTrytes] trytes:
            List of transaction trytes to be broadcast.

        :return:
            ``dict`` with the following structure::

                {
                    'duration': int,
                        Number of milliseconds it took to complete the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#broadcasttransactions
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().broadcast_transactions(
                        trytes,
                )
        )

    def check_consistency(self, tails: Iterable[TransactionHash]) -> dict:
        """
        Used to ensure tail resolves to a consistent ledger which is
        necessary to validate before attempting promotion. Checks
        transaction hashes for promotability.

        This is called with a pending transaction (or more of them) and
        it will tell you if it is still possible for this transaction
        (or all the transactions simultaneously if you give more than
        one) to be confirmed, or not (because it conflicts with another
        already confirmed transaction).

        :param Iterable[TransactionHash] tails:
            Transaction hashes. Must be tail transactions.

        :return:
            ``dict`` with the following structure::

                {
                    'state': bool,
                        Whether tails resolve to consistent ledger.
                    'info': str,
                        This field will only exist if 'state' is ``False``.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#checkconsistency
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().check_consistency(
                        tails,
                )
        )

    def find_transactions(
            self,
            bundles: Optional[Iterable[BundleHash]] = None,
            addresses: Optional[Iterable[Address]] = None,
            tags: Optional[Iterable[Tag]] = None,
            approvees: Optional[Iterable[TransactionHash]] = None,
    ) -> dict:
        """
        Find the transactions which match the specified input and
        return.

        All input values are lists, for which a list of return values
        (transaction hashes), in the same order, is returned for all
        individual elements.

        Using multiple of these input fields returns the intersection of
        the values.

        :param Optional[Iterable[BundleHash] bundles:
          List of bundle IDs.

        :param Optional[Iterable[Address]] addresses:
            List of addresses.

        :param Optional[Iterable[Tag]] tags:
            List of tags.

        :param Optional[Iterable[TransactionHash]] approvees:
            List of approvee transaction IDs.

        :return:
            ``dict`` with the following structure::

                {
                    'hashes': List[TransationHash],
                        Found transactions.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#findtransactions
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().find_transactions(
                        bundles,
                        addresses,
                        tags,
                        approvees,
                )
        )

    def get_balances(
            self,
            addresses: Iterable[Address],
            tips: Optional[Iterable[TransactionHash]] = None,
    ) -> dict:
        """
        Returns the confirmed balance which a list of addresses have at the
        latest confirmed milestone.

        In addition to the balances, it also returns the milestone as
        well as the index with which the confirmed balance was
        determined.  The balances are returned as a list in the same
        order as the addresses were provided as input.

        :param Iterable[Address] addresses:
            List of addresses to get the confirmed balance for.

        :param Optional[Iterable[TransactionHash]] tips:
            Tips whose history of transactions to traverse to find the balance.

        :return:
            ``dict`` with the following structure::

                {
                    'balances': List[int],
                        List of balances in the same order as the addresses
                        parameters that were passed to the endpoint.
                    'references': List[TransactionHash],
                        The referencing tips. If no tips parameter was passed
                        to the endpoint, this field contains the hash of the
                        latest milestone that confirmed the balance.
                    'milestoneIndex': int,
                        The index of the milestone that confirmed the most
                        recent balance.
                    'duration': int,
                        Number of milliseconds it took to process the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#getbalances
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_balances(
                        addresses,
                        tips,
                )
        )

    def get_inclusion_states(
            self,
            transactions: Iterable[TransactionHash],
    ) -> dict:
        """
        Get the inclusion states of a set of transactions. This is for
        determining if a transaction was accepted and confirmed by the
        network or not.

        :param Iterable[TransactionHash] transactions:
            List of transactions you want to get the inclusion state
            for.

        :return:
            ``dict`` with the following structure::

                {
                    'states': List[bool],
                        List of boolean values in the same order as the
                        transactions parameters. A ``True`` value means the
                        transaction was confirmed.
                    'duration': int,
                        Number of milliseconds it took to process the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#getinclusionstates
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_inclusion_states(
                        transactions,
                )
        )

    # Add an alias for this call, more descriptive
    is_confirmed = get_inclusion_states

    def get_missing_transactions(self) -> dict:
        """
        Returns all transaction hashes that a node is currently requesting
        from its neighbors.

        :return:
            ``dict`` with the following structure::

                {
                    'hashes': List[TransactionHash],
                        Array of missing transaction hashes.
                    'duration': int,
                        Number of milliseconds it took to process the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#getmissingtransactions
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_missing_transactions()
        )

    def get_neighbors(self) -> dict:
        """
        Returns the set of neighbors the node is connected with, as well
        as their activity count.

        The activity counter is reset after restarting IRI.

        :return:
            ``dict`` with the following structure::

                {
                    'neighbors': List[dict],
                        Array of objects, including the following fields with
                        example values:
                            "address": "/8.8.8.8:14265",
                            "numberOfAllTransactions": 158,
                            "numberOfRandomTransactionRequests": 271,
                            "numberOfNewTransactions": 956,
                            "numberOfInvalidTransactions": 539,
                            "numberOfStaleTransactions": 663,
                            "numberOfSentTransactions": 672,
                            "connectiontype": "TCP"
                    'duration': int,
                        Number of milliseconds it took to process the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#getneighbors
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_neighbors()
        )

    def get_node_api_configuration(self) -> dict:
        """
        Returns a node's API configuration settings.

        :return:
            ``dict`` with the following structure::

                {
                    '<API-config-settings>': type,
                        Configuration parameters for a node.
                    ...
                    ...
                    ...

                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/iri-configuration-options
        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#getnodeapiconfiguration
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_node_api_configuration()
        )

    def get_node_info(self) -> dict:
        """
        Returns information about the node.

        :return:
            ``dict`` with the following structure::

                {
                    'appName': str,
                        Name of the IRI network.
                    'appVersion': str,
                        Version of the IRI.
                    'jreAvailableProcessors': int,
                        Available CPU cores on the node.
                    'jreFreeMemory': int,
                        Amount of free memory in the Java virtual machine.
                    'jreMaxMemory': int,
                        Maximum amount of memory that the Java virtual machine
                        can use,
                    'jreTotalMemory': int,
                        Total amount of memory in the Java virtual machine.
                    'jreVersion': str,
                        The version of the Java runtime environment.
                    'latestMilestone': TransactionHash
                        Transaction hash of the latest milestone.
                    'latestMilestoneIndex': int,
                        Index of the latest milestone.
                    'latestSolidSubtangleMilestone': TransactionHash,
                        Transaction hash of the latest solid milestone.
                    'latestSolidSubtangleMilestoneIndex': int,
                        Index of the latest solid milestone.
                    'milestoneStartIndex': int,
                        Start milestone for the current version of the IRI.
                    'neighbors': int,
                        Total number of connected neighbor nodes.
                    'packetsQueueSize': int,
                        Size of the packet queue.
                    'time': int,
                        Current UNIX timestamp.
                    'tips': int,
                        Number of tips in the network.
                    'transactionsToRequest': int,
                        Total number of transactions that the node is missing in
                        its ledger.
                    'features': List[str],
                        Enabled configuration options.
                    'coordinatorAddress': Address,
                        Address (Merkle root) of the Coordinator.
                    'duration': int,
                        Number of milliseconds it took to process the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#getnodeinfo
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_node_info()
        )

    def get_transactions_to_approve(
            self,
            depth: int,
            reference: Optional[TransactionHash] = None,
    ) -> dict:
        """
        Tip selection which returns ``trunkTransaction`` and
        ``branchTransaction``.

        :param int depth:
          Number of milestones to go back to start the tip selection algorithm.

          The higher the depth value, the more "babysitting" the node
          will perform for the network (as it will confirm more
          transactions that way).

        :param TransactionHash reference:
          Transaction hash from which to start the weighted random walk.
          Use this parameter to make sure the returned tip transaction hashes
          approve a given reference transaction.

        :return:
            ``dict`` with the following structure::

                {
                    'trunkTransaction': TransactionHash,
                        Valid trunk transaction hash.
                    'branchTransaction': TransactionHash,
                        Valid branch transaction hash.
                    'duration': int,
                        Number of milliseconds it took to complete the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#gettransactionstoapprove
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_transactions_to_approve(
                        depth,
                        reference,
                )
        )

    def get_trytes(self, hashes: Iterable[TransactionHash]) -> dict:
        """
        Returns the raw transaction data (trytes) of one or more
        transactions.

        :return:
            ``dict`` with the following structure::

                {
                    'trytes': List[TransactionTrytes],
                        List of transaction trytes for the given transaction
                        hashes (in the same order as the parameters).
                    'duration': int,
                        Number of milliseconds it took to complete the request.
                }

            .. note::
                If a node doesn't have the trytes for a given transaction hash in
                its ledger, the value at the index of that transaction hash is either
                ``null`` or a string of 9s.

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#gettrytes
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_trytes(
                        hashes,
                )
        )

    def interrupt_attaching_to_tangle(self) -> dict:
        """
        Interrupts and completely aborts the :py:meth:`attach_to_tangle`
        process.

        :return:
            ``dict`` with the following structure::

                {
                    'duration': int,
                        Number of milliseconds it took to complete the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#interruptattachingtotangle
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().interrupt_attaching_to_tangle()
        )

    def remove_neighbors(self, uris: Iterable[str]) -> dict:
        """
        Removes one or more neighbors from the node.  Lasts until the
        node is restarted.

        :param str uris:
            Use format ``<protocol>://<ip address>:<port>``.
            Example: `remove_neighbors(['udp://example.com:14265'])`

        :return:
            ``dict`` with the following structure::

                {
                    'removedNeighbors': int,
                        Total number of removed neighbors.
                    'duration': int,
                        Number of milliseconds it took to complete the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#removeneighbors
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().remove_neighbors(uris)
        )

    def store_transactions(self, trytes: Iterable[TryteString]) -> dict:
        """
        Store transactions into local storage of the node.

        The input trytes for this call are provided by
        :py:meth:`attach_to_tangle`.

        :param TransactionTrytes trytes:
            Valid transaction trytes returned by :py:meth:`attach_to_tangle`.

        :return:
            ``dict`` with the following structure::

                {
                    'trytes': TransactionTrytes,
                        Stored trytes.
                    'duration': int,
                        Number of milliseconds it took to complete the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#storetransactions
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().store_transactions(trytes)
        )

    def were_addresses_spent_from(
            self,
            addresses: Iterable[Address]
    ) -> dict:
        """
        Check if a list of addresses was ever spent from, in the current
        epoch, or in previous epochs.

        If an address has a pending transaction, it's also considered 'spent'.

        :param Iterable[Address] addresses:
            List of addresses to check.

        :return:
            ``dict`` with the following structure::

                {
                    'states': List[bool],
                        States of the specified addresses in the same order as
                        the values in the addresses parameter. A ``True`` value
                        means that the address has been spent from.
                    'duration': int,
                        Number of milliseconds it took to complete the request.
                }

        References:

        - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference#wereaddressesspentfrom
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().were_addresses_spent_from(addresses)
        )


class Iota(StrictIota, AsyncIota):
    """
    Implements the synchronous core API, plus additional synchronous wrapper
    methods for common operations.

    :param AdapterSpec adapter:
        URI string or BaseAdapter instance.

    :param Optional[Seed] seed:
        Seed used to generate new addresses.
        If not provided, a random one will be generated.

        .. note::
            This value is never transferred to the node/network.

    :param Optional[bool] devnet:
        Whether to use devnet settings for this instance.
        On the devnet, minimum weight magnitude is decreased, on mainnet
        it is 14 by default.

        For more info on the Mainnet and the Devnet, visit
        `the official docs site<https://docs.iota.org/docs/getting-started/0.1/network/iota-networks/>`.

    :param Optional[bool] local_pow:
        Whether to perform proof-of-work locally by redirecting all calls
        to :py:meth:`attach_to_tangle` to
        `ccurl pow interface <https://pypi.org/project/PyOTA-PoW/>`_.

            See :ref:`README:Optional Local Pow` for more info and
            :ref:`find out<pow-label>` how to use it.

    References:

    - https://docs.iota.org/docs/node-software/0.1/iri/references/api-reference
    - https://github.com/iotaledger/wiki/blob/master/api-proposal.md
    """

    def __init__(
            self,
            adapter: AdapterSpec,
            seed: Optional[TrytesCompatible] = None,
            devnet: bool = False,
            local_pow: bool = False
    ) -> None:
        """
        :param seed:
            Seed used to generate new addresses.
            If not provided, a random one will be generated.

            .. note::
                This value is never transferred to the node/network.
        """
        # Explicitly call AsyncIota's init, as we need the seed
        AsyncIota.__init__(self, adapter, seed, devnet, local_pow)

    def broadcast_and_store(
            self,
            trytes: Iterable[TransactionTrytes]
    ) -> dict:
        """
        Broadcasts and stores a set of transaction trytes.

        :param Iterable[TransactionTrytes] trytes:
            Transaction trytes to broadcast and store.

        :return:
            ``dict`` with the following structure::

                {
                    'trytes': List[TransactionTrytes],
                        List of TransactionTrytes that were broadcast.
                        Same as the input ``trytes``.
                }

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#broadcastandstore
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().broadcast_and_store(trytes)
        )

    def broadcast_bundle(
            self,
            tail_transaction_hash: TransactionHash
    ) -> dict:
        """
        Re-broadcasts all transactions in a bundle given the tail transaction hash.
        It might be useful when transactions did not properly propagate,
        particularly in the case of large bundles.

        :param TransactionHash tail_transaction_hash:
            Tail transaction hash of the bundle.

        :return:
            ``dict`` with the following structure::

                {
                    'trytes': List[TransactionTrytes],
                        List of TransactionTrytes that were broadcast.
                }

        References:

        - https://github.com/iotaledger/iota.js/blob/next/api_reference.md#module_core.broadcastBundle
        """

        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().broadcast_bundle(tail_transaction_hash)
        )

    def find_transaction_objects(
            self,
            bundles: Optional[Iterable[BundleHash]] = None,
            addresses: Optional[Iterable[Address]] = None,
            tags: Optional[Iterable[Tag]] = None,
            approvees: Optional[Iterable[TransactionHash]] = None,
    ) -> dict:
        """
        A more extensive version of :py:meth:`find_transactions` that
        returns transaction objects instead of hashes.

        Effectively, this is :py:meth:`find_transactions` +
        :py:meth:`get_trytes` + converting the trytes into
        transaction objects.

        It accepts the same parameters as :py:meth:`find_transactions`.

        Find the transactions which match the specified input.
        All input values are lists, for which a list of return values
        (transaction hashes), in the same order, is returned for all
        individual elements. Using multiple of these input fields returns the
        intersection of the values.

        :param Optional[Iterable[BundleHash]] bundles:
          List of bundle IDs.

        :param Optional[Iterable[Address]] addresses:
            List of addresses.

        :param Optional[Iterable[Tag]] tags:
            List of tags.

        :param Optional[Iterable[TransactionHash]] approvees:
            List of approvee transaction IDs.

        :return:
            ``dict`` with the following structure::

                {
                    'transactions': List[Transaction],
                        List of Transaction objects that match the input.
                }

        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().find_transaction_objects(
                        bundles,
                        addresses,
                        tags,
                        approvees,
                )
        )

    def get_account_data(
            self,
            start: int = 0,
            stop: Optional[int] = None,
            inclusion_states: bool = False,
            security_level: Optional[int] = None
    ) -> dict:
        """
        More comprehensive version of :py:meth:`get_transfers` that
        returns addresses and account balance in addition to bundles.

        This function is useful in getting all the relevant information
        of your account.

        :param int start:
            Starting key index.

        :param  Optional[int] stop:
            Stop before this index.

            Note that this parameter behaves like the ``stop`` attribute
            in a :py:class:`slice` object; the stop index is *not*
            included in the result.

            If ``None`` (default), then this method will check every
            address until it finds one that is unused.

            .. note::
                An unused address is an address that **has not been spent from**
                and **has no transactions** referencing it on the Tangle.

                A snapshot removes transactions from the Tangle. As a
                consequence, after a snapshot, it may happen that this API does
                not return the correct account data with ``stop`` being ``None``.

                As a workaround, you can save your used addresses and their
                ``key_index`` attribute in a local database. Use the
                ``start`` and ``stop`` parameters to tell the API from where to
                start checking and where to stop.

        :param bool inclusion_states:
            Whether to also fetch the inclusion states of the transfers.

            This requires an additional API call to the node, so it is
            disabled by default.

        :param  Optional[int] security_level:
            Number of iterations to use when generating new addresses
            (see :py:meth:`get_new_addresses`).

            This value must be between 1 and 3, inclusive.

            If not set, defaults to
            :py:attr:`AddressGenerator.DEFAULT_SECURITY_LEVEL`.

        :return:
            ``dict`` with the following structure::

                {
                    'addresses': List[Address],
                        List of generated addresses.

                        Note that this list may include unused
                        addresses.

                    'balance': int,
                        Total account balance.  Might be 0.

                    'bundles': List[Bundle],
                        List of bundles with transactions to/from this
                        account.
                }

        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_account_data(
                        start,
                        stop,
                        inclusion_states,
                        security_level,
                )
        )

    def get_bundles(
            self,
            transactions: Iterable[TransactionHash]
    ) -> dict:
        """
        Returns the bundle(s) associated with the specified transaction
        hashes.

        :param Iterable[TransactionHash] transactions:
            Transaction hashes.  Must be a tail transaction.

        :return:
            ``dict`` with the following structure::

             {
               'bundles': List[Bundle],
                    List of matching bundles.  Note that this value is
                    always a list, even if only one bundle was found.
             }

        :raise :py:class:`iota.adapter.BadApiResponse`:
          - if any of the bundles fails validation.
          - if any of the bundles is not visible on the Tangle.

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#getbundle
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_bundles(transactions)
        )

    def get_inputs(
            self,
            start: int = 0,
            stop: Optional[int] = None,
            threshold: Optional[int] = None,
            security_level: Optional[int] = None,
    ) -> dict:
        """
        Gets all possible inputs of a seed and returns them, along with
        the total balance.

        This is either done deterministically (by generating all
        addresses until :py:meth:`find_transactions` returns an empty
        result), or by providing a key range to search.

        :param int start:
            Starting key index.
            Defaults to 0.

        :param Optional[int] stop:
            Stop before this index.

            Note that this parameter behaves like the ``stop`` attribute
            in a :py:class:`slice` object; the stop index is *not*
            included in the result.

            If ``None`` (default), then this method will not stop until
            it finds an unused address.

            .. note::
                An unused address is an address that **has not been spent from**
                and **has no transactions** referencing it on the Tangle.

                A snapshot removes transactions from the Tangle. As a
                consequence, after a snapshot, it may happen that this API does
                not return the correct inputs with ``stop`` being ``None``.

                As a workaround, you can save your used addresses and their
                ``key_index`` attribute in a local database. Use the
                ``start`` and ``stop`` parameters to tell the API from where to
                start checking for inputs and where to stop.

        :param Optional[int] threshold:
            If set, determines the minimum threshold for a successful
            result:

            - As soon as this threshold is reached, iteration will stop.
            - If the command runs out of addresses before the threshold
              is reached, an exception is raised.

            .. note::
                This method does not attempt to "optimize" the result
                (e.g., smallest number of inputs, get as close to
                ``threshold`` as possible, etc.); it simply accumulates
                inputs in order until the threshold is met.

            If ``threshold`` is 0, the first address in the key range
            with a non-zero balance will be returned (if it exists).

            If ``threshold`` is ``None`` (default), this method will
            return **all** inputs in the specified key range.

        :param Optional[int] security_level:
            Number of iterations to use when generating new addresses
            (see :py:meth:`get_new_addresses`).

            This value must be between 1 and 3, inclusive.

            If not set, defaults to
            :py:attr:`AddressGenerator.DEFAULT_SECURITY_LEVEL`.

        :return:
            ``dict`` with the following structure::

                {
                    'inputs': List[Address],
                        Addresses with nonzero balances that can be used
                        as inputs.

                    'totalBalance': int,
                        Aggregate balance from all matching addresses.
                }

            Note that each :py:class:`Address` in the result has its
            :py:attr:`Address.balance` attribute set.

            Example:

            .. code-block:: python

                response = iota.get_inputs(...)

                input0 = response['inputs'][0] # type: Address
                input0.balance # 42

        :raise:
            - :py:class:`iota.adapter.BadApiResponse` if ``threshold``
              is not met.  Not applicable if ``threshold`` is ``None``.

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#getinputs
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_inputs(
                        start,
                        stop,
                        threshold,
                        security_level,
                )
        )

    def get_new_addresses(
            self,
            index: int = 0,
            count: int = 1,
            security_level: int = AddressGenerator.DEFAULT_SECURITY_LEVEL,
            checksum: bool = False,
    ):
        """
        Generates one or more new addresses from the seed.

        :param int index:
            The key index of the first new address to generate (must be
            >= 0).

        :param int count:
            Number of addresses to generate (must be >= 1).

            .. tip::
                This is more efficient than calling :py:meth:`get_new_addresses`
                inside a loop.

            If ``None``, this method will progressively generate
            addresses and scan the Tangle until it finds one that has no
            transactions referencing it and was never spent from.

            .. note::
                A snapshot removes transactions from the Tangle. As a
                consequence, after a snapshot, it may happen that when ``count``
                is ``None``, this API call returns a "new" address that used to
                have transactions before the snapshot.
                As a workaround, you can save your used addresses and their
                ``key_index`` attribute in a local database. Use the
                ``index`` parameter to tell the API from where to start
                generating and checking new addresses.

        :param int security_level:
            Number of iterations to use when generating new addresses.

            Larger values take longer, but the resulting signatures are
            more secure.

            This value must be between 1 and 3, inclusive.

        :param bool checksum:
            Specify whether to return the address with the checksum.
            Defaults to ``False``.

        :return:
            ``dict`` with the following structure::

                {
                    'addresses': List[Address],
                        Always a list, even if only one address was
                        generated.
                }

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#getnewaddress
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_new_addresses(
                        count=count,
                        index=index,
                        security_level=security_level,
                        checksum=checksum,
                )
        )

    def get_transaction_objects(
            self,
            hashes: [Iterable[TransactionHash]],
    ) -> dict:
        """
        Fetches transaction objects from the Tangle given their
        transaction IDs (hashes).

        Effectively, this is :py:meth:`get_trytes` +
        converting the trytes into transaction objects.

        Similar to :py:meth:`find_transaction_objects`, but accepts
        list of transaction hashes as input.

        :param Iterable[TransactionHash] hashes:
          List of transaction IDs (transaction hashes).

        :return:
            ``dict`` with the following structure::

                {
                    'transactions': List[Transaction],
                        List of Transaction objects that match the input.
                }
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_transaction_objects(hashes)
        )

    def get_transfers(
            self,
            start: int = 0,
            stop: Optional[int] = None,
            inclusion_states: bool = False
    ) -> dict:
        """
        Returns all transfers associated with the seed.

        :param int start:
            Starting key index.

        :param Optional[int] stop:
            Stop before this index.

            Note that this parameter behaves like the ``stop`` attribute
            in a :py:class:`slice` object; the stop index is *not*
            included in the result.

            If ``None`` (default), then this method will check every
            address until it finds one that is unused.

            .. note::
                An unused address is an address that **has not been spent from**
                and **has no transactions** referencing it on the Tangle.

                A snapshot removes transactions from the Tangle. As a
                consequence, after a snapshot, it may happen that this API does
                not return the expected transfers with ``stop`` being ``None``.

                As a workaround, you can save your used addresses and their
                ``key_index`` attribute in a local database. Use the
                ``start`` and ``stop`` parameters to tell the API from where to
                start checking for transfers and where to stop.

        :param bool inclusion_states:
            Whether to also fetch the inclusion states of the transfers.

            This requires an additional API call to the node, so it is
            disabled by default.

        :return:
            ``dict`` with the following structure::

                {
                    'bundles': List[Bundle],
                        Matching bundles, sorted by tail transaction
                        timestamp.

                        This value is always a list, even if only one
                        bundle was found.
                }

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#gettransfers
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().get_transfers(
                        start,
                        stop,
                        inclusion_states,
                )
        )

    def is_promotable(
            self,
            tails: Iterable[TransactionHash],
    ) -> dict:
        """
        Checks if tail transaction(s) is promotable by calling
        :py:meth:`check_consistency` and verifying that ``attachmentTimestamp``
        is above a lower bound.
        Lower bound is calculated based on number of milestones issued
        since transaction attachment.

        :param Iterable(TransactionHash) tails:
            List of tail transaction hashes.

        :return:
            The return type mimics that of :py:meth:`check_consistency`.
            ``dict`` with the following structure::

                {
                    'promotable': bool,
                        If ``True``, all tails are promotable. If ``False``, see
                        `info` field.

                    'info': Optional(List[str])
                        If `promotable` is ``False``, this contains info about what
                        went wrong.
                        Note that when 'promotable' is ``True``, 'info' does not
                        exist.

                }

        References:
        - https://github.com/iotaledger/iota.js/blob/next/api_reference.md#module_core.isPromotable
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().is_promotable(tails)
        )

    def prepare_transfer(
            self,
            transfers: Iterable[ProposedTransaction],
            inputs: Optional[Iterable[Address]] = None,
            change_address: Optional[Address] = None,
            security_level: Optional[int] = None,
    ) -> dict:
        """
        Prepares transactions to be broadcast to the Tangle, by
        generating the correct bundle, as well as choosing and signing
        the inputs (for value transfers).

        :param Iterable[ProposedTransaction] transfers:
            Transaction objects to prepare.

        :param Optional[Iterable[Address]] inputs:
            List of addresses used to fund the transfer.
            Ignored for zero-value transfers.

            If not provided, addresses will be selected automatically by
            scanning the Tangle for unspent inputs.  Depending on how
            many transfers you've already sent with your seed, this
            process could take awhile.

        :param Optional[Address] change_address:
            If inputs are provided, any unspent amount will be sent to
            this address.

            If not specified, a change address will be generated
            automatically.

        :param Optional[int] security_level:
            Number of iterations to use when generating new addresses
            (see :py:meth:`get_new_addresses`).

            This value must be between 1 and 3, inclusive.

            If not set, defaults to
            :py:attr:`AddressGenerator.DEFAULT_SECURITY_LEVEL`.

        :return:
            ``dict`` with the following structure::

                {
                    'trytes': List[TransactionTrytes],
                        Raw trytes for the transactions in the bundle,
                        ready to be provided to :py:meth:`send_trytes`.
                }

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#preparetransfers
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().prepare_transfer(
                        transfers,
                        inputs,
                        change_address,
                        security_level,
                )
        )

    def promote_transaction(
            self,
            transaction: TransactionHash,
            depth: int = 3,
            min_weight_magnitude: Optional[int] = None,
    ) -> dict:
        """
        Promotes a transaction by adding spam on top of it.

        :param TransactionHash transaction:
            Transaction hash.  Must be a tail transaction.

        :param int depth:
            Depth at which to attach the bundle.
            Defaults to 3.

        :param Optional[int] min_weight_magnitude:
            Min weight magnitude, used by the node to calibrate Proof of
            Work.

            If not provided, a default value will be used.

        :return:
            ``dict`` with the following structure::

                {
                    'bundle': Bundle,
                        The newly-published bundle.
                }
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().promote_transaction(
                        transaction,
                        depth,
                        min_weight_magnitude,
                )
        )

    def replay_bundle(
            self,
            transaction: TransactionHash,
            depth: int = 3,
            min_weight_magnitude: Optional[int] = None,
    ) -> dict:
        """
        Takes a tail transaction hash as input, gets the bundle
        associated with the transaction and then replays the bundle by
        attaching it to the Tangle.

        :param TransactionHash transaction:
            Transaction hash.  Must be a tail.

        :param int depth:
            Depth at which to attach the bundle.
            Defaults to 3.

        :param Optional[int] min_weight_magnitude:
            Min weight magnitude, used by the node to calibrate Proof of
            Work.

            If not provided, a default value will be used.

        :return:
            ``dict`` with the following structure::

                {
                    'trytes': List[TransactionTrytes],
                        Raw trytes that were published to the Tangle.
                }

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#replaytransfer
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().replay_bundle(
                        transaction,
                        depth,
                        min_weight_magnitude,
                )
        )

    def send_transfer(
            self,
            transfers: Iterable[ProposedTransaction],
            depth: int = 3,
            inputs: Optional[Iterable[Address]] = None,
            change_address: Optional[Address] = None,
            min_weight_magnitude: Optional[int] = None,
            security_level: Optional[int] = None,
    ) -> dict:
        """
        Prepares a set of transfers and creates the bundle, then
        attaches the bundle to the Tangle, and broadcasts and stores the
        transactions.

        :param  Iterable[ProposedTransaction] transfers:
            Transfers to include in the bundle.

        :param int depth:
            Depth at which to attach the bundle.
            Defaults to 3.

        :param Optional[Iterable[Address]] inputs:
            List of inputs used to fund the transfer.
            Not needed for zero-value transfers.

        :param Optional[Address] change_address:
            If inputs are provided, any unspent amount will be sent to
            this address.

            If not specified, a change address will be generated
            automatically.

        :param Optional[int] min_weight_magnitude:
            Min weight magnitude, used by the node to calibrate Proof of
            Work.

            If not provided, a default value will be used.

        :param Optional[int] security_level:
            Number of iterations to use when generating new addresses
            (see :py:meth:`get_new_addresses`).

            This value must be between 1 and 3, inclusive.

            If not set, defaults to
            :py:attr:`AddressGenerator.DEFAULT_SECURITY_LEVEL`.

        :return:
            ``dict`` with the following structure::

                {
                    'bundle': Bundle,
                        The newly-published bundle.
                }

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#sendtransfer
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().send_transfer(
                        transfers,
                        depth,
                        inputs,
                        change_address,
                        min_weight_magnitude,
                        security_level,
                )
        )

    def send_trytes(
            self,
            trytes: Iterable[TransactionTrytes],
            depth: int = 3,
            min_weight_magnitude: Optional[int] = None
    ) -> dict:
        """
        Attaches transaction trytes to the Tangle, then broadcasts and
        stores them.

        :param Iterable[TransactionTrytes] trytes:
            Transaction encoded as a tryte sequence.

        :param int depth:
            Depth at which to attach the bundle.
            Defaults to 3.

        :param Optional[int] min_weight_magnitude:
            Min weight magnitude, used by the node to calibrate Proof of
            Work.

            If not provided, a default value will be used.

        :return:
            ``dict`` with the following structure::

                {
                    'trytes': List[TransactionTrytes],
                        Raw trytes that were published to the Tangle.
                }

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#sendtrytes
        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().send_trytes(
                        trytes,
                        depth,
                        min_weight_magnitude,
                )
        )

    def is_reattachable(self, addresses: Iterable[Address]) -> dict:
        """
        This API function helps you to determine whether you should
        replay a transaction or make a new one (either with the same
        input, or a different one).

        This method takes one or more input addresses (i.e. from spent
        transactions) as input and then checks whether any transactions
        with a value transferred are confirmed.

        If yes, it means that this input address has already been
        successfully used in a different transaction, and as such you
        should no longer replay the transaction.

        :param Iterable[Address] addresses:
            List of addresses.

        :return:
            ``dict`` with the following structure::

                {
                  'reattachable': List[bool],
                    Always a list, even if only one address was queried.
                }

        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().is_reattachable(
                        addresses,
                )
        )

    def traverse_bundle(self, tail_hash: TransactionHash) -> dict:
        """
        Fetches and traverses a bundle from the Tangle given a tail transaction
        hash.
        Recursively traverse the Tangle, collecting transactions until
        we hit a new bundle.

        This method is (usually) faster than :py:meth:`find_transactions`, and
        it ensures we don't collect transactions from replayed bundles.

        :param TransactionHash tail_hash:
            Tail transaction hash of the bundle.

        :return:
            ``dict`` with the following structure::

                {
                  'bundle': List[Bundle],
                        List of matching bundles.  Note that this value is
                        always a list, even if only one bundle was found.
                }

        """
        # Execute original coroutine inside an event loop to make this method
        # synchronous
        return asyncio.get_event_loop().run_until_complete(
                super().traverse_bundle(
                        tail_hash,
                )
        )
