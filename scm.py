import os, sys, json, subprocess

# Get all file names
fs = [os.path.join(node[0],n) for node in os.walk(os.getcwd()) for n in node[2]] 

# Get the current .scm file
if not os.path.isfile(".scm"):
    # init
    json.dumps(open(".scm","w"), [{f:subprocess.getoutput("diff " + f + "<(printf)") for f in fs}])
else:
    # load controls
    curr = json.loads(open(".scm","r").read())
