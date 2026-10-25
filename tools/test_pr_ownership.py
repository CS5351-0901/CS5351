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

 def test_d2_cannot_modify_team_or_a1_after_week5(self):
  paths=[
   "course_evidence/team/week06/status.md",
   "course_evidence/A1/week06/review.md",
   "tests/roles/a1/test_core.py",
  ]
  errors=self.check("d2",paths)
  self.assertEqual(len(errors),3)

 def test_v3_b1_b2_support_is_exclusive(self):
  b1=["course_tools/b1_support/models.py","course_tools/b1_support/checks/check_path_rules.py"]
  b2=["course_tools/b2_support/case_models.py","course_tools/b2_support/checks/check_deterministic.py"]
  self.assertEqual(self.check("b1",b1),[])
  self.assertEqual(self.check("b2",b2),[])
  self.assertEqual(len(self.check("b1",b2)),2)
  self.assertEqual(len(self.check("b2",b1)),2)
  self.assertTrue(self.check("d2",b1))
  self.assertTrue(self.check("a1",b2))
  self.assertTrue(self.check("b1",["course_tools/other/file.py"]))
  self.assertTrue(self.check("b2",["course_evidence/team/week06/notes.md"]))

 def test_v3_support_commit_cannot_mix_original_work(self):
  ident="f"*40
  self.assertEqual(g.check_support_commit_scope("b1",[(ident,[
   "course_tools/b1_support/models.py","course_evidence/B1/week07/support.md"
  ])]),[])
  errors=g.check_support_commit_scope("b1",[(ident,[
   "course_tools/b1_support/models.py","main.py",
   "tests/roles/b1/test_role_baseline.py","course_tools/b2_support/path.py"
  ])])
  self.assertEqual(len(errors),3)
  self.assertEqual(g.check_support_commit_scope("b2",[(ident,[
   "main.py","tests/roles/b2/test_role_b2.py"
  ])]),[])

 def test_v3_support_only_stdlib_and_own_imports(self):
  valid="import os\nfrom pathlib import Path\nfrom course_tools.b1_support.models import Item\nfrom .models import Item\n"
  self.assertEqual(g.check_support_imports("b1","course_tools/b1_support/models.py",valid),[])
  invalid="import main\nimport pytest\nfrom skills.CodeAgent import SKILL\nfrom course_tools.b2_support.models import Result\n"
  self.assertEqual(len(g.check_support_imports("b1","course_tools/b1_support/models.py",invalid)),4)
  self.assertTrue(g.check_support_imports("b2","course_tools/b2_support/checks/file.py","from ..b1_support import something"))
  self.assertTrue(g.check_support_imports("b1","course_tools/b1_support/broken.py","def broken("))

 def test_v3_b2_sibling_short_imports_from_actual_modules(self):
  path="course_tools/b2_support/checks/check_deterministic.py"
  valid="import deterministic\nfrom case_models import StringCase\n"
  self.assertEqual(g.check_support_imports("b2",path,valid,{"deterministic","case_models"}),[])
  self.assertEqual(len(g.check_support_imports("b2",path,valid)),2)
  self.assertTrue(g.check_support_imports("b2",path,"import nonexistent\n",{"case_models"}))
  self.assertTrue(g.check_support_imports("b2",path,"import other_role\n",{"case_models"}))
  self.assertTrue(g.check_support_imports("b1","course_tools/b1_support/checks/check_metric.py","import deterministic\n",{"models"}))

 def test_v3_sibling_imports_do_not_allow_unsafe_names(self):
  path="course_tools/b2_support/checks/check_corpus_writer.py"
  allowed={"corpus_writer","deterministic","case_models"}
  forbidden="import pytest\nimport main\nfrom course_tools.b1_support.models import Model\nfrom skills.CodeAgent import forbidden\n"
  self.assertEqual(len(g.check_support_imports("b2",path,forbidden,allowed)),4)
  self.assertEqual(g.check_support_imports("b2",path,"from corpus_writer import write_corpus\n",allowed),[])
  self.assertTrue(g.check_support_imports("b2",path,"from ..other_role import outside\n",allowed))

if __name__=="__main__":unittest.main(verbosity=2)
