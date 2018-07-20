# 开发扩展

HttpRunner 除了作为命令行工具使用外，还可以作为软件包集成到你自己的项目中。

简单来说，HttpRunner 提供了运行 YAML/JSON 格式测试用例的能力，并能返回详细的测试结果信息。

## 初始化参数

HttpRunner 继承自 `unittest.TextTestRunner`，因此 TextTestRunner 可用的初始化参数 HttpRunner 都可以用，参数详情可阅读[官方文档](https://docs.python.org/3.6/library/unittest.html#unittest.TextTestRunner)。除此之外，HttpRunner 还有一个额外的参数，`dot_env_path`。

通常情况下，初始化 HttpRunner 时常用的参数有如下几个：

- `resultclass`: HtmlTestResult/TextTestResult，默认值为 HtmlTestResult
- `failfast`: 设置为 True 时，测试在首次遇到错误或失败时会停止运行；默认值为 False
- `dot_env_path`: 指定加载环境变量文件（.env）的路径，默认值为当前工作目录下的 `.env` 文件
- `stream`

```python
from httprunner import HttpRunner

kwargs = {
    "failfast": False,
    "dot_env_path": "/path/to/.env"
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
  'config': {
    'name': 'testset description',
    'path': 'docs/data/demo-quickstart-2.yml',
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
  "success": true,
  "stat": {
    "testsRun": 2,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "expectedFailures": 0,
    "unexpectedSuccesses": 0,
    "successes": 2
  },
  "time": {
    "start_at": 1532065478.200753,
    "duration": 0.022025108337402344
  },
  "platform": {
    "httprunner_version": "1.5.2",
    "python_version": "CPython 3.6.5+",
    "platform": "Darwin-17.6.0-x86_64-i386-64bit"
  },
  "details": [
    {
      "success": true,
      "name": "testset description",
      "base_url": "",
      "stat": {
        "testsRun": 2,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "expectedFailures": 0,
        "unexpectedSuccesses": 0,
        "successes": 2
      },
      "time": {
        "start_at": 1532065478.200753,
        "duration": 0.022025108337402344
      },
      "records": [
        {
          "name": "/api/get-token",
          "status": "success",
          "attachment": "",
          "meta_data": {
            "url": "http://127.0.0.1:5000/api/get-token",
            "method": "POST",
            "request_time": 1532065478.2021492,
            "request_headers": {
              "user-agent": "python-requests/2.18.4",
              "Accept-Encoding": "gzip,deflate",
              "Accept": "*/*",
              "Connection": "keep-alive",
              "content-type": "application/json",
              "app_version": "2.8.6",
              "device_sn": "FwgRiO7CNA50DSU",
              "os_platform": "ios",
              "user_agent": "iOS/10.3",
              "Content-Length": "52"
            },
            "request_body": {
              "sign": "958a05393efef0ac7c0fb80a7eac45e24fd40c27"
            },
            "status_code": 200,
            "response_headers": {
              "Content-Type": "application/json",
              "Content-Length": "46",
              "Server": "Werkzeug/0.14.1 Python/3.6.5+",
              "Date": "Fri, 20 Jul 2018 05:44:38 GMT"
            },
            "response_body": {
              "success": true,
              "token": "V968SAirRRZW8cs5"
            },
            "content_size": 46,
            "response_time_ms": 14.18,
            "elapsed_ms": 5.366,
            "validators": [
              {
                "check": "status_code",
                "expect": 200,
                "comparator": "eq",
                "check_value": 200,
                "check_result": "passed"
              },
              {
                "check": "content.success",
                "expect": true,
                "comparator": "eq",
                "check_value": true,
                "check_result": "passed"
              }
            ]
          }
        },
        {
          "name": "/api/users/1000",
          "status": "success",
          "attachment": "",
          "meta_data": {
            "url": "http://127.0.0.1:5000/api/users/1000",
            "method": "POST",
            "request_time": 1532065478.218334,
            "request_headers": {
              "user-agent": "python-requests/2.18.4",
              "Accept-Encoding": "gzip, deflate",
              "Accept": "*/*",
              "Connection": "keep-alive",
              "content-type": "application/json",
              "device_sn": "FwgRiO7CNA50DSU",
              "token": "V968SAirRRZW8cs5",
              "Content-Length": "39"
            },
            "request_body": {
              "name": "user1",
              "password": "123456"
            },
            "status_code": 201,
            "response_headers": {
              "Content-Type": "application/json",
              "Content-Length": "54",
              "Server": "Werkzeug/0.14.1 Python/3.6.5+",
              "Date": "Fri, 20 Jul 2018 05:44:38 GMT"
            },
            "response_body": {
              "success": true,
              "msg": "user created successfully."
            },
            "content_size": 54,
            "response_time_ms": 3.43,
            "elapsed_ms": 2.178,
            "validators": [
              {
                "check": "status_code",
                "expect": 201,
                "comparator": "eq",
                "check_value": 201,
                "check_result": "passed"
              },
              {
                "check": "headers.Content-Type",
                "expect": "application/json",
                "comparator": "eq",
                "check_value": "application/json",
                "check_result": "passed"
              }
            ]
          }
        }
      ],
      "output": [
        {
          "in": {},
          "out": {
            "token": "V968SAirRRZW8cs5"
          }
        }
      ]
    },
    {...}
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

# => reports/demo/demo-1532078874.html
```
