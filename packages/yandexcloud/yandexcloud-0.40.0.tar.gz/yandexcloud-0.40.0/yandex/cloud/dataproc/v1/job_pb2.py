# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/dataproc/v1/job.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/dataproc/v1/job.proto',
  package='yandex.cloud.dataproc.v1',
  syntax='proto3',
  serialized_options=b'\n\034yandex.cloud.api.dataproc.v1B\003PHJZEgithub.com/yandex-cloud/go-genproto/yandex/cloud/dataproc/v1;dataproc',
  serialized_pb=b'\n\"yandex/cloud/dataproc/v1/job.proto\x12\x18yandex.cloud.dataproc.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xeb\x04\n\x03Job\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\ncluster_id\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nstarted_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0b\x66inished_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04name\x18\x06 \x01(\t\x12\x12\n\ncreated_by\x18\x0c \x01(\t\x12\x34\n\x06status\x18\x07 \x01(\x0e\x32$.yandex.cloud.dataproc.v1.Job.Status\x12?\n\rmapreduce_job\x18\x08 \x01(\x0b\x32&.yandex.cloud.dataproc.v1.MapreduceJobH\x00\x12\x37\n\tspark_job\x18\t \x01(\x0b\x32\".yandex.cloud.dataproc.v1.SparkJobH\x00\x12;\n\x0bpyspark_job\x18\n \x01(\x0b\x32$.yandex.cloud.dataproc.v1.PysparkJobH\x00\x12\x35\n\x08hive_job\x18\x0b \x01(\x0b\x32!.yandex.cloud.dataproc.v1.HiveJobH\x00\"a\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x10\n\x0cPROVISIONING\x10\x01\x12\x0b\n\x07PENDING\x10\x02\x12\x0b\n\x07RUNNING\x10\x03\x12\t\n\x05\x45RROR\x10\x04\x12\x08\n\x04\x44ONE\x10\x05\x42\n\n\x08job_spec\"\x98\x02\n\x0cMapreduceJob\x12\x0c\n\x04\x61rgs\x18\x01 \x03(\t\x12\x15\n\rjar_file_uris\x18\x02 \x03(\t\x12\x11\n\tfile_uris\x18\x03 \x03(\t\x12\x14\n\x0c\x61rchive_uris\x18\x04 \x03(\t\x12J\n\nproperties\x18\x05 \x03(\x0b\x32\x36.yandex.cloud.dataproc.v1.MapreduceJob.PropertiesEntry\x12\x1b\n\x11main_jar_file_uri\x18\x06 \x01(\tH\x00\x12\x14\n\nmain_class\x18\x07 \x01(\tH\x00\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x08\n\x06\x64river\"\x82\x02\n\x08SparkJob\x12\x0c\n\x04\x61rgs\x18\x01 \x03(\t\x12\x15\n\rjar_file_uris\x18\x02 \x03(\t\x12\x11\n\tfile_uris\x18\x03 \x03(\t\x12\x14\n\x0c\x61rchive_uris\x18\x04 \x03(\t\x12\x46\n\nproperties\x18\x05 \x03(\x0b\x32\x32.yandex.cloud.dataproc.v1.SparkJob.PropertiesEntry\x12\x19\n\x11main_jar_file_uri\x18\x06 \x01(\t\x12\x12\n\nmain_class\x18\x07 \x01(\t\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x8f\x02\n\nPysparkJob\x12\x0c\n\x04\x61rgs\x18\x01 \x03(\t\x12\x15\n\rjar_file_uris\x18\x02 \x03(\t\x12\x11\n\tfile_uris\x18\x03 \x03(\t\x12\x14\n\x0c\x61rchive_uris\x18\x04 \x03(\t\x12H\n\nproperties\x18\x05 \x03(\x0b\x32\x34.yandex.cloud.dataproc.v1.PysparkJob.PropertiesEntry\x12\x1c\n\x14main_python_file_uri\x18\x06 \x01(\t\x12\x18\n\x10python_file_uris\x18\x07 \x03(\t\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x1c\n\tQueryList\x12\x0f\n\x07queries\x18\x01 \x03(\t\"\xa4\x03\n\x07HiveJob\x12\x45\n\nproperties\x18\x01 \x03(\x0b\x32\x31.yandex.cloud.dataproc.v1.HiveJob.PropertiesEntry\x12\x1b\n\x13\x63ontinue_on_failure\x18\x02 \x01(\x08\x12P\n\x10script_variables\x18\x03 \x03(\x0b\x32\x36.yandex.cloud.dataproc.v1.HiveJob.ScriptVariablesEntry\x12\x15\n\rjar_file_uris\x18\x04 \x03(\t\x12\x18\n\x0equery_file_uri\x18\x05 \x01(\tH\x00\x12\x39\n\nquery_list\x18\x06 \x01(\x0b\x32#.yandex.cloud.dataproc.v1.QueryListH\x00\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x36\n\x14ScriptVariablesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x0c\n\nquery_typeBj\n\x1cyandex.cloud.api.dataproc.v1B\x03PHJZEgithub.com/yandex-cloud/go-genproto/yandex/cloud/dataproc/v1;dataprocb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])



