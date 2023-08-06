# Django数据库迁移优化（目前只完善MySQL）

## 主要功能

+ 支持写入表注释及字段注释

+ 支持写入字段默认值

+ 常用字段数据模型基类 `django_kelove_db.abstract_models`

## 使用示例

+ 修改django配置文件 ENGINE 为 django_kelove_db.backends.mysql

+ 配置 `INCLUDE_DEFAULT` (可选)，示例如下

```
DATABASES = {
    'default': {
        'ENGINE': 'django_kelove_db.backends.mysql',
        'NAME': 'django_kelove',
        'USER': 'django_kelove',
        'PASSWORD': 'django_kelove',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'INCLUDE_DEFAULT': lambda model, field, include_default, connection: False if field.db_parameters(
            connection=connection
        )['type'] in ['longtext', 'longblob'] else True
    }
}

KELOVE_DATABASES = {
    'FOREIGN_DELETE_TYPE': 'django.db.models.deletion.PROTECT',
    'DB_CONSTRAINT': False,
    'DB_CONSTRAINT_USER': False,
    'STATUS_CHOICES': [(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')]
}

```
