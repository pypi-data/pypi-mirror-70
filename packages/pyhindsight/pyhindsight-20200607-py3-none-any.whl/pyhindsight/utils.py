import datetime
import json
import logging
import pytz
import struct
from pyhindsight import __version__

log = logging.getLogger(__name__)


def format_plugin_output(name, version, items):
    width = 80
    left_side = width * 0.55
    full_plugin_name = "{} (v{})".format(name, version)
    pretty_name = "{name:>{left_width}}:{count:^{right_width}}" \
        .format(name=full_plugin_name, left_width=int(left_side), version=version, count=' '.join(['-', items, '-']),
                right_width=(width - int(left_side) - 2))
    return pretty_name


def format_meta_output(name, content):
    left_side = 17
    pretty_name = "{name:>{left_width}}: {content}" \
        .format(name=name, left_width=int(left_side), content=content)
    return pretty_name


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, buffer):
            return str(obj, encoding='utf-8', errors='replace')
        else:
            return obj.__dict__


def to_epoch(timestamp):
    try:
        timestamp = float(timestamp)
    except:
        return 0
    if timestamp > 99999999999999:
        # Webkit
        return (float(timestamp) / 1000000) - 11644473600
    elif timestamp > 99999999999:
        # Epoch milliseconds
        return float(timestamp) / 1000
    elif timestamp >= 0:
        # Epoch
        return float(timestamp)
    else:
        return 0


def to_datetime(timestamp, timezone=None):
    """Convert a variety of timestamp formats to a datetime object."""

    try:
        if isinstance(timestamp, datetime.datetime):
            return timestamp
        try:
            timestamp = float(timestamp)
        except:
            timestamp = 0

        if 13700000000000000 > timestamp > 12000000000000000:  # 2035 > ts > 1981
            # Webkit
            new_timestamp = datetime.datetime.utcfromtimestamp((float(timestamp) / 1000000) - 11644473600)
        elif 1900000000000 > timestamp > 2000000000:  # 2030 > ts > 1970
            # Epoch milliseconds
            new_timestamp = datetime.datetime.utcfromtimestamp(float(timestamp) / 1000)
        elif 1900000000 > timestamp >= 0:  # 2030 > ts > 1970
            # Epoch
            new_timestamp = datetime.datetime.utcfromtimestamp(float(timestamp))
        else:
            new_timestamp = datetime.datetime.utcfromtimestamp(0)

        if timezone is not None:
            try:
                return new_timestamp.replace(tzinfo=pytz.utc).astimezone(timezone)
            except NameError:
                return new_timestamp
        else:
            return new_timestamp
    except Exception as e:
        print(e)


def friendly_date(timestamp):
    if isinstance(timestamp, (str, int)):
        return to_datetime(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    elif timestamp is None:
        return ''
    else:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def get_ldb_pairs(ldb_path, prefix=''):
    """Open a LevelDB at given path and return a list of all key/value pairs, optionally
    filtered by a prefix string. Key and value are kept as byte strings """

    try:
        import plyvel
    except ImportError:
        log.warning(f' - Failed to import plyvel; unable to process {ldb_path}')
        return []

    # The ldb key and value are both bytearrays, so the prefix must be too. We allow
    # passing the prefix into this function as a string for convenience.
    if isinstance(prefix, str):
        prefix = prefix.encode()

    try:
        db = plyvel.DB(ldb_path, create_if_missing=False)
    except Exception as e:
        log.warning(f' - Couldn\'t open {ldb_path} as LevelDB; {e}')
        return []

    cleaned_pairs = []
    pairs = list(db.iterator())
    for pair in pairs:
        # Each leveldb pair should be a tuple of length 2 (key & value); if not, log it and skip it.
        if not isinstance(pair, tuple) or len(pair) is not 2:
            log.warning(f' - Found LevelDB key/value pair that is not formed as expected ({str(pair)}); skipping.')
            continue

        key, value = pair
        if key.startswith(prefix):
            key = key[len(prefix):]
            cleaned_pairs.append({'key': key, 'value': value})

    return cleaned_pairs


def read_varint(source):
    result = 0
    bytes_used = 0
    for read in source:
        result |= ((read & 0x7F) << (bytes_used * 7))
        bytes_used += 1
        if (read & 0x80) != 0x80:
            return result, bytes_used


def read_string(input_bytes, ptr):
    length = struct.unpack('<i', input_bytes[ptr:ptr+4])[0]
    ptr += 4
    end_ptr = ptr+length
    string_value = input_bytes[ptr:end_ptr]
    while end_ptr % 4 != 0:
        end_ptr += 1

    return string_value.decode(), end_ptr


def read_int32(input_bytes, ptr):
    value = struct.unpack('<i', input_bytes[ptr:ptr + 4])[0]
    return value, ptr + 4


def read_int64(input_bytes, ptr):
    value = struct.unpack('<Q', input_bytes[ptr:ptr + 8])[0]
    return value, ptr + 8


banner = '''
################################################################################

                   _     _           _     _       _     _
                  | |   (_)         | |   (_)     | |   | |
                  | |__  _ _ __   __| |___ _  __ _| |__ | |_
                  | '_ \| | '_ \ / _` / __| |/ _` | '_ \| __|
                  | | | | | | | | (_| \__ \ | (_| | | | | |_
                  |_| |_|_|_| |_|\__,_|___/_|\__, |_| |_|\__|
                                              __/ |
                        by @_RyanBenson      |___/   v{}

################################################################################
'''.format(__version__)
