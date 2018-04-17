# 开发扩展

HttpRunner 除了作为命令行工具使用外，还可以作为软件包集成到你自己的项目中。

简单来说，HttpRunner 提供了运行 YAML/JSON 格式测试用例的能力，并能返回详细的测试结果信息。

```python
from httprunner import HttpRunner

kwargs = {
    "failfast": False
}
runner = HttpRunner(**kwargs)
```

## 运行方式

HttpRunner 的 run 方法有两个参数：

- path_or_testsets：支持传入两类参数，YAML/JSON 格式测试用例文件路径，或者标准的测试用例结构体；
- mapping（可选）：变量映射，可用于对传入测试用例集中的变量进行替换。

### 传入测试用例文件路径

指定测试用例文件路径支持三种形式：

- YAML/JSON 文件路径，支持绝对路径和相对路径
- 包含 YAML/JSON 文件的文件夹，支持绝对路径和相对路径
- 文件路径和文件夹路径的混合情况（list/set）

```python
# 文件路径
runner.run("docs/data/demo-quickstart-2.yml")

# 文件夹路径
runner.run("docs/data/")

# 混合情况
runner.run(["docs/data/", "files/demo-quickstart-2.yml"])
```

### 传入标准的测试用例结构体

除了传入测试用例文件路径，还可以直接传入标准的测试用例结构体。

以 [demo-quickstart-2.yml](/data/demo-quickstart-2.yml) 为例，对应的数据结构体如下所示：

```json
{
  'name': 'testset description',
  'config': {
    'path': 'docs/data/demo-quickstart-2.yml',
    'name': 'testset description',
    'request': {
      'base_url': '',
      'headers': {'User-Agent': 'python-requests/2.18.4'}
    },
    'variables': [],
    'output': ['token']
  },
  'api': {},
  'testcases': [
    {
      'name': '/api/get-token',
      'request': {
        'url': 'http://127.0.0.1:5000/api/get-token',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json', 'app_version': '2.8.6', 'device_sn': 'FwgRiO7CNA50DSU', 'os_platform': 'ios', 'user_agent': 'iOS/10.3'},
        'json': {'sign': '958a05393efef0ac7c0fb80a7eac45e24fd40c27'}
      },
      'extract': [
        {'token': 'content.token'}
      ],
      'validate': [
        {'eq': ['status_code', 200]},
        {'eq': ['headers.Content-Type', 'application/json']},
        {'eq': ['content.success', True]}
      ]
    },
    {
      'name': '/api/users/1000',
      'request': {
        'url': 'http://127.0.0.1:5000/api/users/1000',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json', 'device_sn': 'FwgRiO7CNA50DSU','token': '$token'}, 'json': {'name': 'user1', 'password': '123456'}
      },
      'validate': [
        {'eq': ['status_code', 201]},
        {'eq': ['headers.Content-Type', 'application/json']},
        {'eq': ['content.success', True]},
        {'eq': ['content.msg', 'user created successfully.']}
      ]
    }
  ]
}
```

传入测试用例结构体时，支持传入单个结构体（dict），以及多个结构体（list of dict）。

```python
# 运行单个结构体
runner.run(testset)

# 运行多个结构体
runner.run([testset1, testset2])
```

## 返回详细测试结果数据

运行完成后，runner 的 summary 属性中包含详尽的运行结果数据。

```python
# get result summary
summary = runner.summary
```

其数据结构为：

```json
{
  "success": True,
  "stat": {
    "testsRun": 2,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "expectedFailures": 0,
    "unexpectedSuccesses": 0,
    "successes": 2
  },
  "platform": {
    "httprunner_version": "1.3.8.beta.3",
    "python_version": "CPython 3.6.4",
    "platform": "Darwin-17.4.0-x86_64-i386-64bit"
  },
  "time": {
    "start_at": datetime.datetime(2018, 4, 16, 22, 11, 55, 420941),
    "duration": 0.035871028900146484
  },
  "records": [
    {
      "name": "/api/get-token",
      "status": "success",
      "response_time_ms": 13.15,
      "attachment": "",
      "meta_data": {
        "method": "POST",
        "request_time": 1523887915.4214551,
        "response_time(ms)": 13.15,
        "elapsed(ms)": 4.081,
        "url": "http://127.0.0.1:5000/api/get-token",
        "request_headers": {"user-agent": "python-requests/2.18.4", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "keep-alive", "content-type": "application/json", "app_version": "2.8.6", "device_sn": "FwgRiO7CNA50DSU", "os_platform": "ios", "user_agent": "iOS/10.3", "Content-Length": "52"},
        "request_body": b'{"sign": "958a05393efef0ac7c0fb80a7eac45e24fd40c27"}',
        "status_code": 200,
        "response_headers": {"Content-Type": "application/json", "Content-Length": "46", "Server": "Werkzeug/0.14.1 Python/3.6.4", "Date": "Mon, 16 Apr 2018 14:11:55 GMT"},
        "response_body": {"success": True, "token": "GEilyOTo30WzUpFt"},
        "content_size": 46
      }
    },
    {
      "name": "/api/users/1000",
      "status": "success",
      "response_time_ms": 3.1,
      "attachment": "",
      "meta_data": {
        "method": "POST",
        "request_time": 1523887915.4355829,
        "response_time(ms)": 3.1,
        "elapsed(ms)": 1.903,
        "url": "http://127.0.0.1:5000/api/users/1000",
        "request_headers": {"user-agent": "python-requests/2.18.4", "Accept-Encoding": "gzip, deflate", "Accept": "*/*","Connection": "keep-alive", "content-type": "application/json", "device_sn": "FwgRiO7CNA50DSU", "token": "GEilyOTo30WzUpFt", "Content-Length": "39"},
        "request_body": b'{"name": "user1", "password": "123456"}',
        "status_code": 201,
        "response_headers": {"Content-Type": "application/json", "Content-Length": "54", "Server": "Werkzeug/0.14.1 Python/3.6.4", "Date": "Mon, 16 Apr 2018 14:11:55 GMT"},
        "response_body": {"success": True, "msg": "user created successfully."},
        "content_size": 54
      }
    }
  ],
  "output": [
    {"in": OrderedDict(), "out": {"token": "9PArqHp37FmHNoQw"}}
  ]
}
```

## 生成 HTML 测试报告

如需生成 HTML 测试报告，可调用 runner 的 gen_html_report 方法。

```python
# generate html report
runner.gen_html_report(
    html_report_name="demo",
    html_report_template="/path/to/custom_report_template"
)

# => reports/demo/demo-2018-04-16-22-22-17.html
```
