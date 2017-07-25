#coding=utf8
'''
使用 python client 对 ElasticSearch 进行常用的增删改查操作
'''
from elasticsearch import Elasticsearch
import sys
import json

argname_list = ['cmd','addr','op','index','type','id']
default_host = '127.0.0.1'
default_port = '9200'

# 参数数量可能的范围 [Argument_Num_Min_Limit,Argument_Num_Max_Limit]
Argument_Num_Min_Limit = 2
Argument_Num_Max_Limit = 6

# 编码信息（shell编码 和 文件编码）
input_encoding  = sys.stdin.encoding
output_encoding = sys.stdout.encoding
file_encoding   = 'utf8'


def printx(s, end = '\n'):
    '''通用输出'''
    if isinstance(s,str):
        s = s.decode(file_encoding)
        s += end
        s = s.encode(output_encoding)
        sys.stdout.write(s)
    elif isinstance(s,dict):
        s = json.dumps(s, indent=4, ensure_ascii=False)
        s += end
        s = s.encode(output_encoding)
        sys.stdout.write(s)
    else:
        print s


def getArguments():
    '''获取参数'''
    args = {'op':None}
    args_num = len(sys.argv)

    # 获得对应参数
    for i in range(1,args_num):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            args['help'] = argname_list[i-1]
            break
        args[argname_list[i]] = sys.argv[i]

    # 简单的参数验证
    if not (Argument_Num_Min_Limit <= args_num <= Argument_Num_Max_Limit):
        raise Exception,'参数错误：提供了错误的参数个数'

    # 参数 addr 部分的处理
    if not args.has_key('addr'):
        # 参数中不存在地址信息，采用默认地址和端口
        args['host'] = default_host
        args['port'] = default_port
    elif args['addr'].find(':')==-1:
        # 参数中只存在地址的 host 信息，采用默认端口
        args['host'] = args['addr']
        args['port'] = default_port
    else:
        # 参数中指定了地址的 host 和 port 信息
        args['host'],args['port'] = args['addr'].split(':')

    return args


def connElasticsearch(args):
    '''尝试连接 ElasticSearch'''
    es = Elasticsearch(['%s:%s'%(args['host'],args['port'])])
    try:
        # 尝试连接
        es.info()
    except Exception,e:
        raise Exception,'ElasticSearch <%s:%s> 连接失败！'%(args['host'],args['port'])
    return es


def getBody():
    '''获得请求体'''
    blank_line_num = 0
    body = ''
    while(blank_line_num < 2):
        s = raw_input('...')
        body += s + '\n'
        blank_line_num = blank_line_num + 1 if s=='' else 0
    body = body.strip().replace("'","\"").decode(input_encoding)
    body = json.loads(body)
    return body


def Insert(es,args):
    '''在 ElasticSearch 中插入数据'''
    if args.has_key('index'):
        if args.has_key('type'):
            printx('请指定文档内容（JSON格式）：')
            args['body'] = getBody()
            if args.has_key('id'):
                # 提供参数：index, type, id
                # 插入指定 id 的文档
                res = es.index(index = args['index'], doc_type = args['type'], id = args['id'], body = args['body'])
            else:
                # 提供参数：index, type
                # 插入指定文档，id自动生成
                res = es.index(index = args['index'], doc_type = args['type'], body = args['body'])
        else:
            # 提供参数：index
            printx('请指定待创建 index 的 settings 和 mappings（JSON格式）：')
            args['body'] = getBody()
            res = es.indices.create(index = args['index'], body = args['body'])
        printx('插入结果：')
        printx(res)
    else:
        # 什么参数都没提供
        raise Exception,'参数错误：没有插入对象'


    
def Delete(es,args):
    '''在 ElasticSearch 中删除数据'''
    if args.has_key('index'):
        if args.has_key('type'):
            if args.has_key('id'):
                # 提供参数：index, type, id
                # 删除指定 id 的文档
                res = es.delete(index = args['index'], doc_type = args['type'], id = args['id'])
            else:
                # 提供参数：index, type
                # 删除指定 type
                res = es.delete_by_query(index = args['index'], doc_type = args['type'], body={"query":{"match_all":{}}})
        else:
            # 提供参数：index
            # 删除指定 index
            res = es.indices.delete(index = args['index'])
        printx('删除结果：')
        printx(res)
    else:
        # 什么参数都没提供
        raise Exception,'参数错误：没有删除对象'

    
def Update(es,args):
    '''在 ElasticSearch 中更新数据'''
    if args.has_key('index'):
        if args.has_key('type'):
            if args.has_key('id'):
                # 提供参数：index, type, id
                # 更新指定 id 的文档
                printx('请指定更新内容（JSON格式）：')
                args['body'] = getBody()
                res = es.update(index = args['index'], doc_type = args['type'], id = args['id'], body = args['body'])
                printx('更新结果：')
                printx(res)
            else:
                # 提供参数：index, type
                raise Exception,'参数错误：除了“索引”名和“类型”名，您还需要指定文档的“id”'
        else:
            # 提供参数：index
            raise Exception,'参数错误：除了“索引”名，您还需要指定文档的“类型”名和“id”'
    else:
        # 什么参数都没提供
        raise Exception,'参数错误：没有更新对象'

    
