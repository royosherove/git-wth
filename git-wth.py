import os
import sys
import time
import time
import datetime
import random
import re
from  relative import *
from git import Repo
from datetime import datetime
from datetime import timedelta

join = os.path.join

global masterbranch
global longest_name
longest_name=0 
masterbranch = "master"
if len(sys.argv) >1 :
    masterbranch = sys.argv[1]
class BranchDetails:
    name = ""
    latest_commit = ""
    merge_base_with_master = ""
    missing_commits = False
    ows_commits = False
    unmerged_to_master = ""
    longest_unmereged=-1
    def __INIT__(self):
        self.longest_unmereged=-1

    def get_longest_unmerged_to_master(self,repo):
      if not self.longest_unmereged ==  -1:
        return self.longest_unmereged
      lines = self.unmerged_to_master.splitlines()
      if len(lines)==0:
          return timedelta(0,0,0)

      commit_date = datetime.fromtimestamp(int(repo.git.show ("-s", "--format=%ct",lines[0])))
      today = datetime.fromtimestamp(time.time())
      diff = today - commit_date

      self.longest_unmereged = diff
      return self.longest_unmereged

# git branch --no-merged
# git branch --contains master
#
def write_graph_lagging(all_branches,filename):
    file1 = open(filename,'w')
    for bran in all_branches:

        if bran.name.startswith("*"):
            continue
        if "->" in bran.name:
            continue

        if bran.ows_commits and bran.missing_commits:
            #NEED TO WRITE GET LONGEST UNMSYNCED FROM MASTER
            diff = bran.get_longest_unmerged_to_master(repo)
            fileline = bran.name.ljust(longest_name,"-") + " " +  unicode(diff.days)
            file1.write(fileline + "\n")

        #print_owed_and_lagging(bran,file1)
    file1.close()

def write_graph_hiding(all_branches,filename):
    file1 = open(filename,'w')
    for bran in all_branches:

        if bran.name.startswith("*"):
            continue
        if "->" in bran.name:
            continue

        if bran.ows_commits and bran.missing_commits:
            diff = bran.get_longest_unmerged_to_master(repo)
            fileline = bran.name.ljust(longest_name,"-") + " " +  unicode(diff.days)
            file1.write(fileline + "\n")

        #print_owed_and_lagging(bran,file1)
    file1.close()
def print_owed(bran):
    if bran.ows_commits and (not bran.missing_commits):
      print 
      print ">>" , bran.name
      print "  -------------"
      print "  ows to master:"
      print "  -------------"
      lines = bran.unmerged_to_master.splitlines()
      print_top_n(lines,5)

def print_top_n(lines,howmany):
  for comm in lines[:howmany]:
      print "  ",  repo.git.show ("-s", "--format=%h : %cr : %s (%cn)", comm)
  if len(lines) > howmany:
      print "+" , (len(lines)-howmany) , "more commits after that"

def print_owed_and_lagging(bran,datfile):
    if bran.ows_commits and bran.missing_commits:
      print ">> " , bran.name
      print "  -------------"
      print "  ows to ", masterbranch, " (oldest first):"
      print "  -------------"

      lines = bran.unmerged_to_master.splitlines()
      print_top_n(lines,5)


      print 
      print "  -------------"
      print "  owed by ", masterbranch, "(oldest first):"
      print "  -------------"
      lines2 = bran.unmerged_to_branch.splitlines()
      print_top_n(lines2,5)
      #print "Ows Master:"
      #print ">> latest is from " , get_commit_date(bran.unmerged_to_master.splitlines()[0])
      #print ">>" , bran.unmerged_to_master
      #print "Missing from master:"
      #print ">> latest is from " , get_commit_date(bran.unmerged_to_branch.splitlines()[0])
      #print ">>",  bran.unmerged_to_branch
      #print 
def getdate(thedate):
    strdate =  time.asctime(time.gmtime(thedate))
    return strdate

def isokstring(thestr):
    if len(re.findall("\w+",thestr)) > 3 :
        return True;

def get_commit_date(commit_name):
    return repo.git.show("-s", "--format=%ct", commit_name)

repo = Repo(".")
assert not repo.bare
repo.head.ref = repo.heads[masterbranch]
global latest_master_commit
latest_master_commit= repo.git.merge_base(masterbranch, masterbranch)

remotes = repo.git.branch("-r")
for remote in remotes.splitlines():
    try:
        #print "tracking remote ", remote
        repo.git.branch("--track", remote.strip())
    except:
        pass
        #print "problem with ", remote