_JOB_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='yandex.cloud.dataproc.v1.Job.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATUS_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROVISIONING', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PENDING', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RUNNING', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DONE', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=608,
  serialized_end=705,
)
_sym_db.RegisterEnumDescriptor(_JOB_STATUS)


_JOB = _descriptor.Descriptor(
  name='Job',
  full_name='yandex.cloud.dataproc.v1.Job',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='yandex.cloud.dataproc.v1.Job.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.dataproc.v1.Job.cluster_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='yandex.cloud.dataproc.v1.Job.created_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='started_at', full_name='yandex.cloud.dataproc.v1.Job.started_at', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='finished_at', full_name='yandex.cloud.dataproc.v1.Job.finished_at', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='yandex.cloud.dataproc.v1.Job.name', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_by', full_name='yandex.cloud.dataproc.v1.Job.created_by', index=6,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='yandex.cloud.dataproc.v1.Job.status', index=7,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mapreduce_job', full_name='yandex.cloud.dataproc.v1.Job.mapreduce_job', index=8,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='spark_job', full_name='yandex.cloud.dataproc.v1.Job.spark_job', index=9,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pyspark_job', full_name='yandex.cloud.dataproc.v1.Job.pyspark_job', index=10,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hive_job', full_name='yandex.cloud.dataproc.v1.Job.hive_job', index=11,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _JOB_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='job_spec', full_name='yandex.cloud.dataproc.v1.Job.job_spec',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=98,
  serialized_end=717,
)


_MAPREDUCEJOB_PROPERTIESENTRY = _descriptor.Descriptor(
  name='PropertiesEntry',
  full_name='yandex.cloud.dataproc.v1.MapreduceJob.PropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='yandex.cloud.dataproc.v1.MapreduceJob.PropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='yandex.cloud.dataproc.v1.MapreduceJob.PropertiesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=941,
  serialized_end=990,
)

_MAPREDUCEJOB = _descriptor.Descriptor(
  name='MapreduceJob',
  full_name='yandex.cloud.dataproc.v1.MapreduceJob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='args', full_name='yandex.cloud.dataproc.v1.MapreduceJob.args', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='jar_file_uris', full_name='yandex.cloud.dataproc.v1.MapreduceJob.jar_file_uris', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file_uris', full_name='yandex.cloud.dataproc.v1.MapreduceJob.file_uris', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='archive_uris', full_name='yandex.cloud.dataproc.v1.MapreduceJob.archive_uris', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='properties', full_name='yandex.cloud.dataproc.v1.MapreduceJob.properties', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='main_jar_file_uri', full_name='yandex.cloud.dataproc.v1.MapreduceJob.main_jar_file_uri', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='main_class', full_name='yandex.cloud.dataproc.v1.MapreduceJob.main_class', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_MAPREDUCEJOB_PROPERTIESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='driver', full_name='yandex.cloud.dataproc.v1.MapreduceJob.driver',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=720,
  serialized_end=1000,
)


_SPARKJOB_PROPERTIESENTRY = _descriptor.Descriptor(
  name='PropertiesEntry',
  full_name='yandex.cloud.dataproc.v1.SparkJob.PropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='yandex.cloud.dataproc.v1.SparkJob.PropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='yandex.cloud.dataproc.v1.SparkJob.PropertiesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=941,
  serialized_end=990,
)

