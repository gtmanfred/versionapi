from distutils.version import LooseVersion

import requests


class NextRelease(object):

    uri = '/nextrelease/<string:org>/<string:repo>/<string:branch>'

    def get(self, org, repo, branch):
        if branch == 'develop':
            response = __flask__.jsonify({'next': 'Fluorine'})
        else:
            releases = sorted(
                filter(
                    lambda release: release['tag_name'].startswith(f'v{branch}'),
                    requests.get(f'https://api.github.com/repos/{org}/{repo}/releases').json(),
                ),
                key=lambda release: LooseVersion(release['tag_name'][1:]),
                reverse=True,
            )
            if not releases:
                response = __flask__.jsonify({})
                response.status_code = 404
            else:
                newest = LooseVersion(releases[0]['tag_name'][1:])
                newest.version[-1] += 1
                response = __flask__.jsonify({'next': '.'.join(str(num) for num in newest.version)})
        return response
