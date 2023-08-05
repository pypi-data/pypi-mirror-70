import datetime
import time
from contextlib import suppress

from funcy import get_in, rpartial, take, walk_values
from toolz import dissoc

from golos.amount import Amount
from golos.blockchain import Blockchain
from golos.converter import Converter
from golos.instance import shared_steemd_instance
from golos.utils import json_expand, parse_time
from golosbase.exceptions import AccountDoesNotExistsException


class Account(dict):
    """
    This class allows to easily access Account data.

    :param str account_name: Name of the account
    :param Steemd steemd_instance: Steemd() instance to use when
        accessing a RPC
    """

    def __init__(self, account_name, steemd_instance=None):
        self.steemd = steemd_instance or shared_steemd_instance()
        self.name = account_name

        # caches
        self._converter = None

        self.refresh()

    def refresh(self):
        account = self.steemd.get_account(self.name)
        if not account:
            raise AccountDoesNotExistsException

        # load json_metadata
        account = json_expand(account, "json_metadata")
        super(Account, self).__init__(account)

    def __getitem__(self, key):
        return super(Account, self).__getitem__(key)

    def items(self):
        return super(Account, self).items()

    @property
    def converter(self):
        if not self._converter:
            self._converter = Converter(self.steemd)
        return self._converter

    @property
    def profile(self):
        with suppress(TypeError):
            return get_in(self, ["json_metadata", "profile"], default={})

    @property
    def sp(self):
        vests = Amount(self["vesting_shares"]).amount
        return round(self.converter.vests_to_sp(vests), 3)

    @property
    def rep(self):
        raise DeprecationWarning("Reputations field was removed from result struct")

    @property
    def balances(self):
        return self.get_balances()

    def get_balances(self):
        available = {
            "GOLOS": Amount(self["balance"]).amount,
            "GBG": Amount(self["sbd_balance"]).amount,
            "GESTS": Amount(self["vesting_shares"]).amount,
        }

        savings = {
            "GOLOS": Amount(self["savings_balance"]).amount,
            "GBG": Amount(self["savings_sbd_balance"]).amount,
        }

        accumulative = {"GOLOS": Amount(self["accumulative_balance"]).amount}

        tip = {"GOLOS": Amount(self["tip_balance"]).amount}

        totals = {
            "GOLOS": sum([available["GOLOS"], savings["GOLOS"], accumulative["GOLOS"], tip["GOLOS"]]),
            "GBG": sum([available["GBG"], savings["GBG"]]),
            "GESTS": sum([available["GESTS"]]),
        }

        total = walk_values(rpartial(round, 3), totals)

        return {
            "available": available,
            "savings": savings,
            "accumulative": accumulative,
            "tip": tip,
            "total": total,
        }

    def voting_power(self):
        return self["voting_power"] / 100

    def get_followers(self, limit: int = None, offset: str = None):
        return [x["follower"] for x in self._get_followers(direction="follower", limit=limit, offset=offset)]

    def get_following(self, limit: int = None, offset: str = None):
        return [x["following"] for x in self._get_followers(direction="following", limit=limit, offset=offset)]

    def _get_followers(self, direction="follower", limit=None, offset=""):
        users = []

        get_users = {"follower": self.steemd.get_followers, "following": self.steemd.get_following}[direction]

        limit = limit or 10 ** 6
        max_request_limit = 100
        left_number = limit

        while left_number > 0:
            select_limit = min(left_number, max_request_limit)
            result = get_users(self.name, offset, "blog", select_limit)
            users.extend(result)

            has_next = len(users) < limit and len(result) >= select_limit
            if has_next:
                if users:
                    del users[-1]
                offset = result[-1][direction]

                left_number = left_number - len(result) + 1
            else:
                left_number = 0

        return users

    def has_voted(self, post):
        active_votes = {v["voter"]: v for v in getattr(post, "active_votes")}
        return self.name in active_votes

    def curation_stats(self):
        trailing_24hr_t = time.time() - datetime.timedelta(hours=24).total_seconds()
        trailing_7d_t = time.time() - datetime.timedelta(days=7).total_seconds()

        reward_24h = 0.0
        reward_7d = 0.0

        for reward in take(5000, self.history_reverse(filter_by="curation_reward")):

            timestamp = parse_time(reward["timestamp"]).timestamp()
            if timestamp > trailing_7d_t:
                reward_7d += Amount(reward["reward"]).amount

            if timestamp > trailing_24hr_t:
                reward_24h += Amount(reward["reward"]).amount

        reward_7d = self.converter.vests_to_sp(reward_7d)
        reward_24h = self.converter.vests_to_sp(reward_24h)
        return {
            "24hr": reward_24h,
            "7d": reward_7d,
            "avg": reward_7d / 7,
        }

    def virtual_op_count(self):
        try:
            last_item = self.steemd.get_account_history(self.name, -1, 0)[0][0]
        except IndexError:
            return 0
        else:
            return last_item

    def get_account_votes(self):
        return self.steemd.get_account_votes(self.name)

    def get_withdraw_routes(self):
        return self.steemd.get_withdraw_routes(self.name, "all")

    def get_conversion_requests(self):
        return self.steemd.get_conversion_requests(self.name)

    @staticmethod
    def filter_by_date(items, start_time, end_time=None):
        start_time = parse_time(start_time).timestamp()
        if end_time:
            end_time = parse_time(end_time).timestamp()
        else:
            end_time = time.time()

        filtered_items = []
        for item in items:
            item_time = None
            if "time" in item:
                item_time = item["time"]
            elif "timestamp" in item:
                item_time = item["timestamp"]

            if item_time:
                timestamp = parse_time(item_time).timestamp()
                if end_time > timestamp > start_time:
                    filtered_items.append(item)

        return filtered_items

    def export(self, load_extras=True):
        """
        This method returns a dictionary that is type-safe to store as JSON or in a database.

        :param bool load_extras: Fetch extra information related to the account (this might take a while).
        """
        extras = dict()
        if load_extras:
            followers = self.get_followers()
            following = self.get_following()
            extras = {
                "followers": followers,
                "followers_count": len(followers),
                "following": following,
                "following_count": len(following),
                "curation_stats": self.curation_stats(),
                "withdrawal_routes": self.get_withdraw_routes(),
                "conversion_requests": self.get_conversion_requests(),
            }

        composed_dict = self.copy()
        composed_dict.update(extras)
        composed_dict.update(
            {"profile": self.profile, "sp": self.sp, "balances": self.get_balances(),}
        )

        return composed_dict

    def get_account_history(self, index, limit, start=None, stop=None, order=-1, filter_by=None, raw_output=False):
        """
        A generator over steemd.get_account_history.

        It offers serialization, filtering and fine grained iteration control.

        Args:
            index (int): start index for get_account_history
            limit (int): How many items in account history will be scanned (any ops, not only filtered)
            start (int): (Optional) skip items until this index
            stop (int): (Optional) stop iteration early at this index
            order: (1, -1): 1 for chronological, -1 for reverse order
            filter_by (str, list): filter out all but these operations
            raw_output (bool): (Defaults to False). If True, return history in
                steemd format (unchanged).
        """
        history = self.steemd.get_account_history(self.name, index, limit)
        for item in history[::order]:
            index, event = item

            # start and stop utilities for chronological generator
            if start and index < start:
                continue

            if stop and index > stop:
                return

            op_type, op = event["op"]
            block_props = dissoc(event, "op")

            def construct_op(account_name):
                # verbatim output from steemd
                if raw_output:
                    return item

                # index can change during reindexing in
                # future hard-forks. Thus we cannot take it for granted.
                immutable = op.copy()
                immutable.update(block_props)
                immutable.update(
                    {"account": account_name, "type": op_type,}
                )
                _id = Blockchain.hash_op(immutable)
                immutable.update(
                    {"_id": _id, "index": index,}
                )
                return immutable

            if filter_by is None:
                yield construct_op(self.name)
            else:
                if type(filter_by) is list:
                    if op_type in filter_by:
                        yield construct_op(self.name)

                if type(filter_by) is str:
                    if op_type == filter_by:
                        yield construct_op(self.name)

    def history(self, filter_by=None, start=0, batch_size=1000, raw_output=False):
        """Stream account history in chronological order."""
        max_index = self.virtual_op_count()
        if not max_index:
            return

        start_index = start + batch_size
        i = start_index
        while i < max_index + batch_size:
            yield from self.get_account_history(
                index=i,
                limit=batch_size,
                start=i - batch_size,
                stop=max_index,
                order=1,
                filter_by=filter_by,
                raw_output=raw_output,
            )
            i += batch_size + 1

    def history_reverse(self, filter_by=None, batch_size=1000, raw_output=False):
        """Stream account history in reverse chronological order."""
        start_index = self.virtual_op_count()
        if not start_index:
            return

        i = start_index
        while i > 0:
            if i - batch_size < 0:
                batch_size = i
            yield from self.get_account_history(
                index=i, limit=batch_size, order=-1, filter_by=filter_by, raw_output=raw_output,
            )
            i -= batch_size + 1

    def rawhistory(self, first=99999999999, limit=-1, only_ops=[], exclude_ops=[]):
        """
        Returns a generator for individual account transactions. The latest operation will be first. This call can be
        used in a ``for`` loop.

        :param str account: account name to get history for
        :param int first: sequence number of the first transaction to return
        :param int limit: limit number of filtered operations to return
        :param array only_ops: Limit generator by these operations
        """
        cnt = 0
        _limit = 100
        if _limit > first:
            _limit = first
        while first > 0:
            # RPC call
            txs = self.steemd.get_account_history(self.name, first, _limit)
            for i in txs[::-1]:
                if exclude_ops and i[1]["op"][0] in exclude_ops:
                    continue
                if not only_ops or i[1]["op"][0] in only_ops:
                    cnt += 1
                    yield i
                    if limit >= 0 and cnt >= limit:
                        break
            if limit >= 0 and cnt >= limit:
                break
            if len(txs) < _limit:
                break
            first = txs[0][0] - 1  # new first
            if _limit > first:
                _limit = first
