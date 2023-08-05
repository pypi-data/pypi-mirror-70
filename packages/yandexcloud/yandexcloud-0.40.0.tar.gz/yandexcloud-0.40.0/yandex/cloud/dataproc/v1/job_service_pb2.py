# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/dataproc/v1/job_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from yandex.cloud.dataproc.v1 import job_pb2 as yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/dataproc/v1/job_service.proto',
  package='yandex.cloud.dataproc.v1',
  syntax='proto3',
  serialized_options=b'\n\034yandex.cloud.api.dataproc.v1B\004PHJSZEgithub.com/yandex-cloud/go-genproto/yandex/cloud/dataproc/v1;dataproc',
  serialized_pb=b'\n*yandex/cloud/dataproc/v1/job_service.proto\x12\x18yandex.cloud.dataproc.v1\x1a\x1cgoogle/api/annotations.proto\x1a\"yandex/cloud/dataproc/v1/job.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\x1a yandex/cloud/api/operation.proto\"O\n\rGetJobRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1c\n\x06job_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\x8d\x01\n\x0fListJobsRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06<=1000\x12\x1d\n\npage_token\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=100\x12\x1a\n\x06\x66ilter\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"X\n\x10ListJobsResponse\x12+\n\x04jobs\x18\x01 \x03(\x0b\x32\x1d.yandex.cloud.dataproc.v1.Job\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xdf\x02\n\x10\x43reateJobRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12/\n\x04name\x18\x02 \x01(\tB!\xf2\xc7\x31\x1d|[a-z][-a-z0-9]{1,61}[a-z0-9]\x12?\n\rmapreduce_job\x18\x03 \x01(\x0b\x32&.yandex.cloud.dataproc.v1.MapreduceJobH\x00\x12\x37\n\tspark_job\x18\x04 \x01(\x0b\x32\".yandex.cloud.dataproc.v1.SparkJobH\x00\x12;\n\x0bpyspark_job\x18\x05 \x01(\x0b\x32$.yandex.cloud.dataproc.v1.PysparkJobH\x00\x12\x35\n\x08hive_job\x18\x06 \x01(\x0b\x32!.yandex.cloud.dataproc.v1.HiveJobH\x00\x42\n\n\x08job_spec\"O\n\x11\x43reateJobMetadata\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x18\n\x06job_id\x18\x02 \x01(\tB\x08\x8a\xc8\x31\x04<=50\"\x90\x01\n\x11ListJobLogRequest\x12 \n\ncluster_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x18\n\x06job_id\x18\x02 \x01(\tB\x08\x8a\xc8\x31\x04<=50\x12 \n\tpage_size\x18\x03 \x01(\x03\x42\r\xfa\xc7\x31\t<=1048576\x12\x1d\n\npage_token\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=100\">\n\x12ListJobLogResponse\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t2\xf7\x04\n\nJobService\x12\x8e\x01\n\x04List\x12).yandex.cloud.dataproc.v1.ListJobsRequest\x1a*.yandex.cloud.dataproc.v1.ListJobsResponse\"/\x82\xd3\xe4\x93\x02)\x12\'/dataproc/v1/clusters/{cluster_id}/jobs\x12\xa7\x01\n\x06\x43reate\x12*.yandex.cloud.dataproc.v1.CreateJobRequest\x1a!.yandex.cloud.operation.Operation\"N\x82\xd3\xe4\x93\x02,\"\'/dataproc/v1/clusters/{cluster_id}/jobs:\x01*\xb2\xd2*\x18\n\x11\x43reateJobMetadata\x12\x03Job\x12\x87\x01\n\x03Get\x12\'.yandex.cloud.dataproc.v1.GetJobRequest\x1a\x1d.yandex.cloud.dataproc.v1.Job\"8\x82\xd3\xe4\x93\x02\x32\x12\x30/dataproc/v1/clusters/{cluster_id}/jobs/{job_id}\x12\xa3\x01\n\x07ListLog\x12+.yandex.cloud.dataproc.v1.ListJobLogRequest\x1a,.yandex.cloud.dataproc.v1.ListJobLogResponse\"=\x82\xd3\xe4\x93\x02\x37\x12\x35/dataproc/v1/clusters/{cluster_id}/jobs/{job_id}:logsBk\n\x1cyandex.cloud.api.dataproc.v1B\x04PHJSZEgithub.com/yandex-cloud/go-genproto/yandex/cloud/dataproc/v1;dataprocb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2.DESCRIPTOR,yandex_dot_cloud_dot_operation_dot_operation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_validation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_api_dot_operation__pb2.DESCRIPTOR,])




