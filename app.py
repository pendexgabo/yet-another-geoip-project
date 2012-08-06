import os
import pygeoip
import json
from pygeoip import GeoIP
from flask import Flask, request, current_app, url_for, render_template



app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', hostname =  request.base_url)


@app.route('/location.json')
def location():

	callback = request.args.get('callback', False);
	ip = request.args.get('ip', client_ip());
	
	gi = GeoIP('data/GeoLiteCity.dat')
	geodata = gi.record_by_addr(ip);
	geodata['ip_address'] = ip;
	geodata = json.dumps(geodata)

	if callback:
		content = str(callback) + '(' + str(geodata) + ')'
	else:
		content = geodata

 	return current_app.response_class(content, mimetype='application/json')


def client_ip():
	if request.headers.get('X-Forwarded-For'):
		ip_adds = request.headers.get('X-Forwarded-For').split(',')
		ip = ip_adds[0]
	else:
		ip = request.remote_addr

	return ip


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug = True)
