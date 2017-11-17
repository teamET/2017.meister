import flask,json

app=flask.Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.route('/<int:key>',methods=["GET","POST","PUT"])
def api_test(key):
    print("key",key)
    if flask.request.method=="GET" :
        print("method is get")
        print("result",flask.request.data)
        return flask.request.data
    elif flask.request.method=='POST':

        return flask.request.data
    elif flask.request.method=='PUT':
        return flask.request.data
    else:
        print("method is not get")

if __name__ =='__main__':
    app.run(debug=True,host='0.0.0.0')
