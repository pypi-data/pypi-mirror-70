from sqlalchemy import MetaData, text, and_
from sqlalchemy.sql.expression import select, delete
from contextlib import contextmanager
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import datetime
from .keywords import keywords, operators, quotes, start_quotes


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                fields[field] = obj.__getattribute__(field)
            return fields

        return json.JSONEncoder.default(self, obj)


class Dict(dict):   # dynamic property support, such as d.name
    """
    dict升级版本，支持动态属性操作， 动态属性增加 d.<prop_name> = xx
    """
    def __getattr__(self, name):
        if name in self: return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        self.pop(name, None)

    def __getitem__(self, key):
        if key not in self: return None
        return dict.__getitem__(self, key)


config = Dict()     # default to mysql


def default_escape(key, start='"', end='"'):
    """
    对SQL字段转义
    1）关键词不转义
    2）key为方法调用不转义
    3）xx.yyy带表前缀分裂转义
    :param key:
    :param start:
    :param end:
    :return:
    """
    if not key:
        return key
    if key[0] in quotes:
        return key
    if '(' in key:  # function
        return key
    if '.' in key:
        bb = []
        for b in key.split('.'):
            if not b:
                bb.append(b)
            else:
                bb.append(start+b+end)
        return '.'.join(bb)
    return start+key+end


def mssql_escape(key):
    return default_escape(key, start='[', end=']')


def mysql_escape(key):
    return default_escape(key, start='`', end='`')


def escape(key):
    func = config.escape or default_escape
    return func(key)


def default_page(sql, page, limit):
    page = int(page)
    limit = int(limit)
    return f"{sql} limit {limit} offset {(page-1)*limit}"


def mssql_page(sql, page, limit):
    page = int(page)
    limit = int(limit)
    return f"{sql} OFFSET {(page-1)*limit} ROWS FETCH NEXT {limit} ROWS ONLY"


def sql_page(sql, page, limit):
    func = config.sql_page or default_page
    return func(sql, page, limit)


def default_count(sql):
    return f"select count(0) as total from ({sql}) as t"


def mssql_count(sql):
    return f"select count(0) as total from ({sql} OFFSET 0 ROWS) as t"


def sql_count(sql):
    func = config.sql_count or default_count
    return func(sql)


