
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

Running tests...
----------------------------------------------------------------------
 get token with iOS/10.3 and 2.8.6 ... INFO:root: Start to POST http://127.0.0.1:5000/api/get-token
INFO:root: status_code: 200, response_time: 12 ms, response_length: 46 bytes
OK (0.014408)s

----------------------------------------------------------------------
Ran 1 test in 0.015s
```

若需要查看到更详尽的信息，例如请求的参数和响应的详细内容，可以将日志级别设置为`DEBUG`，即在命令中添加`--log-level debug`。

```
$ hrun tests/data/demo_parameters.yml --log-level debug

Running tests...
----------------------------------------------------------------------
 get token with iOS/10.3 and 2.8.6 ... INFO:root: Start to POST http://127.0.0.1:5000/api/get-token
DEBUG:root: kwargs: {'headers': {'Content-Type': 'application/json', 'device_sn': 'eOq6w6T7DaFnHvu', 'user_agent': 'iOS/10.3', 'os_platform': 'ios', 'app_version': '2.8.6'}, 'json': {'sign': '354432a9efd9111e8ee2a77f9c08124d997876a9'}}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:5000 "POST /api/get-token HTTP/1.1" 200 46
DEBUG:root: response: {'method': 'POST', 'start_time': 1518884607.878689, 'url': '/api/get-token', 'response_time': 11, 'content_size': 46, 'request_headers': {'User-Agent': 'python-requests/2.18.4', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'device_sn': 'eOq6w6T7DaFnHvu', 'user_agent': 'iOS/10.3', 'os_platform': 'ios', 'app_version': '2.8.6', 'Content-Length': '52'}, 'request_body':b'{"sign": "354432a9efd9111e8ee2a77f9c08124d997876a9"}', 'status_code': 200, 'response_headers': {'Content-Type': 'application/json', 'Content-Length': '46', 'Server': 'Werkzeug/0.14.1 Python/3.6.4', 'Date': 'Sat, 17 Feb 2018 16:23:27 GMT'}, 'response_content': b'{"success": true, "token": "Wo2J1hKCdSq7l66s"}'}
INFO:root: status_code: 200, response_time: 11 ms, response_length: 46 bytes
OK (0.013259)s

----------------------------------------------------------------------
Ran 1 test in 0.013s
```
