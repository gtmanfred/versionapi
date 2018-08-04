# -*- coding: utf-8 -*-
import versionapi.celeryapp
import versionapi.tasks.lookup


class Tasks(object):

    uri = '/tasks'

    def post(self):
        repo = __flask__.request.json.get('repo', 'saltstack/salt')
        pr_num = __flask__.request.json.get('pr_num', None)
        commit_id = __flask__.request.json.get('commit_id', None)
        if pr_num is None and commit_id is None:
            response = __flask__.jsonify({
                'message': 'Error! \'pr_num\' or \'commit_id\' must be provided.'
            })
            response.status_code = 406
        elif pr_num and commit_id:
            response = __flask__.jsonify({
                'message': 'Error! Only one of \'pr_num\' or \'commit_id\' can be provided.'
            })
            response.status_code = 406
        else:
            result = versionapi.tasks.lookup.search.delay(
                repository=repo,
                pr_num=pr_num,
                commit_id=commit_id,
            )
            response = __flask__.jsonify({'jid': result.id})
            response.status_code = 200
        return response


class Task(object):

    uri = '/tasks/<string:taskid>'

    def get(self, taskid):
        result = versionapi.celeryapp.tasks.AsyncResult(taskid)
        if result.status == 'PENDING':
            response = __flask__.jsonify({'result': {}})
            response.status_code = 404
        elif result.ready() is False:
            response = __flask__.jsonify({'result': {}})
            response.status_code = 202
        else:
            response = __flask__.jsonify({'result': result.get()})
            if 'fatal: Couldn\'t find remote ref pull/' in response.json['result']:
                response.status_code = 404
        return response
