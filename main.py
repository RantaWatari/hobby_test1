from flask import Flask, render_template,Blueprint


from flask import Flask, request, jsonify,redirect,flash
from deta import Deta
import drive
import os
from werkzeug.utils import secure_filename



deta = Deta(project_key="c0h15t2h_Sk3eFWswxpDpuLxH68FGpCMiGA3rV9kP") # configure your Deta project
db = deta.Base(name='test1')  # access your DB


app = Flask(__name__)
app.register_blueprint(drive.bp)

img_path = os.path.join("static","img")
app.config["UPLOAD_FOLDER"] = img_path


@app.route("/img",methods=["GET"])
def img():
    img = os.path.join(app.config['UPLOAD_FOLDER'],"CaesarShiftCipher\caesar.jpg")
    print(app.config)
    print(img)
    return render_template("index.html",img=[img])

@app.route("/",methods=["GET","POST"])
def hello_world():

    if request.method == "GET":
        #img_list = os.listdir("static/img"+"/CaesarShiftCipher")
        img_list = os.listdir("static/img")
        print(img_list)
        #img_list = ["static/img/CaesarShiftCipher/"+ i for i in img_list]
        img_list = ["static/img/"+ i for i in img_list if "." in i]
        print(img_list)
        print(app.config)
        return render_template("index.html",img=img_list)
    
    if request.method == "POST":
        file = request.files["file"]
        print(type(file))
        #filename = secure_filename(file.filename)
        filename = str(file.filename)
        print(filename)
        #filename = "filetest1.gif"
        print(type(filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        
        return redirect(location="/")

@app.route("/dd",methods=["GET"])
def dd():
    os.system("cd")
    os.system("cd")
    img_list = os.listdir("static/img")
    #img_list = ["static/img/CaesarShiftCipher/"+ i for i in img_list]
    img_list = ["static/img/"+ i for i in img_list if "." in i]
    for i in img_list: 
        os.remove(path=f"{i}")
    
    return redirect(location="/")



@app.route("/test",methods=["GET"])
def test(): 
   return render_template("CaesarShiftCipher.html")


@app.route('/users', methods=["POST"])
def create_user():
    name = request.json.get("name")
    age = request.json.get("age")
    hometown = request.json.get("hometown")
    key = request.json.get("key")
    key = int(2314)

    user = db.put({
        "name": name,
        "age": age,
        "hometown": hometown,
        "key": key,
    })

    return jsonify(user, 201)

@app.route("/users/<key>")
def get_user(key):
    user = db.get(key)
    return user if user else jsonify({"error": "Not found"}, 404)

@app.route("/users/<key>", methods=["PUT"])
def update_user(key):
    user = db.put(request.json, key)
    return user

@app.route("/users/<key>", methods=["DELETE"])
def delete_user(key):
    db.delete(key)
    return jsonify({"status": "ok"}, 200)

@app.route("/users/fetch")
def fetch_user():
    
    users_fetch = db.fetch() #class generator type
    for i in users_fetch:
        users = i
    cont = []
    for j in users:
        cont.append(j)
    #cont = repr(users)
    
    return cont if cont else jsonify({"error": "Not found"}, 404)