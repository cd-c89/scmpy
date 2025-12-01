#!/usr/bin/env python3

import os, sys, json, subprocess, difflib

SCM_NAME = ".scm"
DIFF_NAME = ".diff"

# diff helper
diff_lines = lambda ls_0, ls_1: [
    line.rstrip() for line in list(difflib.unified_diff(ls_0, ls_1))
]


# saves current version to .scm
def commit():
    # Get all files that aren't hidden
    tree = [node for node in os.walk(os.getcwd()) if "." not in node[0]]
    fs = [os.path.join(node[0], n) for node in tree for n in node[2] if n[0] != "."]

    # Get or create .scm file
    if not os.path.isfile(SCM_NAME) or os.path.getsize(".scm") == 0:
        # create
        latest = {f: open(f).read().splitlines() for f in fs}
        json.dump(
            {"latest": latest, "commit": [{"init": latest, "diff": {}}]},
            open(SCM_NAME, "w"),
        )
    else:
        # get
        scm = json.loads(open(SCM_NAME, "r").read())
        late = scm["latest"]
        curr = scm["commit"]
        old_fs = [f for f in curr[-1]["init"]] + [f for f in curr[-1]["diff"]]
        new_fs = [f for f in fs if fs not in old_fs]
        init = {f: open(f).read().splitlines() for f in new_fs if f not in old_fs}
        # We use unified diff from difflib since it still works with patch.
        diff = {f: diff_lines(late[f], open(f).read().splitlines()) for f in old_fs}
        scm["latest"] = {f: open(f).read().splitlines() for f in fs}
        scm["commit"].append({"init": init, "diff": diff})
        json.dump(scm, open(SCM_NAME, "w"))


# pops latest without caching.
# not gonna ether novel files, that seems pointless?
def scrape():
    (not os.path.isfile(SCM_NAME) or os.path.getsize(".scm") == 0) and exit()
    [
        open(k, "w").write("\n".join(v))
        for k, v in json.loads(open(SCM_NAME, "r").read())["latest"].items()
    ]


# let's just roll back one, that's logically equivalent
def revert():
    scrape()
    scm = json.loads(open(SCM_NAME, "r").read())
    late = scm["latest"]
    curr = scm["commit"]
    len(curr) < 2 and exit()
    last = curr.pop()["diff"]
    for k, v in last.items():
        open(DIFF_NAME, "w").write("\n".join(v))
        os.system("patch -R " + k + " " + DIFF_NAME)
    json.dump(scm, open(SCM_NAME, "w"))
    os.delete(DIFF_NAME)


viewer = lambda: os.system(
    "jq . .scm"
)  # print(json.dumps(json.load(open(SCM_NAME)), indent=4))

# Trivial Comment

__name__ == "__main__" and len(sys.argv) == 2 and {
    "commit": commit,
    "scrape": scrape,
    "revert": revert,
    "viewer": viewer,
}[sys.argv[1]]()
