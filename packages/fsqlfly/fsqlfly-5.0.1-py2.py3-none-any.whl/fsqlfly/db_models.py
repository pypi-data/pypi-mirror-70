import json
import sqlalchemy as sa
from jinja2 import Template
from datetime import datetime
from configparser import ConfigParser
from typing import Tuple, TypeVar, Any, Optional, Type, Union
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from fsqlfly.common import (FlinkConnectorType, FlinkTableType, ConnectorType, DEFAULT_CONFIG, CanalMode, SchemaField,
                            BlinkSQLType, NameFilter, SchemaContent, VersionConfig, FlinkSaveFormat)

from fsqlfly.utils.strings import load_yaml
from fsqlfly.utils.template import generate_template_context
from fsqlfly.utils.db_execute import execute
from sqlalchemy_utils import ChoiceType, Choice
from logzero import logger

_Base = declarative_base()

CONNECTION_TYPE = ChoiceType([(k, k) for k in FlinkConnectorType.keys()], impl=String(16))
TABLE_TYPE = ChoiceType([(k, k) for k in FlinkTableType.keys()], impl=String(8))
CONNECTOR_CHOICE_TYPE = ChoiceType([(k, k) for k in ConnectorType.keys()], impl=String(8))
CONFIG_T = TypeVar('CONFIG_T', int, str, bool, float)


def _b(x: str):
    return backref(x, cascade="delete, delete-orphan")


class SaveDict(dict):
    @property
    def id(self):
        return self.get('id')


class Base(_Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=sa.func.now())
    updated_at = Column(DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())
    is_locked = Column(Boolean, default=False)

    def as_dict(self) -> SaveDict:
        def _convert(v: Any) -> Any:
            if isinstance(v, Choice):
                return v.code
            return v

        return SaveDict({column.name: _convert(getattr(self, column.name)) for column in self.__table__.columns})

    @classmethod
    def get_default_config_parser(cls) -> ConfigParser:
        default_config_parser = ConfigParser()

        default_config_parser.read_string(DEFAULT_CONFIG)
        return default_config_parser

    def get_config_parser(self) -> ConfigParser:
        return self.get_default_config_parser()

    def get_config(self, name: str, section: str, typ: Optional[Type[CONFIG_T]] = None) -> CONFIG_T:
        cache_name = '__config_parser__'
        if not hasattr(self, cache_name):
            setattr(self, cache_name, self.get_config_parser())
        parser = getattr(self, cache_name)
        secret = parser[section]
        if typ:
            if typ is int:
                return secret.getint(name)
            elif typ is float:
                return secret.getint(name)
            elif typ is bool:
                return secret.getboolean(name)
        return secret.get(name)


class Connection(Base):
    __tablename__ = 'connection'
    name = Column(String(32), nullable=False, unique=True)
    update_interval = Column(Integer, default=0)
    url = Column(Text, nullable=False)
    type = Column(CONNECTION_TYPE, nullable=False)
    info = Column(Text)
    connector = Column(Text, nullable=False)
    config = Column(Text)
    include = Column(String(2048))
    exclude = Column(String(2048))
    is_active = Column(Boolean, default=False)

    def get_config(self, name: str, section: Optional[str] = None,
                   typ: Optional[Union[Type[int], Type[float], Type[float], Type[str]]] = None) -> Any:
        return super(Connection, self).get_config(name, section=section if section else self.type, typ=typ)

    def get_config_parser(self) -> ConfigParser:
        parser = super(Connection, self).get_config_parser()
        if self.config and self.config.strip():
            parser.read_string(self.config)

        return parser

    def get_connection_connector(self) -> dict:
        config = self.get_config_parser()
        context = generate_template_context(execution_date=datetime.now(), connection=self, **config[self.type])
        output = Template(self.connector).render(**context)
        return load_yaml(output)


class SchemaEvent(Base):
    __tablename__ = 'schema_event'
    __table_args__ = (
        UniqueConstraint('connection_id', 'name', 'database', 'version'),
    )
    name = Column(String(128), nullable=False)
    info = Column(Text)
    database = Column(String(64), nullable=True)
    connection_id = Column(Integer, ForeignKey('connection.id'), nullable=False)
    connection = relationship('Connection', backref=_b('schemas'))
    father_id = Column(Integer, ForeignKey('schema_event.id'), nullable=True)
    father = relationship('SchemaEvent', backref=_b('children'), remote_side='SchemaEvent.id')
    version = Column(Integer, nullable=False, default=0)
    comment = Column(Text)
    primary_key = Column(String(64))
    fields = Column(Text)
    partitionable = Column(Boolean, default=False)

    def to_schema_content(self) -> SchemaContent:
        origin_dict = self.as_dict()
        use = ['name', 'database', 'comment', 'partitionable']
        origin = {k: v for k, v in origin_dict.items() if k in use}
        origin['fields'] = [SchemaField(**x) for x in load_yaml(self.fields)] if self.fields else []
        origin['type'] = self.connection.type.code
        return SchemaContent(**origin)


