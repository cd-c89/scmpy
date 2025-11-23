import os, sys, json, subprocess

# Get all file names
fs = [os.path.join(node[0],n) for node in os.walk(os.getcwd()) for n in node[2] if "." not in node[2] if "." not in node[0]] 

# Get the current .scm file
if not os.path.isfile(".scm"):
    # init
    os.system("touch .temporary")
    json.dump([{f:subprocess.getoutput("diff .temporary " + f) for f in fs}], open(".scm", "w"))
    os.system("rm .temporary")
else:
    # load controls
    curr = json.loads(open(".scm","r").read())
