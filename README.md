### es-handle - 使用 python client 对 ElasticSearch 进行常用的增删改查操作

#### 声明
* 运行环境：python 2.7
* 依赖：elasticsearch ，安装依赖：pip install elasticsearch
* windows 和 linux 环境均已通过测试 
* 如果有问题，请及时反馈给我

#### 完成清单
* 增删改查操作：√ 
* -h 帮助信息：√
* 优化精简 printx 代码：×


#### 增删改查支持的参数组合


| | 增（insert） | 删（delete） | 改（update） | 查（search） |
| -------- | -------- | -------- | -------- | -------- |
| index,type,id | √     | √     | √     | √     |
| index,type    | √     | √     | ×     | √     |
| index         | √     | √     | ×     | √     |
| null          | ×     | ×     | ×     | √     |

    
#### 各参数组合使用的 ElasticSearch Python Client API

| | 增（insert） | 删（delete）       | 改（update） | 查（search） |
| -------- | -------- | -------------| -------- | -------- |
| index,type,id | es.index()         | es.delete()          | es.update() | es.get()    |
| index,type    | es.index()         | es.delete_by_query() | ×           | es.search() |
| index         | es.indices.create()| es.indices.delete()  | ×           | es.search() |
| null          | ×                  | ×                    | ×           | es.search() |

#### Usage
```
命令格式：
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
cat    - 查看 ElasticSearch 指定状态
    默认查看当前所有索引

例子：
# 查看 ElasticSearch 连接状态
es.py localhost

# 增(insert)
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

# 删(delete)
# 1. 删除指定 id 的文档
es.py localhost delete test_index test_type 1
# 2. 删除整个类型(type)
es.py localhost delete test_index test_type
# 3. 删除整个索引(index)
es.py localhost delete test_index

# 改(update)
# 1. 更新指定id的文档内容(更新的内容应包含在 "doc" 关键字中)
es.py localhost update test_index test_type 1
{
    "doc": {
        "content" : "hello world"
    }
}

# 查(search)
# 1. 查询指定id的文档内容
es.py localhost search test_index test_type 1
# 2. 查询指定type
es.py localhost search test_index test_type
# 3. 查询指定index
es.py localhost search test_index
# 4. 查询所有index
es.py localhost search

# 看(cat)
# 1. 查看 ElasticSearch 所有索引
es.py localhost cat
```

#### 参考资料
ElasticSearch Python Client API（官方文档）  
http://elasticsearch-py.readthedocs.io/en/master/api.html

python操作Elasticsearch (一、例子)  
http://www.cnblogs.com/yxpblog/p/5141738.html

elasticsearch的python增删查改实例分析  
http://www.cnblogs.com/skying555/p/6297814.html

How to update a document using elasticsearch-py?（es.update() 中 body 的格式）  
https://stackoverflow.com/questions/30598152/how-to-update-a-document-using-elasticsearch-py

python中json.dumps使用的坑以及字符编码（json.dumps() 保持真实字符，方便 encode）  
http://www.cnblogs.com/stubborn412/p/3818423.html

怎么知道Python Shell的编码是什么（获得当前shell的编码）  
https://zhidao.baidu.com/question/620013490340115212.html

Elasticsearch5.4 删除type（ElasticSearch 删除整个 type）  
http://blog.csdn.net/leafage_m/article/details/74011357

How to prettyprint a JSON file?（json.dumps() 以便于观看的方式转换 - prettyprint）  
https://stackoverflow.com/questions/12943819/how-to-prettyprint-a-json-file

python类型比较的3种方式（正确比较 if type(s) == 'str'）  
http://blog.csdn.net/five3/article/details/8098556

[解决办法]Python中使用json.loads解码字符串时出错：ValueError: Expecting property name: line 1 column 2 (char 1)（json.loads不能处理单引号的解决办法）  
http://blog.csdn.net/sinsa110/article/details/51189456





