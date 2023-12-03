from flask import*
from sqlite3 import*
import pickle
app=Flask(__name__)
app.secret_key="siddhi"

@app.route("/", methods=["GET","POST"])
def home():
	if "un" in session:
		if request.method=="POST":
			f=open("re.model","rb")
			model=pickle.load(f)
			f.close()
			Age = float(request.form["Age"])
			Glucose = float(request.form["Glucose"])
			BP = float(request.form["BP"])
			Insulin = float(request.form["Insulin"])
			data = [[Age , Glucose , BP , Insulin ]]
			prediction = model.predict(data)
			if prediction=="[0]":
				result="No,You may not have diabetes"
				return render_template("home.html",m=result)
			else:
				result="Yes,You may have diabetes"
				return render_template("home.html",m=result)
		else:
			return render_template("home.html")

	else:
		return redirect(url_for("login"))




@app.route("/login",methods=["GET","POST"])
def login():
	if "un" in session:
		return redirect(url_for("home"))
	if request.method=="POST":
		un=request.form["un"]
		pw1=request.form["pw1"]
		con=None
		try:
			con=connect("pred.db")
			cursor=con.cursor()
			sql="select *from user where un='%s' and pw1='%s'"
			cursor.execute(sql%(un,pw1))
			data=cursor.fetchall()
			if len(data)==0:
				return render_template("login.html",m="invalid username/password")
			else:
				session["un"]=un
				return redirect(url_for("home"))
		except Exception as e:
			return render_template("signup.html",m="issue"+str(e))
		finally:
			if con is not None:
				con.close()
	else:
		return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
	if "un" in session:
		return redirect(url_for("home"))
	if request.method=="POST":
		un=request.form["un"]
		pw1=request.form["pw1"]
		pw2=request.form["pw2"]
		if pw1==pw2:
			con=None
			try:
				con=connect("pred.db")
				cursor=con.cursor()
				sql="insert into user values('%s','%s')"
				cursor.execute(sql%(un,pw1))
				con.commit()
				return redirect(url_for("login"))
			except Exception as e:
				con.rollback()
				return render_template("signup.html",m="user already exists"+str(e))
			finally:
				if con is not None:
					con.close()
		else:
			return render_template("signup.html",m="password did not match")
	else:
		return render_template("signup.html")

@app.route("/logout")
def logout():
	session.pop("un",None)
	return redirect(url_for("login"))

if __name__=="__main__":
	app.run(debug=True,use_reloader=True)

















