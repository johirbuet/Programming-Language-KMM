from sys import *
import re
numbers=re.compile("[0-9]")
tokens=[]
def open_file(filename):
	data=open(filename,"r").read()
	data+="<EOF>"
	return data
def lex(data):
	tok=""
	state=0
	string=""
	expr=""
	isexpr=0
	data=list(data)
	for char in data:
		tok+=char
		if tok==" ":
			if state==0:
				tok=""
			elif state==1:
				tok=" "
		elif tok=="\n" or tok=="<EOF>":
			if expr!="" and isexpr==1:
				tokens.append("EXPR:"+expr)
				expr=""
			elif expr!="" and isexpr==0:
				tokens.append("NUM:"+expr)
				expr=""
			tok=""
		elif tok=="printc":
			tokens.append("printc")
			tok=""
		elif numbers.match(tok):
			expr+=tok
			tok=""
		elif tok=="+":
			isexpr=1
			expr+=tok
			tok=""
		elif tok=="\"":
			if state==0:
				state=1
			elif state==1:
				tokens.append("STRING:"+string+"\"")
				string=""
				state=0
				tok=""
		elif state==1:
			string+=tok
			tok=""
	print(tokens)
	return tokens
def parse(toks):
	i=0
	while i< len(toks):
		if toks[i]+" "+toks[i+1][0:6]=="printc STRING":
			print(toks[i+1][7:])
			i+=2
		if toks[i]+" "+toks[i+1][0:4]=="printc EXPR":
			print(toks[i+1][5:])
			i+=2
def run():
	data=open_file(argv[1])
	toks=lex(data)
	parse(toks)

run()
