import argparse
import json
import sys
from collections import defaultdict
from pprint import pprint


def main():
    parser = argparse.ArgumentParser(
        description="Group list of dicts according to input group keys",
    )
    parser.add_argument('group_keys', nargs='+', help='List of group keys')
    args = parser.parse_args(sys.argv[1:])
    json_arr = ''.join(line.strip() for line in sys.stdin)
    arr = json.loads(json_arr)
    pprint(create_group(arr, args.group_keys))


def create_group(arr, keys):
    tree_groups = defaultdict(list)
    tree_groups[0] = [groupify_arr(arr, keys.pop(0))]
    for level, key in enumerate(keys):
        for group in tree_groups[level]:
            for k, v in group.items():
                group[k] = groupify_arr(v, key)
                tree_groups[level + 1].append(group[k])

    return tree_groups[0][0]


def groupify_arr(arr, key):
    """Group array of dicts to dict of array according to key"""
    container = {}
    for row in arr:
        group_key = row.pop(key)
        container.setdefault(group_key, []).append(row)

    return container


if __name__ == '__main__':
    main()


