from flask import Flask,redirect,render_template,url_for,request
from flask_pymongo import PyMongo

app=Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/items'
mongo=PyMongo(app)  

@app.route('/')
def home():
    item1=[]
    user1=[]
    item=mongo.db.item_coll
    user=mongo.db.user_coll
    for i in item.find():
        item1.append(i)
    for j in user.find():
        user1.append(j)    
    return render_template("index.html",item=item1, user=user1)


@app.route('/add_item',methods=(["POST","GET"]))
def add_item():
    if request.method=="POST":
        item_name=request.form.get("item_name")
        quantity=request.form.get("quantity")
        price=request.form.get("price")
        total=int(quantity)*int(price)
        coll = mongo.db.item_coll
        coll.insert_one({'item_name':item_name,'quantity': quantity, 'price': price, 'total': total})
        return redirect(url_for('home'))
    return render_template("add_item.html")

@app.route('/add_user',methods=(["POST","GET"]))
def add_user():
    if request.method=="POST":
        user_name=request.form.get("user_name")
        phone_no=request.form.get("phone_no")
        address=request.form.get("address")
        coll = mongo.db.user_coll
        coll.insert_one({'user_name':user_name,'phone_no': phone_no, 'address': address})
        return redirect(url_for('home'))
    return render_template("add_user.html")


@app.route('/edit_item/<string:item_name>',methods=(["POST","GET"]))
def edit_item(item_name):
    if request.method=="POST":
        item_name=request.form.get("item_name")
        quantity=request.form.get("quantity")
        price=request.form.get("price")
        total=int(quantity)*int(price)
        coll = mongo.db.item_coll
        coll.update_one({'item_name': item_name},{"$set":{ 'quantity': quantity, 'price': price, 'total': total}})
        return redirect(url_for("home"))
    coll = mongo.db.item_coll
    idd=coll.find_one({'item_name': item_name})
    return render_template("edit_item.html", ITEM=idd)

@app.route('/edit_user/<string:user_name>',methods=(["POST","GET"]))
def edit_user(user_name):
    if request.method=="POST":
        user_name=request.form.get("user_name")
        phone_no=request.form.get("phone_no")
        address=request.form.get("address")
        coll = mongo.db.user_coll
        coll.update_one({'user_name': user_name},{"$set":{ 'phone_no': phone_no, 'address':address}})
        return redirect(url_for("home"))
    coll = mongo.db.user_coll
    id1=coll.find_one({'user_name': user_name})
    return render_template("edit_user.html", USER=id1)

@app.route('/delete_item/<string:item_name>')
def delete_item(item_name):
    coll = mongo.db.item_coll
    coll.delete_one({"item_name":item_name})
    return redirect(url_for("home"))

@app.route('/delete_user/<string:user_name>')
def delete_user(user_name):
    coll = mongo.db.user_coll
    coll.delete_one({"user_name":user_name})
    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)