class Connector(Base):
    __tablename__ = 'connector'
    name = Column(String(128), nullable=False, unique=True)
    info = Column(Text)
    type = Column(CONNECTOR_CHOICE_TYPE, nullable=False)
    source_id = Column(Integer, ForeignKey('connection.id', ondelete='NO ACTION'), nullable=True)
    target_id = Column(Integer, ForeignKey('connection.id', ondelete='NO ACTION'), nullable=True)
    source = relationship(Connection, foreign_keys=source_id, passive_deletes=False)
    target = relationship(Connection, foreign_keys=target_id, passive_deletes=False)
    config = Column(Text)
    generate_sql = Column(Text)
    cache = Column(Text)

    def get_config_parser(self) -> ConfigParser:
        parser = self.get_default_config_parser()
        if self.config and self.config.strip():
            parser.read_string(self.config)

        return parser

    @property
    def connector_mode(self) -> CanalMode:
        config_mode = self.get_config('mode', typ=str)

        return CanalMode(config_mode)

    def get_config(self, name: str, section: Optional[str] = None, typ: Optional[Type[CONFIG_T]] = None) -> CONFIG_T:
        return super(Connector, self).get_config(name, section=section if section else self.type.code, typ=typ)

    @property
    def process_time_field(self) -> Optional[SchemaField]:
        if self.get_config('process_time_enable', typ=bool):
            return SchemaField(name=self.get_config('process_time_name', typ=str),
                               type=BlinkSQLType.TIMESTAMP, proctime=True)

    @property
    def rowtime_enable(self) -> bool:
        return self.get_config('rowtime_enable', typ=bool)

    @property
    def rowtime_field(self) -> Optional[SchemaField]:
        if self.get_config('rowtime_enable', typ=bool):
            row_field = {
                "timestamps": {"type": "from-field", "from": self.get_config('rowtime_from', typ=str)},
                "watermarks": {"type": "periodic-bounded", "delay": self.get_config("rowtime_watermarks", typ=int)}
            }
            return SchemaField(name=self.get_config('rowtime_name', typ=str),
                               type=BlinkSQLType.TIMESTAMP, rowtime=row_field)

    @property
    def binlog_type_name_field(self) -> SchemaField:
        return SchemaField(name=self.get_config('binlog_type_name', typ=str),
                           type=BlinkSQLType.INTEGER)

    @property
    def db_execute_time_field(self) -> Optional[SchemaField]:
        if not self.get_config('rowtime_enable', typ=bool):
            return SchemaField(name=self.get_config('rowtime_from', typ=str),
                               type=BlinkSQLType.TIMESTAMP)

    @property
    def binlog_type_name(self) -> str:
        return self.get_config('binlog_type_name', typ=str)

    @property
    def before_column_suffix(self) -> str:
        return self.get_config('before_column_suffix', typ=str)

    @property
    def after_column_suffix(self) -> str:
        return self.get_config('after_column_suffix', typ=str)

    @property
    def update_suffix(self) -> str:
        return self.get_config('update_suffix', typ=str)

    def check_system_type(self):
        assert self.type == 'system', 'only system has need tables '

    @property
    def table_filter(self) -> NameFilter:
        if self.type.code == ConnectorType.canal:
            return NameFilter(include=self.get_config('table_filter'))
        else:
            return self.need_tables

    @property
    def need_tables(self) -> NameFilter:
        self.check_system_type()
        return NameFilter(self.get_config('source_include'), self.get_config('source_exclude'))

    def get_transform_name_format(self, resource_name: 'ResourceName', **kwargs) -> str:
        self.check_system_type()
        source_type, target_type = self.source.type.code, self.target.type.code
        return Template(self.get_config('transform_name_format')).render(
            generate_template_context(source_type=source_type, target_type=target_type,
                                      resource_name=resource_name, connector=self, **kwargs))

    def get_transform_target_full_name(self, **kwargs) -> Tuple[str, str]:
        database = Template(self.get_config('target_database_format')).render(**kwargs)
        table = Template(self.get_config('target_table_format')).render(**kwargs)
        return database, table

    @property
    def use_partition(self) -> bool:
        self.check_system_type()
        return self.get_config('use_partition', typ=bool)

    @property
    def system_overwrite(self) -> bool:
        self.check_system_type()
        return self.get_config('overwrite', typ=bool)

    @property
    def system_execution_parallelism(self) -> int:
        self.check_system_type()
        return self.get_config('execution_parallelism', typ=int)

    @property
    def system_execution_restart_strategy(self) -> dict:
        self.check_system_type()
        return json.loads(self.get_config('execution_restart_strategy', typ=str))

    @property
    def partition_key_value(self) -> Tuple[str, str]:
        self.check_system_type()
        return self.get_config('partition_name'), self.get_config('partition_value')


