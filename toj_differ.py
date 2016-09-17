#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
diff the solved problems of two users at [TOJ](http://www.toj.asia/)
Required:
    pip3 install pyquery
Run:
    python3 toj_differ.py <user1> <user2>
"""
import json
import re
import sys
from pyquery import PyQuery as PQ

URL_PREFIX = 'http://acm.tju.edu.cn/toj/user_'
URL_SUFFIX = '.html'
DEFAULT_FILE_NAME = 'toj_diff_result.json'
DIFF_RESULT_TYPE = {
    u'firstUser': u'ID1',
    u'secondUser': u'ID2',
    u'both': u'ID1和ID2均通过',
    u'firstOnly': u'仅ID1通过',
    u'secondOnly': u'仅ID2通过'
}

def get_query(user_url):
    html = PQ(url=user_url)
    s = str(html('script'))
    problem_ids = re.findall('p\((\d+)\)', s)
    return set(int(pid) for pid in problem_ids)

def get_diff(id1, st1, id2, st2):
    res = {}
    res[u'code'] = 0
    res[DIFF_RESULT_TYPE[u'firstUser']] = id1
    res[DIFF_RESULT_TYPE[u'secondUser']] = id2
    res[DIFF_RESULT_TYPE[u'both']] = sorted(st1 & st2)
    res[DIFF_RESULT_TYPE[u'firstOnly']] = sorted(st1 - st2)
    res[DIFF_RESULT_TYPE[u'secondOnly']] = sorted(st2 - st1)
    return res

def save_to_file(result, filename=DEFAULT_FILE_NAME):
    with open(filename, 'w') as outfile:
        json.dump(res, outfile, ensure_ascii=False, indent=2, sort_keys=True)

def main(*argv):
    if len(argv) < 2:
        return {'code': 1}
    st1 = get_query(URL_PREFIX + argv[0] + URL_SUFFIX)
    st2 = get_query(URL_PREFIX + argv[1] + URL_SUFFIX)
    res = get_diff(argv[0], st1, argv[1], st2)
    return res

if __name__ == '__main__':
    res = {}
    if len(sys.argv) < 3:
        res = main(u'3013216027', u'6013308567')
    else:
        res = main(sys.argv[1], sys.argv[2])
    save_to_file(res)
    print('INFO:result saved into file %s' % DEFAULT_FILE_NAME)
