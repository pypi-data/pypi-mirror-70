import secrets
import string
from decimal import Decimal
from typing import Any, Counter, Dict, List, Optional

from bitshares.market import Market
from bitsharesbase.account import PasswordKey


def generate_password(size: int = 53, chars: str = string.ascii_letters + string.digits) -> str:
    """Generate random word with letters and digits."""
    return ''.join(secrets.choice(chars) for x in range(size))


def get_keys_from_password(
    account_name: str, password: str, prefix: str, key_types: Optional[List[str]] = None,
) -> Dict[str, str]:
    """Generates public/private keys from a password."""
    if not key_types:
        key_types = ['active', 'owner', 'memo']

    keys = {}
    for key_type in key_types:
        # PasswordKey object
        passkey = PasswordKey(account_name, password, role=key_type)

        privkey = passkey.get_private_key()
        print('{} private: {}'.format(key_type, str(privkey)))  # we need explicit str() conversion!

        # pubkey with default prefix GPH
        pubkey = passkey.get_public_key()

        # pubkey with correct prefix
        keys[key_type] = format(pubkey, prefix)
        print('{} public: {}\n'.format(key_type, keys[key_type]))

    return keys


def convert_asset(blockchain_instance: Any, from_value: float, from_asset: str, to_asset: str) -> float:
    """Converts asset to another based on the latest market value.

    :param blockchain_instance: graphene-compatible blockchain instance
    :param float from_value: Amount of the input asset
    :param string from_asset: Symbol of the input asset
    :param string to_asset: Symbol of the output asset
    :return: float Asset converted to another asset as float value
    """
    market = Market('{}/{}'.format(from_asset, to_asset), bitshares_instance=blockchain_instance)
    ticker = market.ticker()
    latest_price = ticker.get('latest', {}).get('price', None)
    precision = market['base']['precision']

    return round((from_value * latest_price), precision)


def transform_asset(
    blockchain_instance: Any, sum_balances: Counter[str], from_asset: str, to_asset: str
) -> Counter[str]:
    """In sum_balances dict, convert one asset into another.

    :param blockchain_instance: graphene-compatible blockchain instance
    :param collections.Counter sum_balances: Counter with balances
    :param str from_asset: asset to convert from
    :param str to_asset: destination asset
    """
    if from_asset in sum_balances:
        amount = convert_asset(blockchain_instance, sum_balances[from_asset], from_asset, to_asset)
        sum_balances[from_asset] = 0
        sum_balances[to_asset] += amount  # type: ignore
    return sum_balances


def raw_to_decimal(raw_amount: int, precision: int) -> Decimal:
    """Convert raw amount to Decimal amount.

    :param raw_amount: bitshares amount in int
    :param precision: asset precision
    """
    return Decimal(raw_amount).scaleb(-precision)