class ResourceName(Base):
    __tablename__ = 'resource_name'
    __table_args__ = (
        UniqueConstraint('connection_id', 'name', 'database'),
    )
    name = Column(String(128), nullable=False)
    info = Column(Text)
    database = Column(String(64), nullable=True)
    connection_id = Column(Integer, ForeignKey('connection.id'), nullable=False)
    connection = relationship(Connection, backref=_b('resource_names'))
    schema_version_id = Column(Integer, ForeignKey('schema_event.id'), nullable=True)
    schema_version = relationship(SchemaEvent, backref=_b('resource_names'), foreign_keys=schema_version_id)
    latest_schema_id = Column(Integer, ForeignKey('schema_event.id'), nullable=True)
    config = Column(Text)
    is_latest = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    full_name = Column(String(512), nullable=False, unique=True)

    def get_include(self):
        return self.database + '.' + self.name if self.database else self.name

    def get_config_parser(self) -> ConfigParser:
        parser = self.connection.get_config_parser()
        if self.config and self.config.strip():
            parser.read_string(self.config)

        return parser

    def get_config(self, name: str, section: Optional[str] = None,
                   typ: Optional[Union[Type[CONFIG_T]]] = None) -> CONFIG_T:
        return super(ResourceName, self).get_config(name, section=section if section else self.connection.type, typ=typ)

    @property
    def db_name(self):
        return self.database + '.' + self.name if self.database else self.name

    @property
    def save_format(self) -> str:
        return self.get_config('format')


class ResourceTemplate(Base):
    __tablename__ = 'resource_template'
    __table_args__ = (
        UniqueConstraint('resource_name_id', 'name'),
    )
    name = Column(String(128), nullable=False)
    type = Column(TABLE_TYPE, nullable=False)
    info = Column(Text)
    is_system = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)
    full_name = Column(String(512), nullable=False, unique=True)
    connection_id = Column(Integer, ForeignKey('connection.id'), nullable=False)
    connection = relationship('Connection', backref=_b('templates'))
    resource_name_id = Column(Integer, ForeignKey('resource_name.id'), nullable=False)
    resource_name = relationship(ResourceName, backref=_b('templates'))
    schema_version = relationship(SchemaEvent, backref=_b('templates'))
    schema_version_id = Column(Integer, ForeignKey('schema_event.id'), nullable=True)
    config = Column(Text)


