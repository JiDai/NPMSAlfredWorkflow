import sys
import os
import requests
from workflow import Workflow3 as Workflow
from subprocess import check_output

API_URL = 'https://api.npms.io/v2/search/suggestions?q=%s'


def main(wf):
    # domains = wf.cached_data('example', get_web_data, max_age=60*60*24)  # Cache 1 day

    try:
        query = wf.args[0]
    except IndexError:
        wf.add_item('Please...')

    try:
        response = requests.get(API_URL % query)
        response.raise_for_status()
        suggests = response.json()
    except requests.HTTPError as err:
        wf.add_item('HTTPERROR', subtitle=err.message, uid='ma-by-error', arg='')
    else:
        for suggest in suggests:
            package = suggest['package']
            title = package['name']
            score = '%s%%   Q: %s%%   P: %s%%   M: %s%%' % (
                int(round(suggest['score']['final'] * 100, 0)),
                int(round(suggest['score']['detail']['quality'] * 100, 0)),
                int(round(suggest['score']['detail']['popularity'] * 100, 0)),
                int(round(suggest['score']['detail']['maintenance'] * 100, 0)),
            )
            author = None
            if 'author' in package and 'name' in package['author']:
                author = package['author']['name']

            if 'description' in package and author:
                subtitle = 'by %s, %s' % (author, package['description'])
            elif 'description' in package:
                subtitle = package['description']
            elif author:
                subtitle = 'by %s' % author
            else:
                subtitle = 'No description'
            largetext = '%s\n%s\n%s\nv%s' % (title, subtitle, score, package['version'])
            wf.add_item('%s   %s' % (title, score), subtitle=subtitle, arg=package['links']['npm'], valid=True, largetext=largetext)

    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))
