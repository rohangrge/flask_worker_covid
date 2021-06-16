from datetime import date
from flask import Flask, request, jsonify
#from flask_restful import Resource, Api
import requests
import math
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()
#api = Api(app)

s_id = []


@app.route('/covid', methods=['GET'])
def call():
    global s_id
    d_id = request.args.get('district_id')
    date = request.args.get('date')
    headers = {"Accept-Language": "en-IN",
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = {"district_id": d_id, "date": date}
    res = requests.get(
        "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict", headers=headers, params=data)
    #resp = res.json()
    # print(res.content)
    if(res.status_code == 200):
        proresp = {"sessions": []}
        resp = res.json()
        for k in resp['sessions']:
            if(math.trunc(k['available_capacity_dose1']) >= 8 and k['min_age_limit'] >= 18 and k['min_age_limit'] < 45 and k['session_id'] not in reversed(s_id)):
                proresp['sessions'].append(k)
                s_id.append(k['session_id'])
            else:
                continue

        return proresp, 200
    else:

        a = {'error': 'no scene'}
        return a, 403


def scheduleTask():
    # print('test')
    global s_id
    s_id = []


if __name__ == '__main__':
    scheduler.add_job(id='Scheduled Task', func=scheduleTask,
                      trigger="interval", seconds=14400)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000)
