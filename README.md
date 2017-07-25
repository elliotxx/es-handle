### es-handle - 使用 python client 对 ElasticSearch 进行常用的增删改查操作

#### 完成清单
* 增删改查操作：√ 
* -h 帮助信息：×
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





