# -*- coding: utf-8 -*-

import alfred
import calendar
from delorean import utcnow, parse, epoch

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

        elif query_str == 'yesterday' or query_str == '1 day ago':
            d = utcnow().last_day()
        elif ' days ago' in query_str:
            count = count_from_query(query_str)
            d = utcnow().last_day(count)

        elif query_str == 'last week' or query_str == '1 week ago':
            d = utcnow().last_week()
        elif ' weeks ago' in query_str:
            count = count_from_query(query_str)
            d = utcnow().last_week(count)

        elif query_str == 'last month' or query_str == '1 month ago':
            d = utcnow().last_month()
        elif ' months ago' in query_str:
            count = count_from_query(query_str)
            d = utcnow().last_month(count)

        elif query_str == 'last year' or query_str == '1 year ago':
        	d =	utcnow().last_year()
        elif ' years ago' in query_str:
        	count = count_from_query(query_str)
        	d =	utcnow().last_year(count)

        else:
            # Parse datetime string or timestamp
            try:
                d = epoch(float(query_str))
            except ValueError:
                d = parse(str(query_str))
    except (TypeError, ValueError):
        d = None
    return d

def count_from_query(query):
    splitted = query_str.split(' ')
    return float(splitted[0])


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
    formats = [
        # 1937-01-01 12:00:27
        ("%Y-%m-%d %H:%M:%S", ''),
        # 19 May 2002 15:21:36
        ("%d %b %Y %H:%M:%S", ''), 
        # Sun, 19 May 2002 15:21:36
        ("%a, %d %b %Y %H:%M:%S", ''), 
        # 1937-01-01T12:00:27
        ("%Y-%m-%dT%H:%M:%S", ''),
        # 1996-12-19T16:39:57-0800
        ("%Y-%m-%dT%H:%M:%S%z", ''),
    ]
    for format, description in formats:
        item_value = value.datetime.strftime(format)
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
