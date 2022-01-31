# -*- coding: utf-8 -*-

import alfred
import calendar
from delorean import utcnow, parse, epoch

def get_timezone():
    tz = alfred.env_arg('timezone')
    if not tz:
        tz = 'UTC'
    return tz

def process(query_str):
    """ Entry point """
    value = parse_query_value(query_str)
    if value is not None:
        results = alfred_items_for_value(value)
        xml = alfred.xml(results) # compiles the XML answer
        alfred.write(xml) # writes the XML back to Alfred

def parse_query_value(query_str):
    """ Return value for the query string """
    try:
        query_str = str(query_str).strip('"\' ')
        if query_str == 'now':
            d = utcnow()
        else:
            # Parse datetime string or timestamp
            try:
                d = epoch(float(query_str))
            except ValueError:
                d = parse(str(query_str), get_timezone())
    except (TypeError, ValueError):
        d = None
    return d

def alfred_items_for_value(value):
    """
    Given a delorean datetime object, return a list of
    alfred items for each of the results
    """

    index = 0
    results = []

    # First item as timestamp
    item_value = calendar.timegm(value.datetime.utctimetuple())
    results.append(alfred.Item(
        title=str(item_value),
        subtitle=u'UTC Timestamp',
        attributes={
            'uid': alfred.uid(index), 
            'arg': item_value,
        },
        icon='icon.png',
    ))
    index += 1

    # Various formats
    tz = get_timezone()
    formats = [
        # 1937-01-01 12:00:27
        ("%Y-%m-%d %H:%M:%S", tz),
        # 19 May 2002 15:21:36
        ("%d %b %Y %H:%M:%S", tz),
        # Sun, 19 May 2002 15:21:36
        ("%a, %d %b %Y %H:%M:%S", tz),
        # 1937-01-01T12:00:27
        ("%Y-%m-%dT%H:%M:%S", tz),
        # 1996-12-19T16:39:57-0800
        ("%Y-%m-%dT%H:%M:%S%z", tz),
    ]
    for format, description in formats:
        tz_value = value
        if description:
            tz_value = value.shift(description)
        item_value = tz_value.datetime.strftime(format)
        results.append(alfred.Item(
            title=str(item_value),
            subtitle=description,
            attributes={
                'uid': alfred.uid(index), 
                'arg': item_value,
            },
        icon='icon.png',
        ))
        index += 1

    return results

if __name__ == "__main__":
    try:
        query_str = alfred.args()[0]
    except IndexError:
        query_str = None
    process(query_str)
