# -*- coding:UTF-8 -*-
'''
author:wukaizhong
date:20200108
'''

from flask import Flask
from flask import request
from flask import render_template
import time
import pymongo
import logging
from pymongo import MongoClient
from flask import jsonify
from bson import ObjectId
import re


#打印日志
# logging.basicConfig(filename="logs/index.log", filemode="w+", format="%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%mFf-%d %H:%M:%S", level=logging.INFO)


#实例化
app = Flask(__name__)

#设置默认编码
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print "当前编码:"+sys.getdefaultencoding()

#当前时间
def Today():
	now = int(time.time())
	time_local = time.localtime(now)
	now_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
	return now_time

#查找数据
def Finddb(table="test",field=None,display=None):
	myclient = MongoClient("127.0.0.1",27017)
	mydb = myclient["log"]
	tables = mydb[table]
	result = []
	for data in tables.find(field,display):
		for k,v in data.items():
			if isinstance(v,ObjectId):
				str_value = str(v)
				data["_id"] = str_value
			else:
				data[k] = v
		result.append(data)
	#此处返回的结果就是一个list，里面每一个元素都是一个数据结果，是json结构，要想需要json数据的，需要后期处理list
	return result

#查找数据
#查找表格最新的一条数据
def FinddbOne(table="test",field=None,display=None):
	myclient = MongoClient("127.0.0.1",27017)
	mydb = myclient["log"]
	tables = mydb[table]
	result = []
	datas = tables.find(field,display,sort=[("_id",pymongo.DESCENDING)]).limit(1)
	#处理object数据类型，不能够被处理的问题
	for data in datas:
		for k,v in data.items():
			if isinstance(v,ObjectId):
				str_value = str(v)
				data["_id"] = str_value
			else:
				data[k] = v
		result.append(data)
	#此处返回的结果就是一个list，里面每一个元素都是一个数据结果，是json结构，要想需要json数据的，需要后期处理list
	return result


#插入数据
def Insertdb(table,field):
	myclient = MongoClient("127.0.0.1",27017)
	mydb = myclient["log"]
	tables = mydb[table]
	tables.insert_one(field)
	#tables.insert_many(field)

def Updatedb(table,field,newvalues):
	myclient = MongoClient("127.0.0.1",27017)
	mydb = myclient["log"]
	tables = mydb[table]
	tables.update_one(field,newvalues)
	#tables.update_many(field,newvalues)

def Deletedb(table,field):
	myclient = MongoClient("127.0.0.1",27017)
	mydb = myclient["log"]
	tables = mydb[table]
	tables.delete_one(field)
	#tables.delete_many(field)

@app.route("/")
@app.route("/help")
def Help():
	return render_template("help.html")


@app.route("/showsearch")
def Show_search():
	return render_template("search.html", flag=False)

#mongodb的查询结果,调用url:http://127.0.0.1:9090/result?table=test
@app.route("/search")
def Search():
	flag = False
	tables = request.args.get("table")
	title = request.args.get("title")
	content = request.args.get("content")
	remark = request.args.get("remark")
	if (tables !="") and (tables != None):
		if (title != "") and (title != None):
			field = {"title": re.compile(str(title))}
		elif (content != "") and (content != None):
			field = {"content": re.compile(str(content))}
		elif (remark != "") and (remark != None):
			field = {"remark": re.compile(str(remark))}
		else:
			field={}
	else:
		#此种情况只有html中选中<option value="" selected></option>时才会发生
		print "There aren't tables!"
		return render_template("help.html")
	dt = Finddb(tables, field)
	flag = True
	return render_template("search.html", result={"table": tables, "data": dt},flag = flag)


