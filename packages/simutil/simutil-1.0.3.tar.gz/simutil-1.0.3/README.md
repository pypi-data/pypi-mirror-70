# SimUtil

python容器& libs


# 安装
```
pip install simutil
```

# 初始化
你需要在你的项目根目录下创建一个.env文件，内容如下:

``` python
[environment]                           # 环境变量       
ENVIRONMENT = dev                       # 项目环境

#日志配置
LOG_DEBUG = true                
LOG_LEVEL = DEBUG
LOG_PATH = /Users/**/

# redis配置
REDIS_HOST=127.0.0.1                     
REDIS_PORT=6379                          
REDIS_PASSWORD =                         
REDIS_DB=0                               

# oss配置
OSS_ACCESS_DOMAIN=**                     
OSS_ACCESS_KEY=key                       
OSS_ACCESS_SECRET=secret                 
OSS_BUCKET_NAME=bucket_name              
OSS_END_POINT=endpoint

```

# 使用

容器初始化

``` python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from simpysql.DBModel import DBModel

class ModelDemo(DBModel):
    
    __basepath__ = '/home/project/'             # .env 文件路径
    #__database__ = 'default'                   # 库选择， 没有该属性，则默认default库
    __tablename__ = 'lh_test'                   # table name
    __create_time__ = 'create_time'             # 自动添加创建时间字段create_time(精确到秒)， 设置为None或者删除该属性，则不自动添加 
    __update_time__ = 'update_time'             # 自动更新时间字段update_time(精确到秒)， 设置为None或者删除该属性，则不自动更新
    columns = [                                 # table columns
        'id',
        'name',
        'token_name',
        'status',
        'create_time',
        'update_time',
    ]

    # 可以通过该方法设置自动添加时间字段的格式
    # def fresh_timestamp(self):
    #     return datetime.datetime.now().strftime("%Y%m%d")
```

## 操作实例

```python
ModelDemo().where('id', 4).select('id', 'name').take(5).get()
```

## 其他
欢迎志同道合的朋友一起参与本项目开发SQLServer、PostgreSQL开发, 联系方式: 490573621@qq.com
