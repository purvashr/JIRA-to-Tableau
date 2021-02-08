
# coding: utf-8

# In[ ]:

import os.path
import time
import getpass
import json
import requests
from requests.auth import HTTPBasicAuth
import sys
import datetime as dt
import pandas as pd

start = 0
naptime = 15
b = 1
issues = []
jqlFilter = "60690"
jira = "https://issues.abc.com/rest/api/2/search"
    
while True:
    query = "?jql=filter=" + jqlFilter + "&startAt=" + str(start) + "&maxResults=100"
    result = requests.get(jira + query, auth=HTTPBasicAuth(user, password))
    data = json.loads(result.text)

    if not data["issues"]:
        break
    else:
        issues += data["issues"]
        time.sleep(naptime)
        b += 1
        start += 100

data["issues"] = issues

b=[];a=[];c=[];d=[];e=[];f=[];g=[];h=[];j=[];k=[];l=[];m=[];n=[];o=[];p=[];q=[];r=[];s=[]

w1=len(data["issues"])

import datetime
for i in range(0,w1):
    b=data["issues"][i]['key']
    c=data["issues"][i]["fields"]["status"]["name"]
    e=data["issues"][i]["fields"]["issuetype"]["name"]
    a.append(b)
    d.append(c)
    f.append(e)
    g=data["issues"][i]["fields"]["resolution"]
    if g is None:
        h.append("none")
    else:
        g=data["issues"][i]["fields"]["resolution"]["name"]
        h.append(g)
    j=data["issues"][i]["fields"]["created"]
    k.append(j)
    l=data["issues"][i]["fields"]["resolutiondate"]
    if l is None:
        m.append("none")
    else:
        l=data["issues"][i]["fields"]["resolutiondate"]
        m.append(l)
    p=data["issues"][i]["fields"]["customfield_11604"]
    if p is None:
        q.append("none")
    else:
        p=data["issues"][i]["fields"]["customfield_11604"]
        q.append(p)
    r=data["issues"][i]["fields"]["duedate"]
    if r is None:
        s.append("none")
    else:
        r=data["issues"][i]["fields"]["duedate"]
        s.append(r)

df = pd.DataFrame({'issue': a,'status':d,'issuetype': f,'resolution':h,'created':k,'resolvdate':m,'custombaselinestart':q,'duedate':s})

import datetime
date_1=datetime.datetime.today().strftime('%Y-%m-%d')

df1 = df[(df.status != "Triage") & (df.status != "Backlog") & (df.issuetype != "Task") & (df.resolution=="none") ]
dailywip=df1['issue'].count() # daily wip total
df2 = df[(df.status == "Triage") | (df.status == "Backlog") & (df.issuetype != "Task")]
df_11=df2.count()
daily_queue=df_11['issue'] # incoming queue

df_wrike=pd.read_excel('hi.xlsx')
df_n=df.merge(df_wrike,how='left',left_on=df['issue'], right_on=df_wrike['Issue key'])
df_n['Baseline Create Date'].fillna(df_n['created'],inplace=True)
dfz= df_n[(df_n.status == "Backlog")  & (df_n.issuetype != "Task")]
dff=dfz['Baseline Create Date']
import numpy as np
mean = (np.array(dff, dtype='datetime64[s]')
        .view('i8')
        .mean()
        .astype('datetime64[s]'))
hh=pd.to_datetime(date_1)-pd.to_datetime(mean)
avgageq=hh.days #avgageq

dfa=pd.to_datetime((dfz['Baseline Create Date']))
kj=(pd.to_datetime(date_1)-dfa).sum()
avgagequeue=kj.days/len(dfa)
j=df[(df.resolvdate =='none') & (df.issuetype != "Task")]
g=j[j['custombaselinestart'] !='none']
s=(pd.to_datetime(date_1)-pd.to_datetime(g['custombaselinestart']))
pp=s.sum()
pp1=pp.days
avgagewip=pp1/len(s) #avgagewip

df1 = df[(df.resolution == "Done") & (df.issuetype != "Task")]
date_2=datetime.date.fromordinal(datetime.date.today().toordinal()-1)
df111=df1[(pd.to_datetime(df1['resolvdate'])<pd.to_datetime(date_1)) & (pd.to_datetime(df1['resolvdate'])>pd.to_datetime(date_2))]
dailycomplete=df111.count().issue #dailycomplete

