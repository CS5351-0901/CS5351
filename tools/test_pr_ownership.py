"""Regression tests for the PR ownership guard, including D2's actual mistake."""
import importlib.util
from pathlib import Path
import unittest

p=Path(__file__).with_name("check_pr_ownership.py")
s=importlib.util.spec_from_file_location("guard",p)
g=importlib.util.module_from_spec(s)
s.loader.exec_module(g)

class OwnershipTests(unittest.TestCase):
 def check(self,role,paths,old=None,new=None):
  return g.check("course/"+role,"member",g.REPO,paths,old,new)
 def test_d2_own_files_pass(self):
  self.assertEqual(self.check("d2",["course_evidence/D2/week06/notes.md","tests/roles/d2/test_next.py","skills/CodeAgent/scripts/codeagent_security.py"]),[])
 def test_d2_wrong_team_path_fails(self):
  errors=self.check("d2",["course_evidence/D2/week05/baseline.md","course_evidence/team/week01/role_and_scope.md","course_evidence/team/week02/source_map.md","course_evidence/team/week03/initial_findings.md"])
  self.assertEqual(len(errors),3)
 def test_wrong_role_and_governance_paths_fail(self):
  self.assertEqual(len(self.check("a2",["course_evidence/C1/week06/a.md","tools/check_pr_ownership.py",".github/workflows/pr-ownership.yml"])),3)
 def test_all_roles_can_write_own_evidence_and_tests(self):
  for role in g.ROLES:
   with self.subTest(role=role):
    self.assertEqual(self.check(role,["course_evidence/"+role.upper()+"/week06/notes.md","tests/roles/"+role+"/test_next.py"]),[])
 def test_main_code_owned_by_specific_role(self):
  a="class CodeAgentPlugin:\n def _call_security_scan(self):\n  return 1\n"
  b="class CodeAgentPlugin:\n def _call_security_scan(self):\n  return 2\n"
  self.assertEqual(self.check("d2",["main.py"],a,b),[])
  self.assertTrue(self.check("b1",["main.py"],a,b))
 def test_module_edits_need_leader(self):
  a="import os\nclass CodeAgentPlugin:\n def _call_security_scan(self):\n  return True\n"
  b=a.replace("import os","import sys")
  self.assertIn("TEAM LEADER",self.check("d2",["main.py"],a,b)[0])
 def test_comment_changes_need_leader(self):
  a="def get_star(ctx):\n return ctx\n"
  self.assertTrue(self.check("a2",["main.py"],a,a.replace(" return ctx"," # note\n return ctx")))
 def test_leader_ops_only(self):
  self.assertEqual(g.role_for("ops/guard","gekamok",g.REPO),"ops")
  with self.assertRaises(ValueError):g.role_for("ops/guard","other",g.REPO)
 def test_other_branches_and_forks_blocked(self):
  with self.assertRaises(ValueError):g.role_for("user/test","member",g.REPO)
  with self.assertRaises(ValueError):g.role_for("course/d2","member","other/fork")
 def test_path_traversal_blocked(self):
  self.assertTrue(self.check("d2",["course_evidence/D2/../team/file.md"]))

if __name__=="__main__":unittest.main(verbosity=2)