class Db:
    def __init__(self, engine, reflect=True, force_escape_sql=False):
        """
        数据库操作实用类，提供基础的增删改查，分页。事务支持。
        在同一个Session中的SQL序列，处于一个事务中。不同的Session则产生不同的事务执行。
        典型代码
        with db.session() as s:
            s.execute(xxx)
            s.execute(yyy)

        :param engine: SQLAlchemy Engine对象
        :param reflect: 是否读取反射信息--表、字段
        :param force_escape_sql: 是否强制对所有SQL转义处理
        """
        self.engine = engine
        self.force_escape_sql = force_escape_sql

        self.dialect = Dict()
        self.dialect.escape = default_escape
        self.dialect.sql_count = default_count
        self.dialect.sql_page = default_page

        if self.is_mssql():
            # change global, may remove
            config.escape = mssql_escape
            config.sql_count = mssql_count
            config.sql_page = mssql_page

            self.dialect.escape = mssql_escape
            self.dialect.sql_count = mssql_count
            self.dialect.sql_page = mssql_page

        if self.is_mysql():
            config.escape = mysql_escape
            self.dialect.escape = mysql_escape

        self.tables = {}
        self.meta = MetaData()
        if reflect:
            self.reflect()

    def reflect(self, **kwargs):
        """
        反射读取数据库信息，表结构
        :param kwargs:
        :return:
        """
        self.meta.reflect(bind=self.engine, **kwargs)
        self.tables = self.meta.tables

    def escape(self, key):
        return self.dialect.escape(key)

    def escape_sql(self, sql):
        res = []
        i = 0
        curr = ''
        curr_is_op = True
        last_quote = None  # 2种状态, None, '"`[
        while i < len(sql):
            if sql[i] in quotes:
                if last_quote:
                    start_quote = quotes[sql[i]]
                    curr += sql[i]
                    if last_quote == start_quote:
                        res.append((curr, True))
                        curr = ''
                        last_quote = None
                    i += 1
                    continue
                last_quote = sql[i]
                if last_quote not in start_quotes:
                    last_quote = None

            if last_quote:
                curr += sql[i]
                i += 1
                continue

            if sql[i] in operators:
                if not curr_is_op:
                    raw = False
                    if curr.isdigit():
                        raw = True
                    res.append((curr, raw))
                    curr = sql[i]
                    curr_is_op = True
                    i += 1
                    continue
                curr += sql[i]
                i += 1
                continue
            if curr_is_op:
                res.append((curr, True))
                curr = ''
            curr_is_op = False
            curr += sql[i]
            i += 1

        if curr != '':
            raw = curr_is_op
            if not curr_is_op:
                if curr.isdigit():  # 以数字结尾
                    raw = True
            res.append((curr, raw))
        escaped = ''
        for r in res:
            k = r[0]
            if r[1]:
                escaped += k
                continue

            if k.lower() in keywords:
                escaped += k
                continue
            if k.startswith('$') or k.startswith(':'):
                escaped += k
                continue

            escaped += self.escape(k)
        return escaped

    def sql_page(self, sql, page, limit):
        return self.dialect.sql_page(sql, page, limit)

    def sql_count(self, sql):
        return self.dialect.sql_count(sql)

    def is_mssql(self):
        return 'mssql' in self.engine.name

    def is_mysql(self):
        return 'mysql' in self.engine.name

    def in_clause(self, key, param_array):
        """
        SQLServer使用pyodbc的时候in条件不友好需要特别操作
        :param key:
        :param param_array:
        :return:
        """
        if self.is_mysql():
            real_key = f":{key}"
            params = {key: param_array}
            return real_key, params

        i = 0
        params = {}
        in_key = []
        for d in param_array:
            sub_key = f"{key}_{i}"
            i += 1
            params[sub_key] = d
            in_key.append(f":{sub_key}")

        real_key = f"({','.join(in_key)})"
        return real_key, params

    @contextmanager
    def session(self):
        """Provide a transactional scope around a series of operations."""

        sa_conn = self.engine.connect()

        tx = sa_conn.begin()
        try:
            connection = Connection(sa_conn, self)
            yield connection
            tx.commit()
        except:
            tx.rollback()
            raise
        finally:
            sa_conn.close()

    @contextmanager
    def connection(self):
        """Expose raw connection"""

        sa_conn = self.engine.connect()

        tx = sa_conn.begin()
        try:
            yield sa_conn
            tx.commit()
        except:
            tx.rollback()
            raise
        finally:
            sa_conn.close()

    def query_meta(self, sql, session=None, **kvargs):
        """
        从完整SQL执行结构中获取结果表结构信息 { 字段: {name: xx } }
        :param sql: 完整SQL
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :param kvargs:
        :return:
        """
        if session:
            return session.query_meta(sql, **kvargs)
        with self.session() as s:
            return s.query_meta(sql, **kvargs)

    def query(self, sql, converter=None, session=None, **kvargs):
        """
        执行完整SQL查询，返回对象列表。
        SQL中参数的格式: :<param_name>, 例如 :name 代表参数名为name
        :param sql: 完整SQL
        :param converter: 对每行数据转换对象的处理方法
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :param kvargs: SQL中的参数指定， 例如name='test'
        :return: 对象列表，无匹配则是空数组
        """
        if session:
            return session.query(sql, converter, **kvargs)
        with self.session() as s:
            return s.query(sql, converter, **kvargs)

    def query_page(self, sql, converter=None, session=None, **kvargs):
        """
        执行完整SQL查询，返回分页列表
        SQL中参数的格式: :<param_name>, 例如 :name 代表参数名为name

        :param sql: 完整SQL
        :param converter: 对每行数据转换对象的处理方法
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :param kvargs: SQL中的参数指定， 例如name='test'
        :param page: 第几页，从第1页开始计算，默认1
        :param limit: 每页大小，默认20
        :param do_count: 0--不计算总数, 1/None--计算总数和数据, 2--仅计算总数，不返回数据； 默认值：1/None
        :return: 分页数据 {'total': 1, 'page': 1, 'limit': 20, 'data': []}
        """
        if session:
            return session.query_page(sql, converter, **kvargs)
        with self.session() as s:
            return s.query_page(sql, converter, **kvargs)

    def query_one(self, sql, converter=None, session=None, **kvargs):
        """
        执行完整SQL查询查询单条记录，SQL中不限制记录数，方法中增加限制
        SQL中参数的格式: :<param_name>, 例如 :name 代表参数名为name
        :param sql: 完整SQL
        :param converter: 对每行数据转换对象的处理方法
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :param kvargs: SQL中的参数指定， 例如name='test'
        :return: 单个数据对象，或者None
        """
        if session:
            return session.query_one(sql, converter, **kvargs)
        with self.session() as s:
            return s.query_one(sql, converter, **kvargs)

    def execute(self, sql, session=None, **kvargs):
        """
        执行完整SQL，更新或者删除动作
        SQL中参数的格式: :<param_name>, 例如 :name 代表参数名为name
        :param sql: 完整SQL
        :param converter: 对每行数据转换对象的处理方法
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :param kvargs: SQL中的参数指定， 例如name='test'
        """
        if session:
            return session.execute(sql, **kvargs)
        with self.session() as s:
            return s.execute(sql, **kvargs)

    def add(self, table, json_data, session=None):
        """
        添加一条记录，指定表名，json数据中未能匹配的字段忽略
        :param table: 数据表名
        :param json_data: Key-Value数据
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :return: 返回过滤掉未能匹配的json数据+数据库生成的主键字段（默认id字段）
        """
        if session:
            return session.add(table, json_data)
        with self.session() as s:
            return s.add(table, json_data)

    def add_many(self, table, data, session=None):
        """
        指定表，批量增加多条记录，json数据中未能匹配的字段忽略
        :param table: 数据表名
        :param data: 对象列表，每个对象字段需要保持一致
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :return: 返回受影响的行数
        """
        if session:
            return session.add_many(table, data)
        with self.session() as s:
            return s.add_many(table, data)

    def update_many(self, table, data, keys=None, session=None):
        """
        指定表，批量更新多条记录，json数据中未能匹配的字段忽略
        :param table: 数据表名
        :param data: 对象列表，每个对象字段需要保持一致，需要提供主键数据
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :return: 返回受影响的行数
        """
        if session:
            return session.update_many(table, data, keys=keys)
        with self.session() as s:
            return s.update_many(table, data, keys=keys)

    def save_many(self, table, data,  overwrite=True, session=None):
        """
        批量保存记录，根据数据库主键自动判断是新增还是更新动作（目前支持MySQL）
        :param table: 数据表名
        :param data: 对象列表，每个对象字段需要保持一致，需要提供主键数据
        :param overwrite:  是否执行覆盖
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :return: 返回受影响的行数
        """
        if session:
            return session.save_many(table, data, overwrite=overwrite)
        with self.session() as s:
            return s.save_many(table, data, overwrite=overwrite)

    def execute_many(self, sql, data, session=None):
        """
        批量执行插入或者删除动作，数据列表中的每个记录需要保持一致格式
        :param sql: 完整的SQL，插入或者删除动作
        :param data: 对象列表，每个对象字段需要保持一致
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :return: 返回受影响的行数
        """
        if session:
            return session.execute_many(sql, data)
        with self.session() as s:
            return s.execute_many(sql, data)

    def merge(self, table, json_data, session=None):
        """
        根据提供的数据对象主键与表名执行更新动作，适合获取到数据库主键对象数据，内存更新后再次调用更新至DB
        :param table: 数据表名
        :param json_data: Key-Value数据
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :return: 返回过滤掉未能匹配的json数据+数据库生成的主键字段（默认id字段）
        """
        if session:
            return session.merge(table, json_data)
        with self.session() as s:
            return s.merge(table, json_data)

    def save(self, table, json_data, session=None):
        """
        插入或者新增记录
        此方法缺点是增加多了一次查询数据库的动作来判断数据是否存在
        相当于query_one + add / merge 结合动作
        :param table: 数据表名
        :param json_data: Key-Value数据
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :return: 返回包含数据库主键的对象
        """
        if session:
            return session.save(table, json_data)
        with self.session() as s:
            return s.save(table, json_data)

    def delete(self, table, key, session=None):
        """
        根据表和主键值删除记录
        :param table: 数据表名
        :param key: 主键值
        :param session: 链接Session，如果不提供则重新创建Session，在新的事务中执行
        :return: 影响的记录数
        """
        if session:
            return session.delete(table, key)
        with self.session() as s:
            return s.delete(table, key)


