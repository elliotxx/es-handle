### es-handle - 使用 python client 对 ElasticSearch 进行常用的增删改查操作

#### 完成清单
* 增删改查操作：已完成
* -h 帮助信息：未完成
* 优化精简 printx 代码：未完成


#### 增删改查支持的参数组合


| | 增（insert） | 删（delete） | 改（update） | 查（search） |
| -------- | -------- | -------- | -------- | -------- |
| index,type,id | √     | √     | √     | √     |
| index,type    | √     | √     | ×     | √     |
| index         | √     | √     | ×     | √     |
| null          | ×     | ×     | ×     | ×     |

    
#### 各参数组合使用的 ElasticSearch Python Client API

| | 增（insert） | 删（delete） | 改（update） | 查（search） |
| -------- | -------- | -------- | -------- | -------- |
| index,type,id | es.index()     | es.delete()          | es.update() | es.get()    |
| index,type    | es.index()     | es.delete_by_query() | ×           | es.search() |
| index         | es.create()    | es.indices.delete()  | ×           | es.search() |
| null          | ×              | ×                    | ×           | ×           |