ts='9/27/2017'
jj=df[(df['issuetype']!='Subtask') & (df['issuetype']!='Epic')  & (df.issuetype != "Task") & (pd.to_datetime(df['created'])>=pd.to_datetime(ts))]
ff1=jj[jj['custombaselinestart'] !='none']

jj1=df_n[(df_n['issuetype']!='Subtask') & (df.issuetype != "Task") & (df_n['issuetype']!='Epic') & (pd.to_datetime(df_n['created'])>pd.to_datetime(ts))]
ff3=jj1[jj1['custombaselinestart'] !='none']

a=pd.to_datetime(ff1['custombaselinestart'])-pd.to_datetime(ff3['Baseline Create Date'])
c=a.sum()
histavg_q=c.days/len(a) #historical avg queue time

df45=df[df.resolvdate !='none'].custombaselinestart
dfggg=df45[df45!='none']
import numpy as np

mean1 = (np.array(dfggg, dtype='datetime64[s]')
        .view('i8')
        .mean()
        .astype('datetime64[s]'))
df46= df[(df.resolvdate !='none')]
mean2 = (np.array(df46.resolvdate, dtype='datetime64[s]')
        .view('i8')
        .mean()
        .astype('datetime64[s]'))

zz=pd.to_datetime(mean2)-pd.to_datetime(mean1)
avgwip_cycletime=zz.days

#wip status breakdown
df3 = df[(df.status == "Investigation")  & (df.issuetype != "Task")].count()
inv_status=df3['issue']    #investigation status count

df4 = df[(df.status == "SUBLET: INVESTIGATION") & (df.issuetype != "Task")].count()
sub_inv_status=df4['issue']

df5 = df[(df.status == "In Development") & (df.issuetype != "Task")].count()
dev_status=df5['issue']

df6 = df[(df.status == "SUBLET: APPROVAL")  & (df.issuetype != "Task")].count()
sub_dev_status=df6['issue']

df7 = df[(df.status == "In Validation")  & (df.issuetype != "Task")].count()
val_status=df7['issue']

df8 = df[(df.status == "SUBLET: VALIDATION") & (df.issuetype != "Task")].count()
sub_val_status=df8['issue']

df9 = df[(df.status == "Product Manager Review") & (df.status == "In Review") ].count()
df11=df9
tech_pub_status=df11['issue']

df12 = df[(df.status == "Waiting for Documentation") & (df.issuetype != "Task")].count()
sublet_status_tech=df12['issue'] #sublet technical publications count

#wip type breakdown
df13 = df[(df.issuetype == "Repair Procedure Development") & (df.resolvdate =='none') & (df.status != "Triage") & (df.status != "Backlog")].count()
repproc_type_misc=df13['issue'] 

df14 = df[(df.issuetype == "Documentation") & (df.resolvdate =='none') & (df.status != "Triage") & (df.status != "Backlog")].count()
tech_type_misc=df14['issue'] 

df15 = df[(df.issuetype == "Tooling Request") & (df.resolvdate =='none') & (df.status != "Triage") & (df.status != "Backlog")].count()
tool_type_misc=df15['issue'] 

df16 = df[(df.issuetype == "Correction") & (df.resolvdate =='none') & (df.status != "Triage") & (df.status != "Backlog")].count()
syscorr_type_misc=df16['issue'] 

df17 = df[(df.issuetype == "Miscellaneous") & (df.resolvdate =='none') & (df.status != "Triage") & (df.status != "Backlog")].count()
wip_type_misc=df17['issue']

#queue type breakdown
df30 = df[(df.issuetype == "Repair Procedure Development") & (df.resolvdate =='none') & (df.status == "Triage")].count()
df31= df[(df.issuetype == "Repair Procedure Development") & (df.resolvdate =='none')& (df.status == "Backlog")].count()
todayq_rep_proc=df30+df31

todayq_rep_proc=todayq_rep_proc.issue
df32= df[(df.issuetype == "Documentation") & (df.resolvdate =='none')& (df.status == "Backlog")].count()
df33= df[(df.issuetype == "Documentation") & (df.resolvdate =='none')& (df.status == "Triage")].count()
todayq_technotes=df32+df33