_GETJOBREQUEST = _descriptor.Descriptor(
  name='GetJobRequest',
  full_name='yandex.cloud.dataproc.v1.GetJobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.dataproc.v1.GetJobRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='job_id', full_name='yandex.cloud.dataproc.v1.GetJobRequest.job_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
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
  serialized_start=243,
  serialized_end=322,
)


_LISTJOBSREQUEST = _descriptor.Descriptor(
  name='ListJobsRequest',
  full_name='yandex.cloud.dataproc.v1.ListJobsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.dataproc.v1.ListJobsRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='yandex.cloud.dataproc.v1.ListJobsRequest.page_size', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372\3071\006<=1000', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='yandex.cloud.dataproc.v1.ListJobsRequest.page_token', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\005<=100', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filter', full_name='yandex.cloud.dataproc.v1.ListJobsRequest.filter', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\006<=1000', file=DESCRIPTOR),
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
  serialized_start=325,
  serialized_end=466,
)


_LISTJOBSRESPONSE = _descriptor.Descriptor(
  name='ListJobsResponse',
  full_name='yandex.cloud.dataproc.v1.ListJobsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='jobs', full_name='yandex.cloud.dataproc.v1.ListJobsResponse.jobs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='yandex.cloud.dataproc.v1.ListJobsResponse.next_page_token', index=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=468,
  serialized_end=556,
)


_CREATEJOBREQUEST = _descriptor.Descriptor(
  name='CreateJobRequest',
  full_name='yandex.cloud.dataproc.v1.CreateJobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.dataproc.v1.CreateJobRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='yandex.cloud.dataproc.v1.CreateJobRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\3071\035|[a-z][-a-z0-9]{1,61}[a-z0-9]', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mapreduce_job', full_name='yandex.cloud.dataproc.v1.CreateJobRequest.mapreduce_job', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='spark_job', full_name='yandex.cloud.dataproc.v1.CreateJobRequest.spark_job', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pyspark_job', full_name='yandex.cloud.dataproc.v1.CreateJobRequest.pyspark_job', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hive_job', full_name='yandex.cloud.dataproc.v1.CreateJobRequest.hive_job', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
    _descriptor.OneofDescriptor(
      name='job_spec', full_name='yandex.cloud.dataproc.v1.CreateJobRequest.job_spec',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=559,
  serialized_end=910,
)


_CREATEJOBMETADATA = _descriptor.Descriptor(
  name='CreateJobMetadata',
  full_name='yandex.cloud.dataproc.v1.CreateJobMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.dataproc.v1.CreateJobMetadata.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='job_id', full_name='yandex.cloud.dataproc.v1.CreateJobMetadata.job_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\004<=50', file=DESCRIPTOR),
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
  serialized_start=912,
  serialized_end=991,
)


_LISTJOBLOGREQUEST = _descriptor.Descriptor(
  name='ListJobLogRequest',
  full_name='yandex.cloud.dataproc.v1.ListJobLogRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.dataproc.v1.ListJobLogRequest.cluster_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='job_id', full_name='yandex.cloud.dataproc.v1.ListJobLogRequest.job_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='yandex.cloud.dataproc.v1.ListJobLogRequest.page_size', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372\3071\t<=1048576', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='yandex.cloud.dataproc.v1.ListJobLogRequest.page_token', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\212\3101\005<=100', file=DESCRIPTOR),
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
  serialized_start=994,
  serialized_end=1138,
)