def Search(es,args):
    '''在 ElasticSearch 中查询数据'''
    if args.has_key('index'):
        if args.has_key('type'):
            if args.has_key('id'):
                # 提供参数：index, type, id
                # 查询指定 id 的文档
                res = es.get(index = args['index'], doc_type = args['type'], id = args['id'])
            else:
                # 提供参数：index, type
                # 查询指定 type
                res = es.search(index = args['index'], doc_type = args['type'], body={"query":{"match_all":{}}})
        else:
            # 提供参数：index
            # 查询指定 index
            res = es.search(index = args['index'], body={"query":{"match_all":{}}})
    else:
        # 什么参数都没提供
        # 查询所有索引简略信息
        res = es.search(body={"query":{"match_all":{}}})
    printx('查询结果：')
    printx(res)


def Info(es,args):
    '''获取 ElasticSearch 连接信息'''
    printx('Elasticsearch <%s:%s> 连接信息：'%(args['host'],args['port']))
    printx(es.info())


def Help(args):
    '''帮助信息'''
    h = {
        'basic' : '''命令格式：
es.py [-h] IP[:port] [-h|option] [-h|index] [type] [id]

option:
insert - 向 ElasticSearch 插入数据
    支持 插入指定id的文档、插入不指定id的文档、仅创建 index 三种格式
delete - 从 ElasticSearch 删除数据
    支持 删除文档、删除整个类型(type)、删除整个索引(index) 三种格式
    注意：如果类型中数据过多，删除操作会异步进行
update - 更新指定 ElasticSearch 文档内容
    支持 更新指定id的文档内容 一种格式
    注意：更新的内容应包含在 "doc" 关键字中，例：
    es.py localhost update test_index test_type 1
    {
       "doc":{
           "content" : "hello world"
       }
    }
    如此，索引 test_index 的类型 test_type 中 id 为 1 的文档的
    content 字段内容更新为"hello world"
search - 查询 ElasticSearch 指定内容
    支持 查询指定id的文档内容、查询指定type、查询指定index、
    查询所有index 四种格式
        ''',
        'addr' : '''# 查看 ElasticSearch 连接状态
es.py localhost
        ''',
        'insert' : '''# 增(insert)
# 1. 插入指定 id 的文档
es.py localhost:9200 insert test_index test_type 1
{
    "title" : "Good morning",
    "content" : "hello"
}
# 2. 插入不指定 id 的文档
es.py localhost insert test_index test_type
输入同上...
# 3. 创建 index
es.py localhost insert test_index_2
{
    "settings" : {
        "number_of_shards" : 1
    },
    "mappings" : {
        "test_type_2" : {
            "properties" : {
                "title" : { "type" : "text" },
                "content" : { "type" : "text" }
            }
        }
    }
}
        ''',
        'delete' : '''# 删(delete)
# 1. 删除指定 id 的文档
es.py localhost delete test_index test_type 1
# 2. 删除整个类型(type)
es.py localhost delete test_index test_type
# 3. 删除整个索引(index)
es.py localhost delete test_index
        ''',
        'update' : '''# 改(update)
# 1. 更新指定id的文档内容(更新的内容应包含在 "doc" 关键字中)
es.py localhost update test_index test_type 1
{
    "doc": {
        "content" : "hello world"
    }
}
        ''',
        'search' : '''# 查(search)
# 1. 查询指定id的文档内容
es.py localhost search test_index test_type 1
# 2. 查询指定type
es.py localhost search test_index test_type
# 3. 查询指定index
es.py localhost search test_index
# 4. 查询所有index
es.py localhost search
        '''
    }
    printx(h['basic'])
    printx('例子：')
    if   args['help'] == 'cmd':
        printx(h['addr'])
        printx(h['insert'])
        printx(h['delete'])
        printx(h['update'])
        printx(h['search'])
    elif args['help'] == 'addr':
        printx(h['addr'])
    elif args['help'] == 'op':
        printx(h[args['op']])


def main():
    '''主函数'''
    # 获得参数
    args = getArguments()
    # 判断是否需要输出帮助信息
    if args.has_key('help'):
        Help(args)
    else:
        # 尝试连接 ElasticSearch
        es = connElasticsearch(args)
        # 进行增删改查操作
        if args['op'] == 'insert':
            Insert(es,args)
        elif args['op'] == 'delete':
            Delete(es,args)
        elif args['op'] == 'update':
            Update(es,args)
        elif args['op'] == 'search':
            Search(es,args)
        elif args['op'] ==  None:
            Info(es,args)
        else:
            pass


if __name__=='__main__':
    # main()
    try:
        main()
    except Exception,e:
        printx('[ERROR]: ',end='')
        printx(str(e))
    

