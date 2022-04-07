#  Copyright (c) 2022. VMware, Inc.
#  SPDX-License-Identifier: Apache-2.0
import hashlib
import pickle

from typing import Any, Callable, Mapping, Sequence

# noinspection PyPackageRequirements
import base58
from multihash import multihash

DELIMITER = ':'

SEPARATOR = ','

JSON_SEPARATORS = (SEPARATOR, DELIMITER)

JSON_ENCODING = 'utf-8'

DEFAULT_ENCODING_FORMAT = 'hex'

DEFAULT_ALGORITHM = hashlib.sha3_256
DEFAULT_CID_ENCODING = 'sha3-256'
DEFAULT_CID_STRING_ENCODING = JSON_ENCODING


class ContentAddressableError(RuntimeError):
    pass


class ContentAlgoError(ContentAddressableError):
    pass


class ContentImplementationError(ContentAddressableError):
    pass


def canonical_form(in_data: Any) -> bytes:
    """
    convert an object of any kind into a canonical form we can use
    for encode/decode and computing a content_identifier.
    """
    return pickle.dumps(in_data)


def content_id(
        in_data: Any,
        algo: Callable = DEFAULT_ALGORITHM,
        encoding: str = DEFAULT_CID_ENCODING,
        length: int = None) -> str:
    """
    Given a dictionary, returns the cryptographic content identifier for
    the dictionary supplied.

    This is a unique identifier in the space of all content.

    :returns: a multihash format string of the contents in canonical format.
    """
    digest = multihash_digest(in_data, algo, encoding)
    if length is None:
        length = len(digest)
    m_hash = multihash.encode(digest, encoding, length)
    return base58.b58encode(m_hash)


def multihash_digest(in_data: Any,
                     algo: Callable = DEFAULT_ALGORITHM,
                     encoding: str = DEFAULT_CID_ENCODING):
    data_bytes = canonical_form(in_data)
    result = algo(data_bytes)
    if not hasattr(result, 'digest'):
        raise ContentAlgoError(
            f'Supplied algorithm {algo} (encoding: {encoding})'
            f'did not return a Hash object with a digest method!')
    digest = result.digest()
    return digest


class Content:
    """
    Content data types can produce Content Identifiers.
    """
    def as_list(self) -> Sequence[Any]:
        """
        Convert this data object into a sequence object.

        (Abstract, you must supply an implementation.
        Suggestion: If this is a single object create a 1 row list.)

        :returns: a sequence representing this object
        """
        raise NotImplementedError('multihash method unimplemented')

    def to_data(self) -> Mapping[Any, Any]:
        """
        Convert this data object into a dictionary object.

        (Abstract, you must supply an implementation.
        Suggestion: if this is a sequence create a dictionary with key 'rows')

        :returns: A Dictionary representing this object.
        """
        raise NotImplementedError('multihash method unimplemented')

    def multihash(self) -> str:
        """
        Aka the content identifier of the object in multihash format.

        This is the synthetic primary key we will use to find this
        exact data object again in the future.

        See:
            content_id method in guci.core

        :returns: a multihash string of the content id for this document.
        """
        return multihash_digest(self.to_data())

    def cid(self) -> str:
        """
        Content Identifiers are a self-describing content addressed identifier
        that uses cryptographic hashes to achieve addressing based on the
        contents of a data object.

        :returns: an object of CIDv0 or CIDv1 from the py-cid package
        """
        return content_id(self.to_data())

    def __str__(self) -> str:
        return self.cid().__str__()
