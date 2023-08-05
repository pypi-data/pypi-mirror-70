# thrift_json in python3

convert from json/dict to thrift
```
from thrift_json import json2thrift, dict2thrift
thrift_obj = json2thrift(json_str, thrift_class)
thrift_obj = dict2thrift(dict_obj, thrift_class)
```

convert from thrift to json/dict
```
from thrift_json import thrift2json, thrift2dict
json_str = thrfit2json(thrift_obj)
dict_obj = thrift2dict(thrift_obj)
```

encode/decode use json directly
```
from thrift_json import ThriftJSONEncoder
json_str = json.dumps(thrift_obj, cls=ThriftJSONEncoder)
from thrift_json import ThriftJSONDecoder
thrift_obj = json.loads(json_str, cls=ThriftJSONDecoder, thrift_class=thrift_class) 
```
