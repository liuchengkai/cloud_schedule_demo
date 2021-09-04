from flask import Flask
from flask import request
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(host="localhost", port=9200)

app = Flask(__name__, static_folder='./', static_url_path='/cloud_schedule')

#获取es数据量
count = es.search(index='noteinfo',doc_type = "data")['hits']['total']['value']
query = es.search(index='noteinfo',doc_type = "data",size = count)
results = query['hits']['hits']

idnumlist = []
for result in results:
    idnumlist.append(result['_source']['idnum'])

@app.route('/')
def hello():
    return "Sivan is the best"


@app.route('/getAll',methods = ['GET'])
def getAll():
    body = {
        "query":{
            "match_all":{}
        }
    }
    
    count = es.search(index='noteinfo',doc_type = "data")['hits']['total']['value']
    query = es.search(index='noteinfo',doc_type = "data", body=body,size=count)
    results = query['hits']['hits']

    resultlist = []
    for result in results:
        resultlist.append(result['_source']) 

    resultjson = json.dumps(resultlist,ensure_ascii = False)
    
    return resultjson    
    
@app.route('/addInfo',methods = ['POST'])
def add():
    #idnumlist从开始运行就一直存在 
    global idnumlist 
    #print(request.form.get('event'))
    print(request.get_json())
    event = request.get_json()['event']
    print(event)
    start_time = request.get_json()['start_time']
    print(start_time)
    end_time = request.get_json()['end_time']
    print(end_time)
    color = request.get_json()['color']
    print(color)
    
    '''
    event = request.form.get('event')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    color = request.form.get('color')
    '''
    print(event)
    #idnum = "1"
    idnum = str(int(idnumlist[len(idnumlist)-1])+1)
    idnumlist.append(idnum)
    print(idnum)
    es.index(index="noteinfo",
            doc_type = "data",
            body = {    "idnum":idnum,
                        "event":event,
                        "startTime":start_time,
                        "endTime":end_time,
                        "color":color})
    
    body = {
        "query":{
            "match_all":{}
        }
    }
    
    '''
    count = es.search(index='noteinfo',doc_type = "data")['hits']['total']['value']
    query = es.search(index='noteinfo',doc_type = "data", body=body,size=count)
    results = query['hits']['hits']

    resultlist = []
    for result in results:
        resultlist.append(result['_source']) 

    
    resultjson = json.dumps(resultlist,ensure_ascii = False)

    return resultjson
    '''
    return idnum    
    
@app.route('/delete/<int:idnum>',methods = ['DELETE'])
def delete(idnum):
    idnum = str(idnum)
    quest = {'query': {'match': {'idnum': idnum}}}
    es.delete_by_query(index='noteinfo', body=quest, doc_type='data')
    
    body = {
        "query":{
            "match_all":{}
        }
    }
    
    count = es.search(index='noteinfo',doc_type = "data")['hits']['total']['value']

    query = es.search(index='noteinfo',doc_type = "data", body=body,size=count)

    results = query['hits']['hits']

    resultlist = []
    for result in results:
        resultlist.append(result['_source']) 

    
    resultjson = json.dumps(resultlist,ensure_ascii = False)
    
    return resultjson


@app.route('/update/<int:idnum>',methods = ['PUT'])
def update(idnum):

    global idnumlist 
    #print(request.form.get('event'))
    idnum = str(idnum)
    #print(idnum)
    #print(request.get_json()['update_event'])
    #finalrequest = json.dumps(request.get)
    
    #适用于PUT请求
    event = request.get_json()['update_event']
    start_time = request.get_json()['update_start_time']
    end_time = request.get_json()['update_end_time']
    color = request.get_json()['update_color']
    
    '''
    #适用于GET请求
    event = request.form.get('update_event')
    start_time = request.form.get('update_start_time')
    end_time = request.form.get('update_end_time')
    color = request.form.get('update_color')
    '''
    #print(event)
    
    quest = {'query': {'match': {'idnum': idnum}}}
    query = es.search(index='noteinfo',doc_type = "data", body=quest)
    if query['hits']['total']['value'] !=0:
        #print(query)
        realid = query['hits']['hits'][0]['_id']
        
        quest = {
                    'doc': {
                        'idnum': idnum,
                        'event':event,
                        'startTime':start_time,
                        'endTime':end_time,
                        'color':color
                    }}
        #修改数据
        es.update(index='noteinfo', id = realid, doc_type='data',body=quest)
    
        body = {
            "query":{
                "match_all":{}
            }
        }
        
        count = es.search(index='noteinfo',doc_type = "data")['hits']['total']['value']
    
        query = es.search(index='noteinfo',doc_type = "data", body=body,size=count)
    
        results = query['hits']['hits']
        
        resultlist = []
        for result in results:
            resultlist.append(result['_source']) 
        
        resultjson = json.dumps(resultlist,ensure_ascii = False)
        
        return resultjson
    else:
        return "[{result:0}]"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
    