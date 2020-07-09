#coding:utf-8

from jpype import *
import jpype
import os
from io import StringIO

jvmPath = u'D:\\Java\\bin\\server\\jvm.dll'                   #jvm.dll启动成功
# jpype.startJVM(jvmPath)
# jpype.java.lang.System.out.println("hello world!")
jarpath = "D:\\AutoWeb\\Auto_system\\API\\Adapter.ASN-1.1.0-SNAPSHOT.jar"
jpype.startJVM(jvmPath, "-Djava.class.path=%s"%jarpath)

OTAEncoder = JClass("com.saicmotor.telematics.tsgp.otaadapter.asn.codec.OTAEncoder")
OTADecoder = JClass("com.saicmotor.telematics.tsgp.otaadapter.asn.codec.OTADecoder")
java_io = JClass("java.io.ByteArrayOutputStream")
java_encode = java_io()

encoder = OTAEncoder(java_encode)
encoder.encode('{}')
return_data = java_encode.toString()
print(return_data)

java_out = JClass("java.io.ByteArrayInputStream")
java_decode = java_out([])
encoder = OTADecoder(java_decode)
return_data = encoder.decode({})
print(return_data)
print(java_decode.toString())

jpype.shutdownJVM()