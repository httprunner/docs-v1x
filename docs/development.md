# 开发扩展

HttpRunner 除了作为命令行工具使用外，还可以作为软件包集成到你自己的项目中。

简单来说，HttpRunner 提供了运行 YAML/JSON 格式测试用例的能力，并能返回详细的测试结果信息。

典型的调用方式如下：

```python
from httprunner import HttpRunner

kwargs = {
    "failfast": False
}
result = HttpRunner("docs/data/demo-quickstart-2.yml", **kwargs).run(
    html_report_name="demo",
    html_report_template="/path/to/custom_report_template"
)
```

调用完成后，在返回值（result）中包含详尽的运行结果数据，其数据结构为：

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
    "python_version": "CPython_3.6.4",
    "platform": "Darwin-17.4.0-x86_64-i386-64bit"
  },
  "time": {
    "start_at": datetime.datetime(2018, 2, 27, 17, 8, 42, 194945),
    "duration": 0.02808094024658203
  },
  "records": [
    {
      "name": "/api/get-token",
      "status": "success",
      "response_time": 10,
      "attachment": "",
      "meta_data": {
        "method": "POST",
        "request_time": 1519722522.195414,
        "response_time": 10,
        "elapsed": 0.002336,
        "url": "/api/get-token",
        "request_headers": {...},
        "request_body": "{"sign": "958a05393efef0ac7c0fb80a7eac45e24fd40c27"}",
        "status_code": 200,
        "response_headers": {...},
        "response_body": "{"success": true, "token": "yf7zUuLBIUD1nYXt"}",
        "content_size": 46
      }
    },
    {
      "name": "/api/users/1000",
      "status": "success",
      "response_time": 2,
      "attachment": "",
      "meta_data": {
        "method": "POST",
        "request_time": 1519722522.2067862,
        "response_time": 2,
        "elapsed": 0.001785,
        "url": "/api/users/1000",
        "request_headers": {...},
        "request_body": "{"name": "user1", "password": "123456"}",
        "status_code": 201,
        "response_headers": {...},
        "response_body": "{"success": true, "msg": "user created successfully."}",
        "content_size": 54
      }
    }
  ],
  "report_path": "reports/demo/demo-2018-02-27-17-08-42.html",
  "output": {"token": "Yfkzr0t3qdTAU7AD"}
}
```
