import flask,json

app=flask.Flask(__name__)
strings=[]

host='http://localhost'
port=':5000'

v1='/api/v1'
href_head='<a href="'
href_end='">'
@app.route('/')
def hello():
    return "hello world"

def href(link):
	return href_head+host+port+flask.url_for(link)+href_end+link+"</a><br>"

@app.route('/index')
def index():
#	index_html=href_head+host+port+flask.url_for('hello')+href_end+"hello</a>"
	index_html=href('hello')+href('pallot_greets')
	return index_html

@app.route('/api/v1/pallot/<string:text>')
def pallot(text):
	strings.append(text+'<br>')
	return ''.join(strings)

@app.route('/api/v1/pallot_greets')
def pallot_greets():
	return ''.join(strings)

@app.route(v1+'/json_show/<string:text>')
def json_show(text):
	return json.dumps(json.loads(text),sort_keys=True,indent=4)

@app.route(v1+'/json_boneyard/<string:text>')
def json_boneyard(text):
	return "json_boneyard"

if __name__ =='__main__':
    app.run(debug=True,host='0.0.0.0')
