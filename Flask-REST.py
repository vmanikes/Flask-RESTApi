from flask import Flask,jsonify,request,render_template
import redis

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
def checkConnection(r):
    try:
        if r.ping() == True:
            return "200 Connection Succesful"
    except Exception as e:
        return e

@app.route('/<string:name>',methods=['GET'])
def get_name(name):

    pipe = r.pipeline()
    pipe.get(name)
    result = pipe.execute()[0]
    if result is not None:
        return jsonify({name:result})
    else:
        return jsonify("Bad Request")

@app.route('/lang/',methods=['POST'])
def post_content():
    pipe = r.pipeline()
    pipe.set('language',request.json['language'])
    result = pipe.execute()[0]

    return jsonify(result)

@app.route("/<string:name>",methods=['DELETE'])
def delete(name):
    pipe = r.pipeline()
    pipe.delete(name)
    result = pipe.execute()[0]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
