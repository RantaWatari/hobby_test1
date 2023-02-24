from flask import Blueprint,render_template,request,redirect,stream_with_context,Response
from deta import Deta

deta = Deta(project_key="c0h15t2h_mW5g2MZCQiMCWoKfzz6eWXqeab6HBMBL") # configure your Deta project
db = deta.Drive(name='drive_test1')  # access your DB


bp = Blueprint("main",__name__)

@bp.route("/drive",methods=["GET","POST"])
def drive():
    if request.method == "GET":
        db_list =  db.list()
        print(db_list)
        #print(db.host)
        get_list = []
        for i in db_list["names"]:
            get_list.append(i)
        print(get_list)
        #print(len(get_list))


        return render_template("drive_test.html",img=get_list)

    if request.method == "POST":
        file = request.files["file"]
        print(f"{file} :: {file.filename} :: {file.content_type}")
        db.put(name =f"{file.filename}", data=file, content_type=f"{file.content_type}")
        
        return redirect(location="/drive")

@bp.route("/drive/AllDelete",methods=["GET"])
def dirve_delete():
    if request.method == "GET":
        db_list = db.list()
        try:
            db.delete_many(db_list["names"])
        except AssertionError:
            pass
        except RuntimeError:
            pass

        return redirect(location="/drive")

@bp.route("/drive/<img>",methods=["GET"])
def drive_img(img):
    if request.method == "GET":
        get_img = db.get(img)
        get_img_format = img.split(".")
        get_img_format = get_img_format[-1]
        print(get_img_format)
        get_img = get_img.iter_chunks()
        
        

        return Response(stream_with_context(get_img),content_type=f"image/{get_img_format}")

        

