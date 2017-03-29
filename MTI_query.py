#! python2.7
"""
query_mfs.py

The two queries 'query_Mon' and 'query_Tue_Fri' are identical except for the dttoc >= SYSDATE;
I tried building this decision process into the sql query itself but I couldn't get consistent results back.
That said, this method works fine.
"""

# query returns an, title, and abstract
query_Mon = """
SELECT q.an, q.arttitle, q.abstract
FROM (SELECT mfs.article.an, mfs.article.arttitle, mfs.artabx.abstract,
row_number() over (partition by mfs.article.an order by case mfs.artabx.abxsrccode when 'AUTH' then 1 when 'PUB' then 2 when 'VEND' then 3 ELSE 4 end) rn
from mfs.issueproc
left join mfs.issue on mfs.issueproc.mid = mfs.issue.mid and mfs.issueproc.dtformat = mfs.issue.dtformat
left join mfs.article on mfs.issueproc.mid = mfs.article.mid and mfs.issueproc.dtformat = mfs.article.dtformat
left join mfs.artabx on mfs.article.an = mfs.artabx.an
left join mfs.artlang on mfs.article.an = mfs.artlang.an
left join mfs.magcover on mfs.article.mid = mfs.magcover.mid
left join mfs.cinsubj_an on mfs.cinsubj_an.an = mfs.article.an
where (mfs.magcover.priority in ('1', '2') and MFS.ISSUEPROC.VID <> 'MED' and mfs.cinsubj_an.an IS NULL and mfs.issueproc.procnum = '32' and (mfs.artlang.artlangcode = 'EN' or MFS.ARTLANG.TTLLANGCODE = 'EN') and mfs.issueproc.dtdataend is null and mfs.issue.dttoc >= trunc(SYSDATE - 3))) q
where q.rn=1 and q.abstract is not null
"""

query_Tue_Fri = """
SELECT q.an, q.arttitle, q.abstract
FROM (SELECT mfs.article.an, mfs.article.arttitle, mfs.artabx.abstract,
row_number() over (partition by mfs.article.an order by case mfs.artabx.abxsrccode when 'AUTH' then 1 when 'PUB' then 2 when 'VEND' then 3 ELSE 4 end) rn
from mfs.issueproc
left join mfs.issue on mfs.issueproc.mid = mfs.issue.mid and mfs.issueproc.dtformat = mfs.issue.dtformat
left join mfs.article on mfs.issueproc.mid = mfs.article.mid and mfs.issueproc.dtformat = mfs.article.dtformat
left join mfs.artabx on mfs.article.an = mfs.artabx.an
left join mfs.artlang on mfs.article.an = mfs.artlang.an
left join mfs.magcover on mfs.article.mid = mfs.magcover.mid
left join mfs.cinsubj_an on mfs.cinsubj_an.an = mfs.article.an
where (mfs.magcover.priority in ('1', '2') and MFS.ISSUEPROC.VID <> 'MED' and mfs.cinsubj_an.an IS NULL and mfs.issueproc.procnum = '32' and (mfs.artlang.artlangcode = 'EN' or MFS.ARTLANG.TTLLANGCODE = 'EN') and mfs.issueproc.dtdataend is null and mfs.issue.dttoc >= trunc(SYSDATE - 1))) q
where q.rn=1 and q.abstract is not null
"""

import datetime
import cx_Oracle
# set up db connection
con = cx_Oracle.connect(###############################)

cur = con.cursor()

# based on what day it is (Monday = '0'), run either query_Monday or query_Tue_Fri
if (datetime.datetime.today().weekday() == 0):
  cur.execute(query_Mon)
else:
  cur.execute(query_Tue_Fri)

# print results in MTI-required format
for result in cur:
    print "PMID-", result[0]
    print "TI  -", result[1]
    print "AB  -", result[2]
    print ""

cur.close()
con.close()
