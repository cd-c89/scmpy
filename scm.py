import os, sys, json, subprocess, difflib

# diff helper
diff_lines = lambda ls_0, ls_1: "".join([line for line in difflib.unified_diff(ls_0, ls_1)])

# Get all files that aren't hidden
tree = [node for node in os.walk(os.getcwd()) if "." not in node[0]]
fs = [os.path.join(node[0],n) for node in tree for n in node[2] if n[0] != "."]   

# Get or create .scm file
if not os.path.isfile(".scm") or os.path.getsize(".scm") == 0:
    # create
    latest = {f:open(f).read().splitlines() for f in fs}
    json.dump({"latest": latest, "commit":[{"init":latest, "diff":{}}]}, open(".scm", "w"))
else:
    # get
    scm = json.loads(open(".scm","r").read())
    late = scm["latest"]
    curr = scm["commit"]
    old_fs = [f for f in curr[-1]["init"]] + [f for f in curr[-1]["diff"]]
    new_fs = [f for f in fs if fs not in old_fs]
    init = {f:open(f).read() for f in new_fs}
    # We use unified diff from difflib since it still works with patch.
    diff = {f:diff_lines(late[f],open(f).read().splitlines()) for f in old_fs}
    scm["latest"] = {f:open(f).read().splitlines() for f in fs}
    scm["commit"].append({"init":init,"diff":diff})
    json.dump(scm, open(".scm","w"))

# Trivial Comment