todayq_technotes=todayq_technotes.issue
df34= df[(df.issuetype == "Tooling Request") & (df.resolvdate =='none')& (df.status == "Backlog")].count()
df35= df[(df.issuetype == "Tooling Reques") & (df.resolvdate =='none')& (df.status == "Triage")].count()
todayq_tooling=df34+df35
todayq_tooling=todayq_tooling.issue

df36= df[(df.issuetype == "Correction") & (df.duedate =='none')& (df.status == "Backlog")].count()
df37= df[(df.issuetype == "Correction") & (df.duedate =='none')& (df.status == "Triage")].count()
todayq_sys_corr=df36+df37
todayq_sys_corr=todayq_sys_corr.issue

df38= df[(df.issuetype == "Miscellaneous") & (df.resolvdate =='none')& (df.status == "Backlog")].count()
df39= df[(df.issuetype == "Miscellaneous") & (df.resolvdate =='none')& (df.status == "Triage")].count()
todayq_misc=df38+df39
todayq_misc=todayq_misc.issue

df40= df[(df.issuetype == "Work Request") & (df.resolvdate =='none')& (df.status == "Backlog")].count()
df41= df[(df.issuetype == "Work Request") & (df.resolvdate =='none')& (df.status == "Triage")].count()
todayq_wrkreq=df40+df41
todayq_wrkreq=todayq_wrkreq.issue

df_daily=pd.DataFrame(
    {'date_1': date_1,'sublet_status_tech':sublet_status_tech,'tech_pub_status': tech_pub_status,'sub_val_status':sub_val_status,'val_status':val_status,'sub_dev_status':sub_dev_status,'dev_status':dev_status,'sub_inv_status':sub_inv_status,'inv_status':inv_status,'wip_type_misc':wip_type_misc,'syscorr_type_misc':syscorr_type_misc,'tool_type_misc':tool_type_misc,'tech_type_misc':tech_type_misc,'repproc_type_misc':repproc_type_misc,'todayq_misc':todayq_misc, 'todayq_sys_corr':todayq_sys_corr,'todayq_tooling':todayq_tooling,'todayq_technotes':todayq_technotes ,'todayq_rep_proc':todayq_rep_proc ,'todayq_wrkreq':todayq_wrkreq},index=[0])

import pymysql
dbPassword      = "WRSFE3432FWRDF3@#"
dbName          = "rshinyapps"
connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

                                     db=dbName)
cursorObject = connectionObject.cursor() 

cursorObject.execute("insert into abc_Historical VALUES('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s','%s','%s','%s')" % (date_2, daily_queue , dailywip, avgageq,avgagewip,histavg_q,avgwip_cycletime,dailycomplete,inv_status,sub_inv_status,dev_status,sub_dev_status,val_status,sub_val_status,tech_pub_status,sublet_status_tech))
connectionObject.commit()

import sqlalchemy
month=(pd.to_datetime(df_n[df_n.issuetype != "Task"]['Baseline Create Date'])).dt.month
year=(pd.to_datetime(df_n['Baseline Create Date'])).dt.year
gg=df_n['Baseline Create Date'][pd.to_datetime(df_n['Baseline Create Date']).dt.year>=2018].groupby([year.rename('yearr'),month.rename('monthh')]).agg('count')
df_m=df_n[df_n['resolvdate']!='none']
dfff=df_m[(df_m['issuetype'] != "Task") & (df_m['resolution']=="Done")]
month1=(pd.to_datetime(dfff['resolvdate'])).dt.month
year1=(pd.to_datetime(dfff['resolvdate'])).dt.year
jj=dfff['resolvdate'][pd.to_datetime(dfff['resolvdate']).dt.year>=2018].groupby([year1.rename('yearrr'),month1.rename('monthhh')]).agg('count')
d = {'submit' :gg,'resolve' : jj}
dfp = pd.DataFrame(d)
ds=dfp.reset_index()
df_daily.to_sql(name=abc_daily', con=engine,if_exists='replace', index=True,index_label=None, chunksize=None)
ds.to_sql(name=abc, con=engine,if_exists='replace', index=True,index_label=None, chunksize=None)