class Connection:
    def __init__(self, conn, db):
        self.connection = conn
        self.tables = db.tables
        self.db = db

    def query(self, sql, converter=None, **kvargs):
        return self._query(sql, converter, **kvargs)

    def query_page(self, sql, converter=None, **kvargs):
        page = kvargs.get('page') or 1
        limit = kvargs.get('limit') or 20
        do_count = kvargs.get('do_count') # 0--only data, 1/None--count + data, 2--only count
        if do_count is None:
            do_count = 1

        total, data = None, None
        if do_count >= 1:
            sql_c = self.db.sql_count(sql)
            res = self.query_one(sql_c, converter, **kvargs)
            total = res.total
        if do_count <= 1:
            sql_p = self.db.sql_page(sql, page, limit)
            sql_p = text(sql_p)
            data = self._query(sql_p, converter, **kvargs)
        return Dict({
            'total': total,
            'page': page,
            'limit': limit,
            'data': data
        })

    def query_meta(self, s, **kvargs):
        if isinstance(s, str):
            if self.db.force_escape_sql:
                s = self.db.escape_sql(s)
            s = text(s)

        rs = self.connection.execute(s, **kvargs)
        keys = rs._metadata.keys
        meta = Dict()
        for key in keys:
            m = meta[key] = Dict()
            m.name = key
        return meta

    def _query(self, s, converter=None, **kvargs):
        if isinstance(s, str):
            if self.db.force_escape_sql:
                s = self.db.escape_sql(s)
            s = text(s)

        rs = self.connection.execute(s, **kvargs)

        def c(row):
            r = Dict(row)
            if not converter:
                sub_dict = {}

                for name in r:
                    bb = name.split('.')  # handle . for layer object
                    key = None
                    if len(bb) > 1:
                        obj_name, key = bb
                        obj = sub_dict.get(obj_name)
                        if not obj:
                            sub_dict[obj_name] = obj = {}

                    v = r[name]
                    if isinstance(v, bytes):
                        if len(v) == 1:
                            v = int(v[0])
                    if key:
                        obj[key] = v
                    else:
                        r[name] = v

                r.update(sub_dict)
                return r
            return converter(r)

        return [c(row) for row in rs]

    def query_one(self, sql, converter=None, **kvargs):
        sql = self.db.sql_page(sql, 1, 1)
        res = self.query(sql, converter, **kvargs)
        if len(res) > 0: return res[0]

    def execute(self, sql, **kvargs):
        if isinstance(sql, str):
            if self.db.force_escape_sql:
                sql = self.db.escape_sql(sql)
            sql = text(sql)
        return self.connection.execute(sql, **kvargs)

    def _check_table(self, table):
        if table not in self.tables:
            raise Exception('Table(%s) Not Found' % table)
        return self.tables[table]

    def _primary_key(self, table):
        t = self._check_table(table)
        if len(t.primary_key) != 1:
            raise Exception('Table(%s) primary key not single' % table)
        for c in t.primary_key:
            return t, c

    def _table_and_column(self, s):
        bb = s.split('.')
        if len(bb) != 2:
            raise Exception('Invalid table and column string: %s' % s)
        t = self._check_table(bb[0])
        if bb[1] not in t.c:
            raise Exception('Column(%s) not in Table(%s)' % (bb[1], bb[0]))
        return t, bb[1]

    def _batch_query(self, t, col_name, value_set):
        value_set = list(value_set)
        if len(value_set) == 1:
            s = select([t]).where(t.c[col_name] == value_set[0])
        else:
            s = select([t]).where(t.c[col_name].in_(value_set))
        data = self._query(s)
        res = {}
        for row in data:
            k = row[col_name]
            if k not in res:
                res[k] = [row]
            else:
                res[k].append(row)
        return res

    def delete(self, table, key):
        t, c_key = self._primary_key(table)
        s = delete(t).where(t.c[c_key.name] == key)
        self.connection.execute(s)

    def add(self, table, json_data):
        self._check_table(table)

        t = self.tables[table]
        sql = t.insert()
        data = Dict({key: json_data[key] for key in json_data if key in t.c})
        res = self.connection.execute(sql, data)
        inserted_keys = res.inserted_primary_key
        i = 0
        for c in t.primary_key:
            if i >= len(inserted_keys):
                break
            data[c.name] = inserted_keys[i]
            i += 1
        return data

    def add_many(self, table, data):
        t = self._check_table(table)
        return self.execute_many(t.insert(), data)

    def update_many(self, table, data, keys=None):
        if len(data) == 0:
            return
        row = data[0]
        t = self._check_table(table)
        _t = self.db.escape
        primary_keys = []
        update_cols = []
        for c in t.c:
            if c.name not in row:
                continue
            col = f"{_t(c.name)}=:{c.name}"
            if keys:
                if c.name in keys:
                    primary_keys.append(col)
                    continue
                if c.primary_key:
                    continue    # 指定了主键，忽略数据库主键更新
            else:
                if c.primary_key:
                    primary_keys.append(col)
                    continue

            update_cols.append(col)

        updates = ', '.join(update_cols)
        where = ' and '.join(primary_keys)
        sql = f"UPDATE {_t(t.name)} SET {updates} WHERE {where}"

        return self.execute_many(sql, data)

    def save_many(self, table, data, overwrite=True):
        """
        快速批量更新，依赖数据库主键约束
        """
        if len(data) == 0:
            return
        row = data[0]
        t = self._check_table(table)
        _t = self.db.escape
        save_cols, save_params, update_cols = [], [], []
        for c in t.c:
            if c.name not in row:
                continue
            save_cols.append(c.name)
            save_params.append(f":{c.name}")
            col = f"{_t(c.name)}=VALUES({_t(c.name)})"
            update_cols.append(col)

        columns = ', '.join(save_cols)
        params = ', '.join(save_params)
        updates = ', '.join(update_cols)
        if overwrite:
            sql = f"INSERT INTO {_t(t.name)}({columns}) VALUES({params}) ON DUPLICATE KEY UPDATE {updates}"
        else:
            sql = f"INSERT IGNORE INTO {_t(t.name)}({columns}) VALUES({params})"

        return self.execute_many(sql, data)

    def execute_many(self, sql, data):
        if isinstance(sql, str):
            if self.db.force_escape_sql:
                sql = self.db.escape_sql(sql)
            sql = text(sql)
        if not isinstance(data, (tuple, list)):
            data = [data]

        # data must be array of dict!!!
        data = [dict(d) for d in data]

        res = self.connection.execute(sql, data)
        return res.rowcount

    def update(self, table, json_data):
        return self.merge(table, json_data)

    def merge(self, table, json_data):
        self._check_table(table)

        t = self.tables[table]
        values, where = {}, []
        for key in json_data:
            if key not in t.c:
                continue
            if key in t.primary_key:
                cond = t.c[key] == json_data[key]
                where.append(cond)
            else:
                values[key] = json_data[key]
        if len(where) == 0:
            raise Exception("Missing database primary key in merge action")

        sql = t.update().where(and_(*where)).values(**values)
        return self.connection.execute(sql).rowcount

    def save(self, table, json_data):
        self._check_table(table)

        update = False
        t = self.tables[table]
        for key in json_data:
            if key in t.primary_key:
                update = True
                sql = t.select().where(t.c[key] == json_data[key])
                res = self.query_one(sql)
                if not res:
                    update = False
                break
        if update:
            return self.merge(table, json_data)
        return self.add(table, json_data)