class ResourceVersion(Base):
    __tablename__ = 'resource_version'
    __table_args__ = (
        UniqueConstraint('template_id', 'version'),
    )
    name = Column(String(128), nullable=False, default='latest')
    info = Column(Text)
    full_name = Column(String(512), nullable=False, unique=True)
    is_system = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)
    is_latest = Column(Boolean, default=False)
    version = Column(Integer, nullable=False, default=0)
    connection_id = Column(Integer, ForeignKey('connection.id'), nullable=False)
    connection = relationship(Connection, backref=_b('versions'))
    resource_name_id = Column(Integer, ForeignKey('resource_name.id'), nullable=False)
    resource_name = relationship(ResourceName, backref=_b('versions'))
    template_id = Column(Integer, ForeignKey('resource_template.id'), nullable=False)
    template = relationship(ResourceTemplate, backref=_b('versions'))
    schema_version = relationship(SchemaEvent, backref=_b('versions'))
    schema_version_id = Column(Integer, ForeignKey('schema_event.id'))
    config = Column(Text)
    cache = Column(Text)

    def get_connection_connector(self) -> dict:
        config = self.resource_name.get_config_parser()
        context = generate_template_context(execution_date=datetime.now(), connection=self.connection,
                                            schema=self.schema_version,
                                            tempalte=self.template, resource_name=self.resource_name,
                                            version=self, **config[self.connection.type])
        output = Template(self.connection.connector).render(**context)
        return load_yaml(output)

    @classmethod
    def latest_name(cls):
        return 'latest'

    @property
    def db_full_name(self):
        return self.full_name.replace('.', '__')

    def get_db_bound(self, key: str) -> Tuple[int, int]:
        resource_name = self.resource_name
        connection = self.connection

        def _get_int(name: str):
            return resource_name.get_config(name, typ=int)

        real_low, real_upper = _get_int('read_partition_lower_bound'), _get_int('read_partition_upper_bound')

        if resource_name.get_config('auto_partition_bound', typ=bool):
            real_low, real_upper = self.get_db_bound_from_db(connection, key, real_low, real_upper, resource_name)

        if real_low is None and real_upper is not None:
            return real_upper - 1, real_upper
        elif real_low is not None and real_upper is None:
            return real_low, real_low + 1
        elif real_low is None and real_upper is None:
            return 0, 1

        info = f'{self.full_name} must need db bound if you add partition key'
        assert real_low is not None and real_upper is not None, info
        assert real_low <= real_upper, 'generate low upper bind is not equal'
        return real_low, real_upper

    @classmethod
    def get_db_bound_from_db(cls, connection: Connection, key: str, real_low: Optional[int], real_upper: Optional[int],
                             resource_name: ResourceName) -> Tuple[Optional[int], Optional[int]]:
        e = '`'
        sql = f'select min({e}{key}{e}), max({e}{key}{e}) from {e}{resource_name.database}{e}.{e}{resource_name.name}{e}'
        data = execute(sql, connection.url)
        l, u = data[0]
        if real_low is None:
            real_low = l
        if real_upper is None:
            real_upper = u
        return real_low, real_upper

    def generate_version_cache(self) -> dict:
        template = self.template
        version = self
        resource_name = self.resource_name
        connection = self.connection
        connection_type = connection.type.code
        template_type = template.type.code
        schema = self.schema_version if self.schema_version else SchemaContent(name=resource_name.name,
                                                                               type=connection.type.code,
                                                                               database=resource_name.database)
        base = load_yaml(template.config) if template.config else dict()
        version_config = load_yaml(version.config) if version.config else dict()
        base.update(**version_config)
        config = VersionConfig(**base)
        v_info = "Version {}:{}".format(version.id, version.name)
        if template.type == 'view':
            res = self.generate_view_cache(config, v_info)
        elif template.type == 'temporal-table':
            res = self.generate_temporal_table_cache(config, v_info)
        elif template.type in ('sink', 'source', 'both'):
            res = self.generate_table_cache(config, connection, connection_type, resource_name, schema, template,
                                            template_type, version)

        else:
            raise NotImplementedError("Not Support {}".format(template.type))

        return res

    def generate_version_schema(self) -> list:
        return self.generate_version_cache().get('schema', [])

    @classmethod
    def is_filter_field(cls, field: SchemaField, connection_type: str, template_type: str,
                        resource_name: ResourceName) -> bool:
        if field.autoincrement and connection_type == FlinkConnectorType.jdbc and template_type == 'sink' and not resource_name.get_config(
                'insert_primary_key', typ=bool):
            return True
        return False

    def generate_table_cache(self, config: VersionConfig, connection: Connection, connection_type: str,
                             resource_name: ResourceName, schema: SchemaEvent, template: ResourceTemplate,
                             template_type: str,
                             version: 'ResourceVersion') -> dict:
        res = dict()
        if config.update_mode:
            res['update-mode'] = config.update_mode
        if config.format:
            res['format'] = config.format
        elif connection_type not in FlinkConnectorType.schema_less():
            if resource_name.save_format == FlinkSaveFormat.json:
                res['format'] = {"type": 'json'}
            elif resource_name.save_format == FlinkSaveFormat.csv:
                res['format'] = {"type": 'csv'}
            else:
                msg = "Not Support Save format: {} in {}".format(resource_name.save_format, resource_name.full_name)
                raise NotImplementedError(msg)

        connector = self.generate_table_connector(connection, connection_type, resource_name, schema, template, version)
        res['connector'] = connector if connector else None
        fields = [SchemaField(**x) for x in load_yaml(schema.fields)] if schema.fields else []
        need_fields = [x for x in fields if x.name in NameFilter(config.include, config.exclude)]
        field_names = [x.name for x in need_fields]
        schemas = []
        if config.schema:
            for x in config.schema:
                assert x['name'] not in field_names, "{} contain in origin field"
            schemas.extend(config.schema)
        for x in need_fields:
            if self.is_filter_field(x, connection_type, template_type, resource_name):
                continue
            schemas.append(self.field2schema(x))
        res['schema'] = schemas
        return res

    def generate_table_connector(self, connection: Connection, connection_type: str, resource_name: ResourceName,
                                 schema: SchemaEvent, template: ResourceTemplate, version: 'ResourceVersion') -> dict:
        connector = version.get_connection_connector()
        jdbc, kafka = FlinkConnectorType.jdbc, FlinkConnectorType.kafka
        if connector and template.type in ('source', 'both') and schema.primary_key and connection_type == jdbc:
            if resource_name.get_config('add_read_partition_key', typ=bool) and 'read' not in connector:
                key = resource_name.get_config('read_partition_key')
                if key is None and schema.primary_key:
                    key = schema.primary_key
                if key:
                    low, upper = self.get_db_bound(key)
                    connector['read'] = {
                        "partition": {
                            "column": key,
                            "num": resource_name.get_config('read_partition_num', typ=int),
                            "lower-bound": low,
                            "upper-bound": upper,
                        },
                        "fetch-size": resource_name.get_config('read_partition_fetch_size', typ=int)
                    }
        if connector and connection_type == kafka:
            if resource_name.get_config('topic'):
                connector['topic'] = resource_name.get_config('topic')
        if connector:
            connector['type'] = connection.type.code
        return connector

    @classmethod
    def generate_temporal_table_cache(cls, config: VersionConfig, v_info: str) -> dict:
        assert config.history_table is not None, '{} View Must Need a history_table'.format(v_info)
        assert config.primary_key is not None, '{} View Must Need a primary_key'.format(v_info)
        assert config.time_attribute is not None, '{} View Must Need a time_attribute'.format(v_info)
        res = {
            "history-table": config.history_table,
            "primary-key": config.primary_key,
            "time-attribute": config.time_attribute
        }
        return res

    @classmethod
    def generate_view_cache(cls, config: VersionConfig, v_info: str) -> dict:
        assert config.query is not None, '{} View Must Need a Query'.format(v_info)
        res = dict(query=config.query)
        return res

    @classmethod
    def field2schema(cls, field: SchemaField) -> dict:
        base = {
            "name": field.name,
            "data-type": field.type
        }
        if field.proctime:
            base['proctime'] = field.proctime
        if field.rowtime:
            base['rowtime'] = field.rowtime
        return base