print "done tracking"
print "***************"
#repo.git.fetch("--all")


unmeregd = repo.git.branch("-a")
#print unmeregd
print "******************************"
print "******************************"

all_branches = []

for line in unmeregd.splitlines():
  thename = line.strip()
  branch_item = BranchDetails()
  branch_item.name = thename
  branch_item.latest_master_commit= latest_master_commit

  all_branches.append(branch_item)
  print
  print "examining ", thename
  l = len(thename)
  if longest_name< l: longest_name = l
  if thename.startswith("*"):
      print "skipping"
      continue

  try:
      branch_item.latest_branch_commit = repo.git.merge_base(  branch_item.name, branch_item.name)
      branch_item.latest_branch_commit_date = get_commit_date(branch_item.latest_branch_commit)

      branch_item.common_merge_base = repo.git.merge_base(  masterbranch,branch_item.name)
      branch_item.common_merge_base_date= get_commit_date(branch_item.common_merge_base)

      branch_item.master_and_common_base_base = repo.git.merge_base(  masterbranch,branch_item.common_merge_base )
      branch_item.master_and_common_base_base_date= get_commit_date(branch_item.master_and_common_base_base)

      branch_item.unmerged_to_master = repo.git.rev_list(masterbranch + "..." + branch_item.name, "--right-only",  "--abbrev-commit", "--date=relative", "--reverse")
      branch_item.unmerged_to_branch = repo.git.rev_list(masterbranch + "..." + branch_item.name, "--left-only", "--abbrev-commit", "--date=relative", "--reverse")
  except:
      print "ERROR looking up some data. moving to next branch"
      #raise
      continue

  #print "Latest Bramch Commit (LBC)         " , latest_branch_commit
  #print "Common Merge Base (CMB)            " , common_merge_base
  #print "Master-to-Common-Base Base (MCB)   " , master_and_common_base_base
  #print "unmerged to master:   " , branch_item.unmerged_to_master
  #print "unmerged to branch:   " , branch_item.unmerged_to_branch


  try:
      repo.git.merge_base(  branch_item.master_and_common_base_base,masterbranch, "--is-ancestor")
      branch_item.chil_of_master = True
  except:
      print "not a child of master.. moving on to next branch"
      continue

  print "master is the parent of this branch"


  branch_item.ows_commits = False
  if len(branch_item.unmerged_to_master.strip()) >0:
      #print ">>>> master is missing commits from " , branch_item.name , branch_item.unmerged_to_master
      branch_item.ows_commits = True

  if len(branch_item.unmerged_to_branch.strip()) >0:
      #print ">>>> " , branch_item.name , " is missing commits from master", branch_item.unmerged_to_branch
      branch_item.missing_commits = True

  if branch_item.latest_branch_commit == branch_item.common_merge_base:
      # these are not the commits you're looking for. Seems to be up to date
      #print "moving to next branch"
      continue

  if len(branch_item.master_and_common_base_base.strip())>0:
      #this shoudl throw is common merge base is not parent of latest master
      repo.git.merge_base(  branch_item.common_merge_base,branch_item.latest_master_commit, "--is-ancestor")
      #print "latest master is the parent of this branch. All good"
      continue


print 
print "---------------"
print "Branches that owe commits and lag behind master:"
print "(possibly feature branches)"
print "---------------"
all_branches = sorted(all_branches,key=lambda item: item.get_longest_unmerged_to_master(repo), reverse=True)
write_graph_hiding(all_branches,"lagging.dat")
write_graph_lagging(all_branches,"lagging.dat")

print 
print "---------------"
print "Branches that only owe commits: "
print "(possibly feature branches)"
print "---------------"
for bran in all_branches:
    print_owed(bran)

print 
print "---------------"
print "Branches that are missing commits from master with nothing to contribute:"
print "(possibly release branches or feature branches with no new commits yet)"
print "---------------"
for bran in all_branches:
    if (not bran.ows_commits) and bran.missing_commits:
      print bran.name
      #print "Missing from master:"
      #print ">>",  bran.unmerged_to_branch

print 
print "---------------"
print "Fully sync branches with master"
print "(possibly stale or unneeded)"
print "---------------"
for bran in all_branches:
    if (not bran.ows_commits) and (not bran.missing_commits):
      print bran.name
#since  = timesince( datetime.fromtimestamp(item[0])) 
#print ">>> ", since , "\t", committed

repo.head.ref = repo.heads[masterbranch]
os.system("python termgraph.py lagging.dat")
