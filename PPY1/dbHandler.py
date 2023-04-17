import pymysql as mysql
import bleach
import sys, json, decimal
import antihack as ah
import socket


endpoint = "dbserver.anonyo.net"
endpoint = socket.gethostbyname(endpoint)
user = "s25833"
port = 3306
passwd = "test"
dbName="PJWSTK"

def tabulate(cur,cols):
	tab=[]
	rw=cur.fetchone()
	while(rw is not None):
		r={}
		for i in range(len(cols)):
			r[cols[i]]=rw[i]
		tab.append(r)
		rw = cur.fetchone()
	return tab

def select(tab:str,cols:list,where:dict,join={},ext="",colNames=None):
	con=Connect()
	resp=con.select(tab,cols,where,join,ext,colNames)
	con.close()
	return resp
def insert(tab:str,vals:dict|list,returnid=True):
	con=Connect()
	resp=con.insert(tab,vals,returnid)
	con.close()
	return resp

def update(tab:str,upd:dict,where:dict,countRows=True):
	con=Connect()
	resp=con.update(tab,upd,where,countRows)
	con.close()
	return resp

def delete(tab:str,where:dict,countRows=True):
	con=Connect()
	resp=con.delete(tab,where,countRows)
	con.close()
	return resp

def runSql(qr:str,val=(),commit=False,returnResp=False,returnId=False,countRows=False):
	con=Connect()
	resp=con.runSql(qr,val,commit,returnResp,returnId,countRows)
	con.close()
	return resp
class Connect:
	def __init__(self):
		try:
			self.cnx = mysql.connect(user=user,port=port, password="test", host=endpoint, database=dbName)
			self.cur = self.cnx.cursor()
		except Exception as e:
			print(e)

	def commit(self):
		self.cnx.commit()
	def close(self):
		self.cur.close()
		self.cnx.close()
	def select(self,tab:str,cols:list,where:dict,join={},ext="",colNames=None,debug=False):
		if colNames is None:
			colNames=list(cols)
		cond=[]
		wr=""
		pts=tuple(where.values())
		if len(where)+len(join)>0:
			for i in where.keys():
				cond.append("{} = %s".format(i))
			for i in join.keys():
				cond.append("%s = %s" % (i, join[i]))
			wr="where {}".format(" AND ".join(cond))
		qr = 'select %s from %s %s %s' % (",".join(cols), tab, wr, ext)
		try:
			self.cur.execute(qr,pts)
		except Exception as e:
			print(e)
		if debug:
			print(self.cur._executed)
		return tabulate(self.cur,colNames)
	def insert(self,tab:str,vals:dict|list,returnid=True,debug=False):
		ids=[]
		if type(vals)==dict:
			vals=[vals]
		for i in vals:
			cols=",".join(i.keys())
			vals=tuple(i.values())
			embed=",".join(["%s"]*len(i.keys()))
			qr="insert into {} ({}) values ({})".format(tab,cols,embed)
			self.cur.execute(qr,vals)
			ids.append(self.cur.lastrowid)
			if debug:
				print(self.cur._executed)
		self.commit()
		if returnid:
			if len(ids)==1:
				return ids[0]
			return ids

	def update(self,tab:str,upd:dict,where:dict,countRows=True,debug=False):
		vals=[]
		st=[]
		whr=[]
		for i in upd:
			vals.append(upd[i])
			st.append("{}=%s".format(i))
		for i in where:
			vals.append(where[i])
			whr.append("{}=%s".format(i))
		st=",".join(st)
		whr=" AND ".join(whr)
		qr="update {} set {} where {}".format(tab,st,whr)
		self.cur.execute(qr,tuple(vals))
		if debug:
			print(self.cur._executed)
		self.commit()
		if countRows:
			return self.cur.rowcount
	def delete(self,tab:str,where:dict,countRows=True,debug=False):
		vals=[]
		whr=[]
		for i in where.keys():
			vals.append(where[i])
			whr.append("{}=%s".format(i))
		whr=" AND ".join(whr)
		qr="delete from {} where {}".format(tab,whr)
		self.cur.execute(qr,tuple(vals))
		if debug:
			print(self.cur._executed)
		self.commit()
		if countRows:
			return self.cur.rowcount
	def runSql(self,qr:str,val=(),commit=False,returnResp=False,returnId=False,countRows=False,debug=False):
		self.cur.execute(qr, tuple(val))
		if debug:
			print(self.cur._executed)
		resp={}
		if commit:
			self.commit()
		if returnResp or returnId or countRows:
			if returnResp:
				resp["resp"]=self.cur.fetchall()
			if returnId:
				resp["id"]=self.cur.lastrowid
			if countRows:
				resp["count"]=self.cur.rowcount
			return resp

