# coding=utf-8
import logging
from typing import Any, List, Set, Union

from funcy import first

from golos.block import Block
from golos.consts import *
from golos.utils import resolve_identifier
from golosbase.chains import known_chains
from golosbase.connector import Connector
from golosbase.storage import configStorage
from golosbase.transactions import SignedTransaction
from golosbase.types import PointInTime

logger = logging.getLogger(__name__)

# DATABASE_API = 'database_api'
#   Doesn't exist
#       get_reward_fund
#       get_comment_discussions_by_payout
#       get_post_discussions_by_payout
#       get_state
#       get_account_references
#       get_liquidity_queue


def get_config_node_list():
    nodes = configStorage.get("nodes", None)
    if nodes:
        return nodes.split(",")


class Steemd(Connector):
    """
    Connect to the Steem network.

    Args:
        nodes (list): A list of Steem HTTP RPC nodes to connect to. If not provided, official Steemit nodes will be used.

    Returns:
        Steemd class instance. It can be used to execute commands against steem node.

    Example:

       If you would like to override the official Steemit nodes (default), you can pass your own.
       When currently used node goes offline, ``Steemd`` will automatically fail-over to the next available node.

       .. code-block:: python

           nodes = [
               'https://steemd.yournode1.com',
               'https://steemd.yournode2.com',
           ]

           s = Steemd(nodes)
    """

    def __init__(self, nodes=None, **kwargs):
        if not nodes:
            nodes = get_config_node_list() or ["https://ws.golos.io"]

        if isinstance(nodes, str):
            nodes = [nodes]

        super(Steemd, self).__init__(nodes, **kwargs)

    @property
    def chain_params(self):
        """
        Identify the connected network.

        This call returns a dictionary with keys chain_id, prefix, and other chain specific settings
        """
        props = self.get_dynamic_global_properties()
        chain = props["current_supply"].split(" ")[1]
        assert chain in known_chains, "The chain you are connecting to is not supported"
        return known_chains.get(chain)

    def get_posts(self, limit=10, sort="hot", category=None, start=None):
        """
        Get multiple posts in an array.

        :param int limit: Limit the list of posts by ``limit``
        :param str sort: Sort the list by "recent" or "payout"
        :param str category: Only show posts in this category
        :param str start: Show posts after this post. Takes an
                          identifier of the form ``@author/permlink``
        """
        from golos.post import Post

        discussion_query = {
            "tag": category,
            "limit": limit,
        }
        if start:
            author, permlink = resolve_identifier(start)
            discussion_query["start_author"] = author
            discussion_query["start_permlink"] = permlink

        if sort not in ["trending", "created", "active", "cashout", "payout", "votes", "children", "hot"]:
            raise Exception("Invalid choice of '--sort'!")

        func = getattr(self, "get_discussions_by_%s" % sort)
        r = []
        for p in func(discussion_query):
            r.append(Post(p, steemd_instance=self))
        return r

    def stream_comments(self, *args, **kwargs):
        """
        Generator that yields posts when they come in.

        To be used in a for loop that returns an instance of `Post()`.
        """
        from golos.blockchain import Blockchain
        from golos.post import Post

        for c in Blockchain(mode=kwargs.get("mode", "irreversible"), steemd_instance=self,).stream(
            "comment", *args, **kwargs
        ):
            yield Post(c, steemd_instance=self)

    @property
    def last_irreversible_block_num(self):
        """Newest irreversible block number."""
        return self.get_dynamic_global_properties()["last_irreversible_block_num"]

    @property
    def head_block_number(self):
        """Newest block number."""
        return self.get_dynamic_global_properties()["head_block_number"]

    def get_account(self, account):
        """
        Lookup account information such as user profile, public keys, balances, etc.

        Args:
            account (str): STEEM username that we are looking up.

        Returns:
            dict: Account information.
        """
        return first(self.call("get_accounts", [account], api=DATABASE_API))

    def get_all_usernames(self, last_user=""):
        """Fetch the full list of STEEM usernames."""
        usernames = self.lookup_accounts(last_user, 1000)
        batch = []
        while len(batch) != 1:
            batch = self.lookup_accounts(usernames[-1], 1000)
            usernames += batch[1:]

        return usernames

    def _get_blocks(self, blocks: Union[List[int], Set[int]]):
        """
        Fetch multiple blocks from steemd at once.

        Warning: This method does not ensure that all blocks are returned,
        or that the results are ordered.  You will probably want to use
        `steemd.get_blocks()` instead.

        Args:
            blocks (list): A list, or a set of block numbers.

        Returns:
            A generator with results.
        """
        results = self.call_multi_with_futures("get_block", blocks, api=DATABASE_API, max_workers=10)
        return ({**x, "block_num": int(x["previous"][:8], base=16) + 1} for x in results if x)

    def get_blocks(self, block_nums: List[int]):
        """
        Fetch multiple blocks from steemd at once, given a range.

        Args:
            block_nums (list): A list of all block numbers we would like to tech.

        Returns:
            dict: An ensured and ordered list of all `get_block` results.
        """
        required = set(block_nums)
        available = set()
        missing = required - available
        blocks = {}

        while missing:
            for block in self._get_blocks(missing):
                blocks[block["block_num"]] = block

            available = set(blocks.keys())
            missing = required - available

        return [blocks[x] for x in block_nums]

    def get_blocks_range(self, start: int, end: int):
        """
        Fetch multiple blocks from steemd at once, given a range.

        Args:
            start (int): The number of the block to start with
            end (int): The number of the block at the end of the range. Not included in results.

        Returns:
            dict: An ensured and ordered list of all `get_block` results.
        """
        return self.get_blocks(list(range(start, end)))

    def get_reward_fund(self, fund_name: str = "post"):
        raise DeprecationWarning("This method not supported!")

    def get_expiring_vesting_delegations(self, account: str, from_time: PointInTime, limit: int = 100):
        return self.call("get_expiring_vesting_delegations", account, from_time, limit, api=DATABASE_API)

    def get_trending_tags(self, after_tag, limit):
        """get_trending_tags."""
        return self.call("get_trending_tags", after_tag, limit, api=TAGS_API)

    def get_tags_used_by_author(self, account: str):
        """get_tags_used_by_author."""
        return self.call("get_tags_used_by_author", account, api=TAGS_API)

    def get_discussions_by_trending(self, discussion_query):
        """get_discussions_by_trending."""
        return self.call("get_discussions_by_trending", discussion_query, api=TAGS_API)

    def get_comment_discussions_by_payout(self, discussion_query):
        raise DeprecationWarning("This method not supported!")

    def get_post_discussions_by_payout(self, discussion_query):
        raise DeprecationWarning("This method not supported!")

    def get_discussions_by_created(self, discussion_query):
        """get_discussions_by_created."""
        return self.call("get_discussions_by_created", discussion_query, api=TAGS_API)

    def get_discussions_by_active(self, discussion_query):
        """get_discussions_by_active."""
        return self.call("get_discussions_by_active", discussion_query, api=TAGS_API)

    def get_discussions_by_cashout(self, discussion_query):
        """get_discussions_by_cashout."""
        return self.call("get_discussions_by_cashout", discussion_query, api=TAGS_API)

    def get_discussions_by_payout(self, discussion_query):
        """get_discussions_by_payout."""
        return self.call("get_discussions_by_payout", discussion_query, api=TAGS_API)

    def get_discussions_by_votes(self, discussion_query):
        """get_discussions_by_votes."""
        return self.call("get_discussions_by_votes", discussion_query, api=TAGS_API)

    def get_discussions_by_children(self, discussion_query):
        """get_discussions_by_children."""
        return self.call("get_discussions_by_children", discussion_query, api=TAGS_API)

    def get_discussions_by_hot(self, discussion_query):
        """get_discussions_by_hot."""
        return self.call("get_discussions_by_hot", discussion_query, api=TAGS_API)

    def get_discussions_by_feed(self, discussion_query):
        """get_discussions_by_feed."""
        return self.call("get_discussions_by_feed", discussion_query, api=TAGS_API)

    def get_discussions_by_blog(self, discussion_query):
        """get_discussions_by_blog."""
        return self.call("get_discussions_by_blog", discussion_query, api=TAGS_API)

    def get_discussions_by_comments(self, discussion_query):
        """get_discussions_by_comments."""
        return self.call("get_discussions_by_comments", discussion_query, api=TAGS_API)

    def get_discussions_by_promoted(self, discussion_query):
        """get_discussions_by_promoted."""
        return self.call("get_discussions_by_promoted", discussion_query, api=TAGS_API)

    def get_block_header(self, block_num):
        """
        Get block headers, given a block number.

        Args:
           block_num (int): Block number.

        Returns:
           dict: Block headers in a JSON compatible format.

        Example:

            .. code-block:: python

               s.get_block_headers(8888888)

            ::

                {'extensions': [],
                 'previous': '0087a2372163ff5c5838b09589ce281d5a564f66',
                 'timestamp': '2017-01-29T02:47:33',
                 'transaction_merkle_root': '4ddc419e531cccee6da660057d606d11aab9f3a5',
                 'witness': 'chainsquad.com'}
        """
        return self.call("get_block_header", block_num, api=DATABASE_API)

    def get_block(self, block_num: int):
        """
        Get the full block, transactions and all, given a block number.

        Args:
            block_num (int): Block number.

        Returns:
            dict: Block in a JSON compatible format.

        Example:

            .. code-block:: python

               s.get_block(8888888)

            ::

                {'extensions': [],
                 'previous': '0087a2372163ff5c5838b09589ce281d5a564f66',
                 'timestamp': '2017-01-29T02:47:33',
                 'transaction_merkle_root': '4ddc419e531cccee6da660057d606d11aab9f3a5',
                 'transactions': [{'expiration': '2017-01-29T02:47:42',
                   'extensions': [],
                   'operations': [['comment',
                     {'author': 'hilarski',
                      'body': 'https://media.giphy.com/media/RAx4Xwh1OPHji/giphy.gif',
                      'json_metadata': '{"tags":["motocross"],"image":["https://media.giphy.com/media/RAx4Xwh1OPHji/giphy.gif"],"app":"steemit/0.1"}',
                      'parent_author': 'b0y2k',
                      'parent_permlink': 'ama-supercross-round-4-phoenix-2017',
                      'permlink': 're-b0y2k-ama-supercross-round-4-phoenix-2017-20170129t024725575z',
                      'title': ''}]],
                   'ref_block_num': 41495,
                   'ref_block_prefix': 2639073901,
                   'signatures': ['2058b69f4c15f704a67a7b5a7996a9c9bbfd39c639f9db19b99ecad8328c4ce3610643f8d1b6424c352df120614cd535cd8f2772fce68814eeea50049684c37d69']}],
                 'witness': 'chainsquad.com',
                 'witness_signature': '1f115745e3f6fee95124164f4b57196c0eda2a700064faa97d0e037d3554ee2d5b618e6bfd457473783e8b8333724ba0bf93f0a4a7026e7925c8c4d2ba724152d4'}
        """
        return self.call("get_block", block_num, api=DATABASE_API)

    def get_ops_in_block(self, block_num, virtual_only):
        """get_ops_in_block."""
        return self.call("get_ops_in_block", block_num, virtual_only, api=OPERATION_HISTORY_API)

    def get_state(self, path):
        raise DeprecationWarning("This method not supported!")

    def get_config(self):
        """Get internal chain configuration."""
        return self.call("get_config", api=DATABASE_API)

    def get_dynamic_global_properties(self):
        """get_dynamic_global_properties."""
        return self.call("get_dynamic_global_properties", api=DATABASE_API)

    def get_chain_properties(self):
        """ Get witness elected chain properties.

        ::

            {'account_creation_fee': '30.000 STEEM',
             'maximum_block_size': 65536,
             'sbd_interest_rate': 250}

        """
        return self.call("get_chain_properties", api=DATABASE_API)

    def get_feed_history(self):
        """ Get the hourly averages of witness reported STEEM/SBD prices.

        ::

            {'current_median_history': {'base': '0.093 SBD', 'quote': '1.010 STEEM'},
             'id': 0,
             'price_history': [{'base': '0.092 SBD', 'quote': '1.010 STEEM'},
              {'base': '0.093 SBD', 'quote': '1.020 STEEM'},
              {'base': '0.093 SBD', 'quote': '1.010 STEEM'},
              {'base': '0.094 SBD', 'quote': '1.020 STEEM'},
              {'base': '0.093 SBD', 'quote': '1.010 STEEM'},

        """
        return self.call("get_feed_history", api=WITNESS_API)

    def get_current_median_history_price(self):
        """
        Get the average STEEM/SBD price.

        This price is based on moving average of witness reported price feeds.

        ::

            {'base': '0.093 SBD', 'quote': '1.010 STEEM'}
        """
        return self.call("get_current_median_history_price", api=WITNESS_API)

    def get_miner_queue(self):
        """get_miner_queue."""
        return self.call("get_miner_queue", api=WITNESS_API)

    def get_witness_schedule(self):
        """get_witness_schedule."""
        return self.call("get_witness_schedule", api=WITNESS_API)

    def get_hardfork_version(self):
        """
        Get the current version of the chain.

        Note:
            This is not the same as latest minor version.
        """
        return self.call("get_hardfork_version", api=DATABASE_API)

    def get_next_scheduled_hardfork(self):
        """get_next_scheduled_hardfork."""
        return self.call("get_next_scheduled_hardfork", api=DATABASE_API)

    def get_accounts(self, account_names: list):
        """
        Lookup account information such as user profile, public keys, balances, etc.

        This method is same as ``get_account``, but supports querying for multiple accounts at the time.
        """
        return self.call("get_accounts", account_names, api=DATABASE_API)

    def get_account_references(self, account_id: int):
        raise DeprecationWarning("This method not supported!")

    def lookup_account_names(self, account_names: list):
        """lookup_account_names."""
        return self.call("lookup_account_names", account_names, api=DATABASE_API)

    def lookup_accounts(self, after, limit):
        """
        Get a list of usernames from all registered accounts.

        Args:
            after (str, int): Username to start with. If '', 0 or -1, it will start at beginning.
            limit (int): How many results to return.

        Returns:
            list: List of usernames in requested chunk.
        """
        return self.call("lookup_accounts", after, limit, api=DATABASE_API)

    def get_account_count(self):
        """How many accounts are currently registered on STEEM?"""
        return self.call("get_account_count", api=DATABASE_API)

    def get_conversion_requests(self, account: str):
        """get_conversion_requests."""
        return self.call("get_conversion_requests", account, api=DATABASE_API)

    def get_account_history(self, account: str, index_from: int, limit: int):
        """
        History of all operations for a given account.

        Args:
           account (str): STEEM username that we are looking up.
           index_from (int): The highest database index we take as a starting point.
           limit (int): How many items are we interested in.

        Returns:
           list: List of operations.

        Example:
           To get the latest (newest) operations from a given user ``furion``, we should set the ``index_from`` to -1.
           This is the same as saying `give me the highest index there is`.

           .. code-block :: python

              s.get_account_history('furion', index_from=-1, limit=3)

           This will yield 3 recent operations like so:

           ::

              [[69974,
                {'block': 9941972,
                 'op': ['vote',
                  {'author': 'breezin',
                   'permlink': 'raising-children-is-not-childsplay-pro-s-and-con-s-of-being-a-young-parent',
                   'voter': 'furion',
                   'weight': 900}],
                 'op_in_trx': 0,
                 'timestamp': '2017-03-06T17:09:48',
                 'trx_id': '87f9176faccc7096b5ffb5d12bfdb41b3c0b2955',
                 'trx_in_block': 5,
                 'virtual_op': 0}],
               [69975,
                {'block': 9942005,
                 'op': ['curation_reward',
                  {'comment_author': 'leongkhan',
                   'comment_permlink': 'steem-investor-report-5-march-2017',
                   'curator': 'furion',
                   'reward': '112.397602 VESTS'}],
                 'op_in_trx': 1,
                 'timestamp': '2017-03-06T17:11:30',
                 'trx_id': '0000000000000000000000000000000000000000',
                 'trx_in_block': 5,
                 'virtual_op': 0}],
               [69976,
                {'block': 9942006,
                 'op': ['vote',
                  {'author': 'ejhaasteem',
                   'permlink': 'life-of-fishermen-in-aceh',
                   'voter': 'furion',
                   'weight': 100}],
                 'op_in_trx': 0,
                 'timestamp': '2017-03-06T17:11:30',
                 'trx_id': '955018ac8efe298bd90b45a4fbd15b9df7e00be4',
                 'trx_in_block': 7,
                 'virtual_op': 0}]]

           If we want to query for a particular range of indexes, we need to consider both `index_from` and `limit` fields.
           Remember, `index_from` works backwards, so if we set it to 100, we will get items `100, 99, 98, 97...`.

           For example, if we'd like to get the first 100 operations the user did, we would write:

           .. code-block:: python

              s.get_account_history('furion', index_from=100, limit=100)

           We can get the next 100 items by running:

           .. code-block:: python

              s.get_account_history('furion', index_from=200, limit=100)
        """
        return self.call("get_account_history", account, index_from, limit, api=ACCOUNT_HISTORY_API)

    def get_owner_history(self, account: str):
        """get_owner_history."""
        return self.call("get_owner_history", account, api=DATABASE_API)

    def get_recovery_request(self, account: str):
        """get_recovery_request."""
        return self.call("get_recovery_request", account, api=DATABASE_API)

    def get_escrow(self, from_account: str, escrow_id: int):
        """get_escrow."""
        return self.call("get_escrow", from_account, escrow_id, api=DATABASE_API)

    def get_withdraw_routes(self, account: str, withdraw_route_type: str):
        """get_withdraw_routes."""
        return self.call("get_withdraw_routes", account, withdraw_route_type, api=DATABASE_API)

    def get_account_bandwidth(self, account: str, bandwidth_type: object):
        """get_account_bandwidth."""
        return self.call("get_account_bandwidth", account, bandwidth_type, api=DATABASE_API)

    def get_savings_withdraw_from(self, account: str):
        """get_savings_withdraw_from."""
        return self.call("get_savings_withdraw_from", account, api=DATABASE_API)

    def get_savings_withdraw_to(self, account: str):
        """get_savings_withdraw_to."""
        return self.call("get_savings_withdraw_to", account, api=DATABASE_API)

    def get_order_book(self, limit):
        """
        Get the internal market order book.

        This method will return both bids and asks.

        Args:
            limit (int): How many levels deep into the book to show.

        Returns:
            dict: Order book.

        Example:

            .. code-block:: python

               s.get_order_book(2)

            Outputs:

            ::

                {'asks': [{'created': '2017-03-06T21:29:54',
                   'order_price': {'base': '513.571 GOLOS', 'quote': '50.000 GBG'},
                   'real_price': '0.09735752213423265',
                   'gbg': 50000,
                   'golos': 513571},
                  {'created': '2017-03-06T21:01:39',
                   'order_price': {'base': '63.288 GOLOS', 'quote': '6.204 GBG'},
                   'real_price': '0.09802806219188472',
                   'gbg': 6204,
                   'golos': 63288}],
                 'bids': [{'created': '2017-03-06T21:29:51',
                   'order_price': {'base': '50.000 GBG', 'quote': '516.503 GOLOS'},
                   'real_price': '0.09680485882947436',
                   'gbg': 50000,
                   'golos': 516503},
                  {'created': '2017-03-06T17:30:24',
                   'order_price': {'base': '36.385 GBG', 'quote': '379.608 GOLOS'},
                   'real_price': '0.09584887568228277',
                   'gbg': 36385,
                   'golos': 379608}]}
        """
        return self.call("get_order_book", limit, api=MARKET_HISTORY_API)

    def get_open_orders(self, account: str):
        """
        get_open_orders. Also this api methods exist in DATABASE_API.

        Example:

        ::

            [{'id': 265808,
              'created': '2018-12-23T12:14:15',
              'expiration': '2018-12-30T12:14:14',
              'seller': 'vvk',
              'orderid': 490504533,
              'for_sale': 1000,
              'sell_price': {'base': '1.000 GOLOS', 'quote': '1.200 GBG'},
              'real_price': '1.19999999999999996',
              'rewarded': False}]
        """
        return self.call("get_open_orders", account, api=MARKET_HISTORY_API)

    def get_liquidity_queue(self, start_account: str, limit: int):
        raise DeprecationWarning("This method not supported!")

    def get_transaction_hex(self, signed_transaction: SignedTransaction):
        """get_transaction_hex."""
        return self.call("get_transaction_hex", signed_transaction, api=DATABASE_API)

    def get_transaction(self, transaction_id: str):
        """get_transaction."""
        return self.call("get_transaction", transaction_id, api=OPERATION_HISTORY_API)

    def get_required_signatures(self, signed_transaction: SignedTransaction, available_keys: list):
        """get_required_signatures."""
        return self.call("get_required_signatures", signed_transaction, available_keys, api=DATABASE_API)

    def get_potential_signatures(self, signed_transaction: SignedTransaction):
        """get_potential_signatures."""
        return self.call("get_potential_signatures", signed_transaction, api=DATABASE_API)

    def verify_authority(self, signed_transaction: SignedTransaction):
        """verify_authority."""
        return self.call("verify_authority", signed_transaction, api=DATABASE_API)

    def verify_account_authority(self, account: str, keys: list):
        """verify_account_authority."""
        return self.call("verify_account_authority", account, keys, api=DATABASE_API)

    def get_active_votes(self, author: str, permlink: str, vote_limit: int = 10000):
        """
        Get all votes for the given post.

        Args:
            author (str): OP's STEEM username.
            permlink (str): Post identifier following the username. It looks like slug-ified title.

        Returns:
            list: List of votes.

        Example:
            .. code-block:: python

               s.get_active_votes('mynameisbrian', 'steemifying-idioms-there-s-no-use-crying-over-spilt-milk')

            Output:

            ::

               [{'percent': 10000,
                 'reputation': '36418980678',
                 'rshares': 356981288,
                 'time': '2017-03-06T20:04:18',
                 'voter': 'dailystuff',
                 'weight': '2287202760855'},
                 ...
                {'percent': 10000,
                 'reputation': 3386400109,
                 'rshares': 364252169,
                 'time': '2017-03-06T19:32:45',
                 'voter': 'flourish',
                 'weight': '2334690471157'}]
        """
        return self.call("get_active_votes", author, permlink, vote_limit, api=SOCIAL_NETWORK_API)

    def get_account_votes(self, account, votes_from: int = 0, vote_limit: int = 10000):
        """
        All votes the given account ever made.

        Returned votes are in the following format:
        ::

           {'authorperm': '@alwaysfelicia/time-line-of-best-times-to-post-on-steemit-mystery-explained',
           'percent': 100,
           'rshares': 709227399,
           'time': '2016-08-07T16:06:24',
           'weight': '3241351576115042'},


        Args:
            account (str): STEEM username that we are looking up.
            votes_from (int): starting index
            vote_limit (int): limit of returned votes

        Returns:
            list: List of votes.
        """
        return self.call("get_account_votes", account, votes_from, vote_limit, api=SOCIAL_NETWORK_API)

    def get_content(self, author: str, permlink: str, vote_limit: int = 10000):
        """get_content."""
        return self.call("get_content", author, permlink, vote_limit, api=SOCIAL_NETWORK_API)

    def get_post(self, identifier):
        """
        Get the full content of a post.

        :param str identifier: Identifier for the post to upvote Takes
                               the form ``@author/permlink``
        """
        from golos.post import Post

        return Post(identifier, steemd_instance=self)

    def get_content_replies(self, author: str, permlink: str, vote_limit: int = 10000):
        """get_content_replies."""
        return self.call("get_content_replies", author, permlink, vote_limit, api=SOCIAL_NETWORK_API)

    def get_all_content_replies(self, author: str, permlink: str, vote_limit: int = 10000):
        """get all content replies."""
        return self.call("get_all_content_replies", author, permlink, vote_limit, api=SOCIAL_NETWORK_API)

    def get_discussions_by_author_before_date(
        self, author: str, start_permlink: str, before_date: PointInTime, limit: int, vote_limit: int = 10000
    ):
        """get_discussions_by_author_before_date."""
        return self.call(
            "get_discussions_by_author_before_date",
            author,
            start_permlink,
            before_date,
            limit,
            vote_limit,
            api=SOCIAL_NETWORK_API,
        )

    def get_trending_categories(self, after: str, limit: int):
        """get trending categories."""
        return self.call("get_trending_categories", after, limit, api=SOCIAL_NETWORK_API)

    def get_active_categories(self, after: str, limit: int):
        """get active categories."""
        return self.call("get_active_categories", after, limit, api=SOCIAL_NETWORK_API)

    def get_recent_categories(self, after: str, limit: int):
        """get recent categories."""
        return self.call("get_recent_categories", after, limit, api=SOCIAL_NETWORK_API)

    def get_best_categories(self, after: str, limit: int):
        """get best categories."""
        return self.call("get_best_categories", after, limit, api=SOCIAL_NETWORK_API)

    def get_languages(self):
        """get languages."""
        return self.call("get_languages", api=TAGS_API)

    def get_replies_by_last_update(self, account: str, start_permlink: str, limit: int, vote_limit: int = 10000):
        """get_replies_by_last_update."""
        return self.call(
            "get_replies_by_last_update", account, start_permlink, limit, vote_limit, api=SOCIAL_NETWORK_API
        )

    def get_witnesses(self, witness_ids: list):
        """get_witnesses."""
        return self.call("get_witnesses", witness_ids, api=WITNESS_API)

    def get_witness_by_account(self, account: str):
        """get_witness_by_account."""
        return self.call("get_witness_by_account", account, api=WITNESS_API)

    def get_witnesses_by_vote(self, from_account: str, limit: int):
        """get_witnesses_by_vote."""
        return self.call("get_witnesses_by_vote", from_account, limit, api=WITNESS_API)

    def lookup_witness_accounts(self, from_account: str, limit: int):
        """lookup_witness_accounts."""
        return self.call("lookup_witness_accounts", from_account, limit, api=WITNESS_API)

    def get_witness_count(self):
        """get_witness_count."""
        return self.call("get_witness_count", api=WITNESS_API)

    def get_active_witnesses(self):
        """Get a list of currently active witnesses."""
        return self.call("get_active_witnesses", api=WITNESS_API)

    def get_vesting_delegations(
        self, account: str, from_account: str, limit: int = 100, delegation_type: str = "delegated"
    ):
        """get_vesting_delegations."""
        return self.call("get_vesting_delegations", account, from_account, limit, delegation_type, api=DATABASE_API)

    def login(self, username: str, password: str):
        raise DeprecationWarning("This method not supported!")

    def get_api_by_name(self, api_name: str):
        raise DeprecationWarning("This method not supported!")

    def get_version(self):
        raise DeprecationWarning("This method not supported!")

    def get_followers(self, account: str, start_follower: str, follow_type: str, limit: int):
        """get_followers."""
        return self.call("get_followers", account, start_follower, follow_type, limit, api=FOLLOW_API)

    def get_following(self, account: str, start_follower: str, follow_type: str, limit: int):
        """get_following."""
        return self.call("get_following", account, start_follower, follow_type, limit, api=FOLLOW_API)

    def get_follow_count(self, account: str):
        """get_follow_count."""
        return self.call("get_follow_count", account, api=FOLLOW_API)

    def get_feed_entries(self, account: str, entry_id: int, limit: int):
        """get_feed_entries."""
        return self.call("get_feed_entries", account, entry_id, limit, api=FOLLOW_API)

    def get_feed(self, account: str, entry_id: int, limit: int):
        """get_feed."""
        return self.call("get_feed", account, entry_id, limit, api=FOLLOW_API)

    def get_blog_entries(self, account: str, entry_id: int, limit: int):
        """get_blog_entries."""
        return self.call("get_blog_entries", account, entry_id, limit, api=FOLLOW_API)

    def get_blog(self, account: str, entry_id: int, limit: int):
        """get_blog."""
        return self.call("get_blog", account, entry_id, limit, api=FOLLOW_API)

    def get_account_reputations(self, accounts: Union[List[str], str], limit: int):
        """get_account_reputations."""
        if not isinstance(accounts, (list, tuple)):
            accounts = [accounts]
        return self.call("get_account_reputations", accounts, api=FOLLOW_API)

    def get_reblogged_by(self, author: str, permlink: str):
        """get_reblogged_by."""
        return self.call("get_reblogged_by", author, permlink, api=FOLLOW_API)

    def get_blog_authors(self, blog_account: str):
        """get_blog_authors."""
        return self.call("get_blog_authors", blog_account, api=FOLLOW_API)

    def broadcast_transaction(self, signed_transaction: SignedTransaction):
        """broadcast_transaction."""
        return self.call("broadcast_transaction", signed_transaction, api=NETWORK_BROADCAST_API)

    def broadcast_transaction_synchronous(self, signed_transaction: SignedTransaction):
        """broadcast_transaction_synchronous."""
        return self.call("broadcast_transaction_synchronous", signed_transaction, api=NETWORK_BROADCAST_API)

    def broadcast_block(self, block: Block):
        """broadcast_block."""
        return self.call("broadcast_block", block, api=NETWORK_BROADCAST_API)

    def set_max_block_age(self, max_block_age: int):
        raise DeprecationWarning("This method not supported!")

    def get_ticker(self):
        """Returns the market ticker for the internal SBD:STEEM market."""
        return self.call("get_ticker", api=MARKET_HISTORY_API)

    def get_volume(self):
        """Returns the market volume for the past 24 hours."""
        return self.call("get_volume", api=MARKET_HISTORY_API)

    def get_trade_history(self, start: PointInTime, end: PointInTime, limit: int):
        """Returns the trade history for the internal SBD:STEEM market."""
        return self.call("get_trade_history", start, end, limit, api=MARKET_HISTORY_API)

    def get_recent_trades(self, limit: int) -> List[Any]:
        """Returns the N most recent trades for the internal GBG:GOLOS market."""
        return self.call("get_recent_trades", limit, api=MARKET_HISTORY_API)

    def get_market_history(self, bucket_seconds: int, start: PointInTime, end: PointInTime):
        """Returns the market history for the internal SBD:STEEM market."""
        return self.call("get_market_history", bucket_seconds, start, end, api=MARKET_HISTORY_API)

    def get_market_history_buckets(self):
        """Returns the bucket seconds being tracked by the plugin."""
        return self.call("get_market_history_buckets", api=MARKET_HISTORY_API)

    def get_key_references(self, public_keys: List[str]):
        """get_key_references."""
        if type(public_keys) == str:
            public_keys = [public_keys]
        return self.call("get_key_references", public_keys, api=ACCOUNT_BY_KEY_API)

    def get_raw_block(self, block: int):
        """get raw block."""
        return self.call("get_raw_block", block, api=RAW_BLOCK_API)

    def get_inbox(self, to: str, newest: str, limit: int, offset: int):
        """
        get inbox messages.

        :param to: <skip>
        :param newest: ISO-formatted datetime string, for example: datetime.utcnow().isoformat()
        :param limit: limit of the return data
        """
        return self.call("get_inbox", to, newest, limit, offset, api=PRIVATE_MESSAGE_API)

    def get_outbox(self, fr: str, newest: str, limit: int, offset: int):
        """
        get outbox messages.

        :param fr: <skip>
        :param newest: ISO-formatted datetime string, for example: datetime.utcnow().isoformat()
        :param limit: limit of the return data
        :return:
        """
        return self.call("get_outbox", fr, newest, limit, offset, api=PRIVATE_MESSAGE_API)

    def get_block_info(self, start: int, count: int):
        """get block info."""
        return self.call("get_block_info", start, count, api=BLOCK_INFO_API)

    def get_blocks_with_info(self, start: int, count: int):
        """get blocks with info."""
        return self.call("get_blocks_with_info", start, count, api=BLOCK_INFO_API)

    def get_proposed_transaction(self, account: str) -> list:
        """get_proposed_transaction."""
        return self.call("get_proposed_transaction", account, api=DATABASE_API)

    def get_database_info(self):
        """get_database_info."""
        return self.call("get_database_info", api=DATABASE_API)


if __name__ == "__main__":
    s = Steemd()
    print(s.get_account_count())