_SPARKJOB = _descriptor.Descriptor(
  name='SparkJob',
  full_name='yandex.cloud.dataproc.v1.SparkJob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='args', full_name='yandex.cloud.dataproc.v1.SparkJob.args', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='jar_file_uris', full_name='yandex.cloud.dataproc.v1.SparkJob.jar_file_uris', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file_uris', full_name='yandex.cloud.dataproc.v1.SparkJob.file_uris', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='archive_uris', full_name='yandex.cloud.dataproc.v1.SparkJob.archive_uris', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='properties', full_name='yandex.cloud.dataproc.v1.SparkJob.properties', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='main_jar_file_uri', full_name='yandex.cloud.dataproc.v1.SparkJob.main_jar_file_uri', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='main_class', full_name='yandex.cloud.dataproc.v1.SparkJob.main_class', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SPARKJOB_PROPERTIESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1003,
  serialized_end=1261,
)


_PYSPARKJOB_PROPERTIESENTRY = _descriptor.Descriptor(
  name='PropertiesEntry',
  full_name='yandex.cloud.dataproc.v1.PysparkJob.PropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='yandex.cloud.dataproc.v1.PysparkJob.PropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='yandex.cloud.dataproc.v1.PysparkJob.PropertiesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=941,
  serialized_end=990,
)

_PYSPARKJOB = _descriptor.Descriptor(
  name='PysparkJob',
  full_name='yandex.cloud.dataproc.v1.PysparkJob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='args', full_name='yandex.cloud.dataproc.v1.PysparkJob.args', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='jar_file_uris', full_name='yandex.cloud.dataproc.v1.PysparkJob.jar_file_uris', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file_uris', full_name='yandex.cloud.dataproc.v1.PysparkJob.file_uris', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='archive_uris', full_name='yandex.cloud.dataproc.v1.PysparkJob.archive_uris', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='properties', full_name='yandex.cloud.dataproc.v1.PysparkJob.properties', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='main_python_file_uri', full_name='yandex.cloud.dataproc.v1.PysparkJob.main_python_file_uri', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='python_file_uris', full_name='yandex.cloud.dataproc.v1.PysparkJob.python_file_uris', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PYSPARKJOB_PROPERTIESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1264,
  serialized_end=1535,
)


_QUERYLIST = _descriptor.Descriptor(
  name='QueryList',
  full_name='yandex.cloud.dataproc.v1.QueryList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='queries', full_name='yandex.cloud.dataproc.v1.QueryList.queries', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1537,
  serialized_end=1565,
)


_HIVEJOB_PROPERTIESENTRY = _descriptor.Descriptor(
  name='PropertiesEntry',
  full_name='yandex.cloud.dataproc.v1.HiveJob.PropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='yandex.cloud.dataproc.v1.HiveJob.PropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='yandex.cloud.dataproc.v1.HiveJob.PropertiesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=941,
  serialized_end=990,
)

_HIVEJOB_SCRIPTVARIABLESENTRY = _descriptor.Descriptor(
  name='ScriptVariablesEntry',
  full_name='yandex.cloud.dataproc.v1.HiveJob.ScriptVariablesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='yandex.cloud.dataproc.v1.HiveJob.ScriptVariablesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='yandex.cloud.dataproc.v1.HiveJob.ScriptVariablesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1920,
  serialized_end=1974,
)

_HIVEJOB = _descriptor.Descriptor(
  name='HiveJob',
  full_name='yandex.cloud.dataproc.v1.HiveJob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='properties', full_name='yandex.cloud.dataproc.v1.HiveJob.properties', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='continue_on_failure', full_name='yandex.cloud.dataproc.v1.HiveJob.continue_on_failure', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='script_variables', full_name='yandex.cloud.dataproc.v1.HiveJob.script_variables', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='jar_file_uris', full_name='yandex.cloud.dataproc.v1.HiveJob.jar_file_uris', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='query_file_uri', full_name='yandex.cloud.dataproc.v1.HiveJob.query_file_uri', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='query_list', full_name='yandex.cloud.dataproc.v1.HiveJob.query_list', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_HIVEJOB_PROPERTIESENTRY, _HIVEJOB_SCRIPTVARIABLESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='query_type', full_name='yandex.cloud.dataproc.v1.HiveJob.query_type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1568,
  serialized_end=1988,
)

