import requests as req
# from pprint import pprint as pp
from json import dump

size = int(input("Кол-во запросов: "))

json_data = {
    'operationName': 'HacktivitySearchQuery',
    'variables': {
        'queryString': '*:*',
        'size': size,
        'from': 0,
        'sort': {
            'field': 'disclosed_at',
            'direction': 'DESC',
        },
        'product_area': 'hacktivity',
        'product_feature': 'overview',
    },
    'query': 'query HacktivitySearchQuery($queryString: String!, $from: Int, $size: Int, $sort: SortInput!) {\n  me {\n    id\n    __typename\n  }\n  search(\n    index: HacktivityReportIndexService\n    query_string: $queryString\n    from: $from\n    size: $size\n    sort: $sort\n  ) {\n    __typename\n    total_count\n    nodes {\n      __typename\n      ... on HacktivityReportDocument {\n        id\n        reporter {\n          id\n          name\n          username\n          ...UserLinkWithMiniProfile\n          __typename\n        }\n        cve_ids\n        cwe\n        severity_rating\n        upvoted: upvoted_by_current_user\n        report {\n          id\n          databaseId: _id\n          title\n          substate\n          url\n          disclosed_at\n          report_generated_content {\n            id\n            hacktivity_summary\n            __typename\n          }\n          __typename\n        }\n        votes\n        team {\n          handle\n          name\n          medium_profile_picture: profile_picture(size: medium)\n          url\n          id\n          currency\n          ...TeamLinkWithMiniProfile\n          __typename\n        }\n        total_awarded_amount\n        latest_disclosable_action\n        latest_disclosable_activity_at\n        __typename\n      }\n    }\n  }\n}\n\nfragment UserLinkWithMiniProfile on User {\n  id\n  username\n  __typename\n}\n\nfragment TeamLinkWithMiniProfile on Team {\n  id\n  handle\n  name\n  __typename\n}\n',
}

resp = req.post('https://hackerone.com/graphql', json=json_data)
nodes = resp.json()["data"]["search"]["nodes"]

for data in nodes:
    report = data["report"]
    reporter = data["reporter"]
    team = data["team"]
    report_generated_content = report["report_generated_content"]

    report.pop("databaseId")

    for obj in [data, report, reporter, team, report_generated_content]:
        if not obj:
            continue

        obj.pop("__typename")
        obj.pop("id")

with open('hacktivity.json', 'w') as fp:
    dump(nodes, fp)