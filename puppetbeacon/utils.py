from datetime import datetime, timedelta


def get_timedelta(timestamp):
    try:
        date_object = datetime.fromtimestamp(timestamp)
        time_delta = datetime.now() - date_object
    except TypeError:
        return None
    return int(time_delta.total_seconds())


def percentage(part, whole):
    return 100.0 * part/whole


def safe_get(data, *keys):
    for key in keys:
        try:
            data = data[key]
        except KeyError:
            return None
    return data