_LISTJOBLOGRESPONSE = _descriptor.Descriptor(
  name='ListJobLogResponse',
  full_name='yandex.cloud.dataproc.v1.ListJobLogResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='content', full_name='yandex.cloud.dataproc.v1.ListJobLogResponse.content', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='yandex.cloud.dataproc.v1.ListJobLogResponse.next_page_token', index=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1140,
  serialized_end=1202,
)

_LISTJOBSRESPONSE.fields_by_name['jobs'].message_type = yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2._JOB
_CREATEJOBREQUEST.fields_by_name['mapreduce_job'].message_type = yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2._MAPREDUCEJOB
_CREATEJOBREQUEST.fields_by_name['spark_job'].message_type = yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2._SPARKJOB
_CREATEJOBREQUEST.fields_by_name['pyspark_job'].message_type = yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2._PYSPARKJOB
_CREATEJOBREQUEST.fields_by_name['hive_job'].message_type = yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2._HIVEJOB
_CREATEJOBREQUEST.oneofs_by_name['job_spec'].fields.append(
  _CREATEJOBREQUEST.fields_by_name['mapreduce_job'])
_CREATEJOBREQUEST.fields_by_name['mapreduce_job'].containing_oneof = _CREATEJOBREQUEST.oneofs_by_name['job_spec']
_CREATEJOBREQUEST.oneofs_by_name['job_spec'].fields.append(
  _CREATEJOBREQUEST.fields_by_name['spark_job'])
_CREATEJOBREQUEST.fields_by_name['spark_job'].containing_oneof = _CREATEJOBREQUEST.oneofs_by_name['job_spec']
_CREATEJOBREQUEST.oneofs_by_name['job_spec'].fields.append(
  _CREATEJOBREQUEST.fields_by_name['pyspark_job'])
_CREATEJOBREQUEST.fields_by_name['pyspark_job'].containing_oneof = _CREATEJOBREQUEST.oneofs_by_name['job_spec']
_CREATEJOBREQUEST.oneofs_by_name['job_spec'].fields.append(
  _CREATEJOBREQUEST.fields_by_name['hive_job'])
_CREATEJOBREQUEST.fields_by_name['hive_job'].containing_oneof = _CREATEJOBREQUEST.oneofs_by_name['job_spec']
DESCRIPTOR.message_types_by_name['GetJobRequest'] = _GETJOBREQUEST
DESCRIPTOR.message_types_by_name['ListJobsRequest'] = _LISTJOBSREQUEST
DESCRIPTOR.message_types_by_name['ListJobsResponse'] = _LISTJOBSRESPONSE
DESCRIPTOR.message_types_by_name['CreateJobRequest'] = _CREATEJOBREQUEST
DESCRIPTOR.message_types_by_name['CreateJobMetadata'] = _CREATEJOBMETADATA
DESCRIPTOR.message_types_by_name['ListJobLogRequest'] = _LISTJOBLOGREQUEST
DESCRIPTOR.message_types_by_name['ListJobLogResponse'] = _LISTJOBLOGRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetJobRequest = _reflection.GeneratedProtocolMessageType('GetJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETJOBREQUEST,
  '__module__' : 'yandex.cloud.dataproc.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.GetJobRequest)
  })
_sym_db.RegisterMessage(GetJobRequest)

ListJobsRequest = _reflection.GeneratedProtocolMessageType('ListJobsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTJOBSREQUEST,
  '__module__' : 'yandex.cloud.dataproc.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.ListJobsRequest)
  })
_sym_db.RegisterMessage(ListJobsRequest)

ListJobsResponse = _reflection.GeneratedProtocolMessageType('ListJobsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTJOBSRESPONSE,
  '__module__' : 'yandex.cloud.dataproc.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.ListJobsResponse)
  })
_sym_db.RegisterMessage(ListJobsResponse)

CreateJobRequest = _reflection.GeneratedProtocolMessageType('CreateJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEJOBREQUEST,
  '__module__' : 'yandex.cloud.dataproc.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.CreateJobRequest)
  })
_sym_db.RegisterMessage(CreateJobRequest)

CreateJobMetadata = _reflection.GeneratedProtocolMessageType('CreateJobMetadata', (_message.Message,), {
  'DESCRIPTOR' : _CREATEJOBMETADATA,
  '__module__' : 'yandex.cloud.dataproc.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.CreateJobMetadata)
  })