_JOB.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_JOB.fields_by_name['started_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_JOB.fields_by_name['finished_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_JOB.fields_by_name['status'].enum_type = _JOB_STATUS
_JOB.fields_by_name['mapreduce_job'].message_type = _MAPREDUCEJOB
_JOB.fields_by_name['spark_job'].message_type = _SPARKJOB
_JOB.fields_by_name['pyspark_job'].message_type = _PYSPARKJOB
_JOB.fields_by_name['hive_job'].message_type = _HIVEJOB
_JOB_STATUS.containing_type = _JOB
_JOB.oneofs_by_name['job_spec'].fields.append(
  _JOB.fields_by_name['mapreduce_job'])
_JOB.fields_by_name['mapreduce_job'].containing_oneof = _JOB.oneofs_by_name['job_spec']
_JOB.oneofs_by_name['job_spec'].fields.append(
  _JOB.fields_by_name['spark_job'])
_JOB.fields_by_name['spark_job'].containing_oneof = _JOB.oneofs_by_name['job_spec']
_JOB.oneofs_by_name['job_spec'].fields.append(
  _JOB.fields_by_name['pyspark_job'])
_JOB.fields_by_name['pyspark_job'].containing_oneof = _JOB.oneofs_by_name['job_spec']
_JOB.oneofs_by_name['job_spec'].fields.append(
  _JOB.fields_by_name['hive_job'])
_JOB.fields_by_name['hive_job'].containing_oneof = _JOB.oneofs_by_name['job_spec']
_MAPREDUCEJOB_PROPERTIESENTRY.containing_type = _MAPREDUCEJOB
_MAPREDUCEJOB.fields_by_name['properties'].message_type = _MAPREDUCEJOB_PROPERTIESENTRY
_MAPREDUCEJOB.oneofs_by_name['driver'].fields.append(
  _MAPREDUCEJOB.fields_by_name['main_jar_file_uri'])
_MAPREDUCEJOB.fields_by_name['main_jar_file_uri'].containing_oneof = _MAPREDUCEJOB.oneofs_by_name['driver']
_MAPREDUCEJOB.oneofs_by_name['driver'].fields.append(
  _MAPREDUCEJOB.fields_by_name['main_class'])
_MAPREDUCEJOB.fields_by_name['main_class'].containing_oneof = _MAPREDUCEJOB.oneofs_by_name['driver']
_SPARKJOB_PROPERTIESENTRY.containing_type = _SPARKJOB
_SPARKJOB.fields_by_name['properties'].message_type = _SPARKJOB_PROPERTIESENTRY
_PYSPARKJOB_PROPERTIESENTRY.containing_type = _PYSPARKJOB
_PYSPARKJOB.fields_by_name['properties'].message_type = _PYSPARKJOB_PROPERTIESENTRY
_HIVEJOB_PROPERTIESENTRY.containing_type = _HIVEJOB
_HIVEJOB_SCRIPTVARIABLESENTRY.containing_type = _HIVEJOB
_HIVEJOB.fields_by_name['properties'].message_type = _HIVEJOB_PROPERTIESENTRY
_HIVEJOB.fields_by_name['script_variables'].message_type = _HIVEJOB_SCRIPTVARIABLESENTRY
_HIVEJOB.fields_by_name['query_list'].message_type = _QUERYLIST
_HIVEJOB.oneofs_by_name['query_type'].fields.append(
  _HIVEJOB.fields_by_name['query_file_uri'])
_HIVEJOB.fields_by_name['query_file_uri'].containing_oneof = _HIVEJOB.oneofs_by_name['query_type']
_HIVEJOB.oneofs_by_name['query_type'].fields.append(
  _HIVEJOB.fields_by_name['query_list'])
_HIVEJOB.fields_by_name['query_list'].containing_oneof = _HIVEJOB.oneofs_by_name['query_type']
DESCRIPTOR.message_types_by_name['Job'] = _JOB
DESCRIPTOR.message_types_by_name['MapreduceJob'] = _MAPREDUCEJOB
DESCRIPTOR.message_types_by_name['SparkJob'] = _SPARKJOB
DESCRIPTOR.message_types_by_name['PysparkJob'] = _PYSPARKJOB
DESCRIPTOR.message_types_by_name['QueryList'] = _QUERYLIST
DESCRIPTOR.message_types_by_name['HiveJob'] = _HIVEJOB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Job = _reflection.GeneratedProtocolMessageType('Job', (_message.Message,), {
  'DESCRIPTOR' : _JOB,
  '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.Job)
  })
_sym_db.RegisterMessage(Job)

MapreduceJob = _reflection.GeneratedProtocolMessageType('MapreduceJob', (_message.Message,), {

  'PropertiesEntry' : _reflection.GeneratedProtocolMessageType('PropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _MAPREDUCEJOB_PROPERTIESENTRY,
    '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
    # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.MapreduceJob.PropertiesEntry)
    })
  ,
  'DESCRIPTOR' : _MAPREDUCEJOB,
  '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.MapreduceJob)
  })