class Namespace(Base):
    __tablename__ = 'namespace'
    name = Column(String(256), unique=True)
    info = Column(Text)
    avatar = Column(Text)
    is_daemon = Column(Boolean, default=False)


class FileResource(Base):
    __tablename__ = 'file_resource'
    name = Column(String(512), unique=True, nullable=False)
    info = Column(Text)
    real_path = Column(Text)
    is_system = Column(Boolean, default=False)


class Functions(Base):
    __tablename__ = 'functions'
    name = Column(String(256), unique=True, nullable=False)
    class_name = Column(String(512), nullable=False)
    constructor_config = Column(Text)
    resource_id = Column(Integer, ForeignKey('file_resource.id'), nullable=False)
    resource = relationship(FileResource, backref=_b('functions'))
    is_active = Column(Boolean, default=True)

    class Meta:
        table_name = "functions"


class Transform(Base):
    __tablename__ = 'transform'
    name = Column(String(256), unique=True, nullable=False)
    info = Column(Text)
    sql = Column(Text, nullable=True)
    require = Column(Text)
    yaml = Column(Text)
    namespace_id = Column(Integer, ForeignKey('namespace.id'), nullable=True)
    namespace = relationship(Namespace, backref=_b('transforms'))
    connector_id = Column(Integer, ForeignKey('connector.id'), nullable=True)
    connector = relationship(Connector, backref=_b('transforms'))
    is_daemon = Column(Boolean, default=False)

    class Meta:
        table_name = "transform"


class TransformSavepoint(Base):
    __tablename__ = 'transform_savepoint'
    name = Column(String(1024), nullable=False)
    path = Column(Text, nullable=False)
    info = Column(Text)
    snapshot = Column(Text)
    transform_id = Column(Integer, ForeignKey('transform.id'))
    transform = relationship('Transform', backref=_b('savepoint'))


def delete_all_tables(engine, force: bool = False):
    if not force:
        word = input('Are you delete all tables (Y/n)')
        if word.strip().upper() != 'Y':
            return
    logger.info("begin delete all tables")
    Base.metadata.drop_all(engine)


def create_all_tables(engine):
    Base.metadata.create_all(engine)


__all__ = ['create_all_tables', 'delete_all_tables', 'Base', 'Connection',
           'SchemaEvent', 'Connector', 'ResourceName', 'ResourceVersion', 'ResourceTemplate',
           'Namespace', 'FileResource', 'Transform', 'Functions', 'TransformSavepoint', 'SaveDict']
