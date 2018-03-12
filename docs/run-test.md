
## 指定用例集路径

使用 HttpRunner 指定用例集路径时，支持多种方式。

使用 hrun 命令外加单个测试用例文件的路径，运行单个测试用例集：

```text
$ hrun filepath/testcase.yml
```

使用 hrun 命令外加多个测试用例文件的路径，即可运行多个测试用例集：

```text
$ hrun filepath1/testcase1.yml filepath2/testcase2.yml
```

使用 hrun 命令外加文件夹的路径，即可运行指定文件夹下所有的测试用例集：

```text
$ hrun testcases_folder_path
```

## failfast

默认情况下，HttpRunner 会运行指定用例集中的所有测试用例，并统计测试结果。

> 对于某些依赖于执行顺序的测试用例集，例如需要先登录成功才能执行后续接口请求的场景，当前面的测试用例执行失败后，后续的测试用例也都必将失败，因此没有继续执行的必要了。

若希望测试用例集在运行过程中，遇到失败时不再继续运行后续用例，则可通过在命令中添加`--failfast`实现。

```text
$ hrun filepath/testcase.yml --failfast
```

## 日志级别

默认情况下，HttpRunner 运行时的日志级别为`INFO`，只会包含最基本的信息，包括用例名称、请求的URL和Method、响应结果的状态码、耗时和内容大小。

```
$ hrun tests/data/demo_parameters.yml
INFO     Loading environment variables from /Users/debugtalk/MyProjects/HttpRunner-dev/HttpRunner/.env
get token with iOS/10.1 and 2.8.5
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 11 ms, response_length: 46 bytes
.

----------------------------------------------------------------------
Ran 1 test in 0.013s

OK
INFO     Start to render Html report ...
INFO     Generated Html report: /Users/debugtalk/MyProjects/HttpRunner-dev/HttpRunner/reports/2018-03-12-19-12-56.html
```

若需要查看到更详尽的信息，例如请求的参数和响应的详细内容，可以将日志级别设置为`DEBUG`，即在命令中添加`--log-level debug`。

```
$ hrun tests/data/demo_parameters.yml --log-level debug
get token with iOS/10.1 and 2.8.5
INFO     POST http://127.0.0.1:5000/api/get-token
DEBUG    request kwargs(raw): {'headers': {'content-type': 'application/json', 'device_sn': '9LLPuda32cEj6BE', 'user_agent': 'iOS/10.1', 'os_platform': 'ios', 'app_version': '2.8.5'}, 'json': {'sign': '49566bce2bbf3a577a2a97bd95ca1dd5bd4af5b3'}}
DEBUG    request kwargs(processed): {'headers': {'content-type': 'application/json', 'device_sn': '9LLPuda32cEj6BE', 'user_agent': 'iOS/10.1', 'os_platform': 'ios', 'app_version': '2.8.5'}, 'json': {'sign': '49566bce2bbf3a577a2a97bd95ca1dd5bd4af5b3'}, 'timeout': 120}
DEBUG    Starting new HTTP connection (1): 127.0.0.1
DEBUG    http://127.0.0.1:8888 "POST http://127.0.0.1:5000/api/get-token HTTP/1.1" 200 46
DEBUG    response status_code: 200
DEBUG    response headers: {'Content-Type': 'application/json', 'Content-Length': '46', 'Server': 'Werkzeug/0.14.1 Python/3.6.4', 'Date': 'Mon, 12 Mar 2018 11:11:48 GMT','Proxy-Connection': 'Close'}
DEBUG    response body: {"success": true, "token": "3DFzZen272dbS7qh"}
INFO     status_code: 200, response_time: 21 ms, response_length: 46 bytes
.

----------------------------------------------------------------------
Ran 1 test in 0.023s

OK
DEBUG    No html report template specified, use default.
INFO     Start to render Html report ...
DEBUG    render data: {'success': True, 'stat': {'testsRun': 1, 'failures': 0, 'errors': 0, 'skipped': 0, 'expectedFailures': 0, 'unexpectedSuccesses': 0, 'successes': 1}, 'platform': {'httprunner_version': '1.1.0', 'python_version': 'CPython 3.6.4', 'platform': 'Darwin-17.4.0-x86_64-i386-64bit'}, 'time': {'start_at': datetime.datetime(2018, 3, 12, 19, 11, 48, 588562), 'duration': 0.04852795600891113}, 'records': [{'name': 'get token with iOS/10.1 and 2.8.5', 'status': 'success', 'response_time': 21, 'attachment': '', 'meta_data': {'method': 'POST', 'request_time': 1520853108.589503, 'response_time': 21, 'elapsed': 0.00506, 'url': '/api/get-token', 'request_headers': {'User-Agent': 'python-requests/2.18.4', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'content-type': 'application/json', 'device_sn': '9LLPuda32cEj6BE', 'user_agent': 'iOS/10.1', 'os_platform': 'ios', 'app_version': '2.8.5', 'Content-Length': '52'}, 'request_body': '{"sign": "49566bce2bbf3a577a2a97bd95ca1dd5bd4af5b3"}', 'status_code': 200, 'response_headers': {'Content-Type': 'application/json', 'Content-Length': '46', 'Server': 'Werkzeug/0.14.1 Python/3.6.4', 'Date': 'Mon, 12 Mar 2018 11:11:48 GMT', 'Proxy-Connection': 'Close'}, 'response_body': '{"success": true, "token": "3DFzZen272dbS7qh"}', 'content_size': 46}}]}
INFO     Generated Html report: /Users/debugtalk/MyProjects/HttpRunner-dev/HttpRunner/reports/2018-03-12-19-11-48.html
DEBUG
================== Variables & Output ==================
Type   | Variable         :  Value
------ | ---------------- :  ---------------------------
Var    | user_agent       :  iOS/10.1
Var    | device_sn        :  ${gen_random_string(15)}
Var    | os_platform      :  ios
Var    | app_version      :  2.8.5

Out    | token            :  3DFzZen272dbS7qh
--------------------------------------------------------
```