_sym_db.RegisterMessage(CreateJobMetadata)

ListJobLogRequest = _reflection.GeneratedProtocolMessageType('ListJobLogRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTJOBLOGREQUEST,
  '__module__' : 'yandex.cloud.dataproc.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.ListJobLogRequest)
  })
_sym_db.RegisterMessage(ListJobLogRequest)

ListJobLogResponse = _reflection.GeneratedProtocolMessageType('ListJobLogResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTJOBLOGRESPONSE,
  '__module__' : 'yandex.cloud.dataproc.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.dataproc.v1.ListJobLogResponse)
  })
_sym_db.RegisterMessage(ListJobLogResponse)


DESCRIPTOR._options = None
_GETJOBREQUEST.fields_by_name['cluster_id']._options = None
_GETJOBREQUEST.fields_by_name['job_id']._options = None
_LISTJOBSREQUEST.fields_by_name['cluster_id']._options = None
_LISTJOBSREQUEST.fields_by_name['page_size']._options = None
_LISTJOBSREQUEST.fields_by_name['page_token']._options = None
_LISTJOBSREQUEST.fields_by_name['filter']._options = None
_CREATEJOBREQUEST.fields_by_name['cluster_id']._options = None
_CREATEJOBREQUEST.fields_by_name['name']._options = None
_CREATEJOBMETADATA.fields_by_name['cluster_id']._options = None
_CREATEJOBMETADATA.fields_by_name['job_id']._options = None
_LISTJOBLOGREQUEST.fields_by_name['cluster_id']._options = None
_LISTJOBLOGREQUEST.fields_by_name['job_id']._options = None
_LISTJOBLOGREQUEST.fields_by_name['page_size']._options = None
_LISTJOBLOGREQUEST.fields_by_name['page_token']._options = None

_JOBSERVICE = _descriptor.ServiceDescriptor(
  name='JobService',
  full_name='yandex.cloud.dataproc.v1.JobService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1205,
  serialized_end=1836,
  methods=[
  _descriptor.MethodDescriptor(
    name='List',
    full_name='yandex.cloud.dataproc.v1.JobService.List',
    index=0,
    containing_service=None,
    input_type=_LISTJOBSREQUEST,
    output_type=_LISTJOBSRESPONSE,
    serialized_options=b'\202\323\344\223\002)\022\'/dataproc/v1/clusters/{cluster_id}/jobs',
  ),
  _descriptor.MethodDescriptor(
    name='Create',
    full_name='yandex.cloud.dataproc.v1.JobService.Create',
    index=1,
    containing_service=None,
    input_type=_CREATEJOBREQUEST,
    output_type=yandex_dot_cloud_dot_operation_dot_operation__pb2._OPERATION,
    serialized_options=b'\202\323\344\223\002,\"\'/dataproc/v1/clusters/{cluster_id}/jobs:\001*\262\322*\030\n\021CreateJobMetadata\022\003Job',
  ),
  _descriptor.MethodDescriptor(
    name='Get',
    full_name='yandex.cloud.dataproc.v1.JobService.Get',
    index=2,
    containing_service=None,
    input_type=_GETJOBREQUEST,
    output_type=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2._JOB,
    serialized_options=b'\202\323\344\223\0022\0220/dataproc/v1/clusters/{cluster_id}/jobs/{job_id}',
  ),
  _descriptor.MethodDescriptor(
    name='ListLog',
    full_name='yandex.cloud.dataproc.v1.JobService.ListLog',
    index=3,
    containing_service=None,
    input_type=_LISTJOBLOGREQUEST,
    output_type=_LISTJOBLOGRESPONSE,
    serialized_options=b'\202\323\344\223\0027\0225/dataproc/v1/clusters/{cluster_id}/jobs/{job_id}:logs',
  ),
])
_sym_db.RegisterServiceDescriptor(_JOBSERVICE)

DESCRIPTOR.services_by_name['JobService'] = _JOBSERVICE

# @@protoc_insertion_point(module_scope)