_sym_db.RegisterMessage(MapreduceJob)
_sym_db.RegisterMessage(MapreduceJob.PropertiesEntry)

SparkJob = _reflection.GeneratedProtocolMessageType('SparkJob', (_message.Message,), {

  'PropertiesEntry' : _reflection.GeneratedProtocolMessageType('PropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _SPARKJOB_PROPERTIESENTRY,
    '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
    # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.SparkJob.PropertiesEntry)
    })
  ,
  'DESCRIPTOR' : _SPARKJOB,
  '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.SparkJob)
  })
_sym_db.RegisterMessage(SparkJob)
_sym_db.RegisterMessage(SparkJob.PropertiesEntry)

PysparkJob = _reflection.GeneratedProtocolMessageType('PysparkJob', (_message.Message,), {

  'PropertiesEntry' : _reflection.GeneratedProtocolMessageType('PropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _PYSPARKJOB_PROPERTIESENTRY,
    '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
    # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.PysparkJob.PropertiesEntry)
    })
  ,
  'DESCRIPTOR' : _PYSPARKJOB,
  '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.PysparkJob)
  })
_sym_db.RegisterMessage(PysparkJob)
_sym_db.RegisterMessage(PysparkJob.PropertiesEntry)

QueryList = _reflection.GeneratedProtocolMessageType('QueryList', (_message.Message,), {
  'DESCRIPTOR' : _QUERYLIST,
  '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.QueryList)
  })
_sym_db.RegisterMessage(QueryList)

HiveJob = _reflection.GeneratedProtocolMessageType('HiveJob', (_message.Message,), {

  'PropertiesEntry' : _reflection.GeneratedProtocolMessageType('PropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _HIVEJOB_PROPERTIESENTRY,
    '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
    # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.HiveJob.PropertiesEntry)
    })
  ,

  'ScriptVariablesEntry' : _reflection.GeneratedProtocolMessageType('ScriptVariablesEntry', (_message.Message,), {
    'DESCRIPTOR' : _HIVEJOB_SCRIPTVARIABLESENTRY,
    '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
    # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.HiveJob.ScriptVariablesEntry)
    })
  ,
  'DESCRIPTOR' : _HIVEJOB,
  '__module__' : 'yandex.cloud.dataproc.v1.job_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.HiveJob)
  })
_sym_db.RegisterMessage(HiveJob)
_sym_db.RegisterMessage(HiveJob.PropertiesEntry)
_sym_db.RegisterMessage(HiveJob.ScriptVariablesEntry)


DESCRIPTOR._options = None
_MAPREDUCEJOB_PROPERTIESENTRY._options = None
_SPARKJOB_PROPERTIESENTRY._options = None
_PYSPARKJOB_PROPERTIESENTRY._options = None
_HIVEJOB_PROPERTIESENTRY._options = None
_HIVEJOB_SCRIPTVARIABLESENTRY._options = None
# @@protoc_insertion_point(module_scope)
