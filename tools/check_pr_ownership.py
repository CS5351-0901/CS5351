"""PR ownership validator. Execute ONLY from a trusted base commit."""
import argparse
import ast
import subprocess
import sys

ROLES = ("a1","a2","b1","b2","c1","c2","d1","d2")
REPO = "CS5351-0901/CS5351"
EXACT = {
 "a1":{"metadata.yaml","_conf_schema.json","pyproject.toml"},
 "a2":set(), "b1":set(), "b2":set(), "c1":set(),
 "c2":{"skills/CodeAgent/scripts/codeagent_packager.py"},
 "d1":{"skills/CodeAgent/scripts/codeagent_sandbox.py","skills/CodeAgent/scripts/codeagent_js_checker.js","skills/CodeAgent/scripts/package.json"},
 "d2":{"skills/CodeAgent/scripts/codeagent_security.py"},
}
FUNCTIONS = {
 "__init__":"a2","_get_config":"a1","_ensure_nodejs":"a1",
 "_install_nodejs_linux":"a1","_install_nodejs_mac":"a1",
 "_install_nodejs_from_official":"a1","_ensure_js_dependencies":"a1",
 "_extract_requirement":"b1","_is_in_blacklist":"b1","_assess_project":"b1",
 "_is_exit_command":"b2","_sanitize_session_id":"b2",
 "_cleanup_session":"b2","_create_process_json":"b2",
 "_analyze_error":"c1","_generate_debug_fix":"c1",
 "_save_snapshot":"c1","_rollback_to_snapshot":"c1",
 "_call_packager":"c2","_call_sandbox":"d1","_call_js_checker":"d1",
 "_call_security_scan":"d2","agent_command":"a2",
 "terminate":"a2","get_star":"a2",
}

def role_for(branch,author,head_repo):
    if head_repo.lower()!=REPO.lower():
        raise ValueError("forked PR heads are not permitted for course roles")
    if branch.startswith("ops/"):
        if author.lower()!="gekamok":
            raise ValueError("only team leader gekamok may use ops/*")
        return "ops"
    if branch.startswith("course/") and branch[7:] in ROLES:
        return branch[7:]
    raise ValueError("branch must be course/<role> or leader ops/*")

def allowed(role,path):
    if role=="ops": return True
    if not path or path.startswith("/") or "\\" in path or ".." in path.split("/"):
        return False
    return (path.startswith("course_evidence/"+role.upper()+"/")
        or path.startswith("tests/roles/"+role+"/")
        or path in EXACT[role] or path=="main.py")

def symbols(text):
    result={}
    globals_=[]
    for n in ast.parse(text,filename="main.py").body:
        if isinstance(n,ast.ClassDef) and n.name=="CodeAgentPlugin":
            rest=[]
            for m in n.body:
                if isinstance(m,(ast.FunctionDef,ast.AsyncFunctionDef)):
                    result[m.name]=ast.dump(m,include_attributes=False)
                else: rest.append(ast.dump(m,include_attributes=False))
            globals_.append((n.name,tuple(ast.dump(x,include_attributes=False) for x in n.bases),
                             tuple(ast.dump(x,include_attributes=False) for x in n.decorator_list),
                             tuple(rest)))
        elif isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
            result[n.name]=ast.dump(n,include_attributes=False)
        else: globals_.append(ast.dump(n,include_attributes=False))
    result["<module/class structure>"]=repr(globals_)
    return result

def check(branch,author,head_repo,paths,before=None,after=None):
    role=role_for(branch,author,head_repo)
    errors=[]
    if not paths: errors.append("empty PR")
    if role=="ops": return errors
    for p in paths:
        if not allowed(role,p): errors.append(p+": outside "+role.upper()+" ownership")
    if "main.py" in paths:
        if before is None or after is None:
            errors.append("main.py: source versions are unavailable")
        else:
            try:
                a,b=symbols(before),symbols(after)
                changed={n for n in a.keys()|b.keys() if a.get(n)!=b.get(n)}
                if before!=after and not changed: changed={"<non-code edit>"}
                for n in sorted(changed):
                    if FUNCTIONS.get(n)!=role:
                        errors.append("main.py::"+n+" owned by "+FUNCTIONS.get(n,"TEAM LEADER"))
            except SyntaxError as e:
                errors.append("main.py failed to parse: "+str(e))
    return errors

def git(*args):
    return subprocess.check_output(["git",*args])

def main():
    p=argparse.ArgumentParser()
    for arg in ("base","head","branch","author","head-repo","expected-head-sha"):
        p.add_argument("--"+arg,required=True)
    args=p.parse_args()
    try:
        sha=git("rev-parse",args.head).decode().strip()
        if sha!=args.expected_head_sha: raise ValueError("PR head changed; rerun status check")
        role=role_for(args.branch,args.author,args.head_repo)
        paths=[s.decode("utf-8","surrogateescape") for s in
            git("diff","--name-only","--no-renames","-z",args.base+"..."+args.head).split(b"\0") if s]
        before=after=None
        if "main.py" in paths and role!="ops":
            before=git("show",args.base+":main.py").decode("utf-8-sig")
            after=git("show",args.head+":main.py").decode("utf-8-sig")
        errors=check(args.branch,args.author,args.head_repo,paths,before,after)
    except (ValueError,OSError,subprocess.CalledProcessError,UnicodeError) as exc:
        print("OWNERSHIP FAIL:",exc,file=sys.stderr)
        return 1
    for e in errors: print("BLOCKED:",e,file=sys.stderr)
    print("OWNERSHIP CHECK", "PASS" if not errors else "FAIL",
          "role="+role,"changed="+str(len(paths)))
    return 1 if errors else 0

if __name__=="__main__": sys.exit(main())