#想要切换get和post方法，只需在html文件中的method改为对应的值即可。
@app.route("/input",methods=['GET','POST'])
def Input():
	#这里的提交方法是get，需要了解怎么样使用post
	#从html获取返回的数据，只要在form、select、input标签下，根据标签的name来获取对应的输入值，即可完成操作
	flag = False
	if request.method == 'POST':
		formData = request.form
		formDict = formData.to_dict()
		table = formDict["table"]
		field = {"title": formDict["title"], "content": formDict["content"], "date": Today(), "remark": formDict["remark"]}
		# 对于输入为空的一个过滤,初次进入页面是None(原则上post第一次不会提交为none的数据)，进入后为输入数据为null
		if (formDict["title"] == "") or (formDict["content"] == "") or (formDict["title"] == None) or (formDict["content"] == None):
			print "The data is null."
		else:
			Insertdb(table,field)
			flag = True
			# app.logger.info("Insert into {} and its _id is {}".format(table, field["_id"]))

	elif request.method == 'GET':
		table = request.args.get("table")
		title = request.args.get("title")
		content = request.args.get("content")
		remark = request.args.get("remark")
		field = {"title": title, "content": content, "date": Today(), "remark": remark}
		# 对于输入为空的一个过滤,初次进入页面是None，进入后为输入数据为null
		if (content == "") or (title == "") or (content == None) or (title == None):
			print "The data is null."
		else:
			Insertdb(table,field)
			flag = True
			# app.logger.info("Insert into {} and its _id is {}".format(table, field["_id"]))
	else:
		print "The methods of Input() is't get and post."
	dt = FinddbOne(table)
	return render_template("input.html", result={"table": table, "data": dt},flag=flag)

#mongodb的查询结果,调用url:http://127.0.0.1:9090/result?table=test
@app.route("/updatesearch")
def UpdateSearch():
	get_parameters = request.args.get("table")
	dt = Finddb(get_parameters)
	return render_template("update.html", result={"table": get_parameters, "data": dt},flag=True)

@app.route("/showupdate")
def Show_update():
	return render_template("update.html", flag=False)

#这里有个bug，如果点击取消修改，会让原本的内容被默认值取代的，这个需要自己注意；
#想着是自己使用那个弹框的问题，这个需要前端继续了解和深化学习才行。目前自己的水平还是有限的。
@app.route("/update",methods=['GET','POST'])
def Update():
	flag = False
	if request.method == 'POST':
		formData = request.form
		dt = formData.to_dict()
		# print dt
		updatetable = dt["updatetable"]
		field = {"_id": ObjectId(dt["data_id"])}
		#因为返回的dt数据中，titleback、contentback、remarkback仅有一个，所以需要判断dt中是否包含这个字段；
		#也可以使用：dt.has_key("titleback"),不过仅python2支持
		if "titleback" in dt:
			if (dt["titleback"] != "") and (dt["titleback"] != None) and (dt["titleback"] != "修改标题"):
				flag = True
				newtitle = {"$set": {"title": dt["titleback"]}}
				Updatedb(updatetable, field, newtitle)
				# app.logger.info("Update the title of {} to {}".format(updatetable, dt["titleback"]))
			else:
				print "There aren't title!"
		elif "contentback" in dt:
			if (dt["contentback"] != "") and (dt["contentback"] != None) and (dt["contentback"] != "修改内容"):
				flag = True
				newcontent = {"$set": {"content": dt["contentback"]}}
				Updatedb(updatetable, field, newcontent)
				# app.logger.info("Update the content of {} to {}".format(updatetable, dt["contentback"]))
			else:
				print "There aren't content!"
		elif "remarkback" in dt:
				if (dt["remarkback"] != "") and (dt["remarkback"] != None) and (dt["remarkback"] != "修改备注"):
					flag = True
					newremark = {"$set": {"remark": dt["remarkback"]}}
					Updatedb(updatetable, field, newremark)
					# app.logger.info("Update the remark of {} to {}".format(updatetable, dt["remarkback"]))
				else:
					print "There aren't remarks!"
		elif "updatetable" not in dt:
			print "There aren't tables."
		else:
			print "There aren't tables or title or content or remarks."
	elif request.method == 'GET':
		pass
	else:
		print "Something is wrong!"
	dt = Finddb(updatetable)
	return render_template("update.html", result={"table": updatetable, "data": dt},flag=flag)

@app.route("/deletedata")
def DeleteData():
	updatetable = request.args.get("updatetable")
	data_id = request.args.get("data_id")
	field = {"_id": ObjectId(data_id)}
	if (updatetable != "") and (data_id != "") and (updatetable != None) and (data_id != None):
		Deletedb(updatetable, field)
		# app.logger.info("Delete from {}  {}".format(updatetable, field))
	else:
		print "There aren't tables or ID."
	dt = Finddb(updatetable)
	return render_template("update.html", result={"table": updatetable, "data": dt})

if __name__ == '__main__':
	#默认值：host=127.0.0.1, port=5000, debug=false
	app.run("127.0.0.1","9190",debug=True)