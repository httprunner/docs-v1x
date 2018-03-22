## 概述

HttpRunner 从 `1.2.3` 版本开始支持 hook 机制，可以在请求前和请求后调用钩子函数。

具体可实现如下目的：

- 请求前：调用钩子函数对请求的 kwargs 进行处理
- 请求后：调用钩子函数对响应实例进行处理

## 用例描述形式

在 YAML/JSON 测试用例的 request 部分新增关键字 `setup_hooks` 和 `teardown_hooks`。

- setup_hooks: 在 HTTP 请求发送前执行 hook 函数，主要用于准备工作，特别是对请求的 kwargs 进行预处理。
- teardown_hooks: 在 HTTP 请求发送后执行 hook 函数，主要用于测试后的清理工作。

```json
"test": {
    "name": "get token with $user_agent, $os_platform, $app_version",
    "request": {
        "url": "/api/get-token",
        "method": "POST",
        "headers": {
            "app_version": "$app_version",
            "os_platform": "$os_platform",
            "user_agent": "$user_agent"
        },
        "json": {
            "sign": "${get_sign($user_agent, $device_sn, $os_platform, $app_version)}"
        },
        "validate": [
            {"eq": ["status_code", 200]}
        ],
        "setup_hooks": [
            "setup_hook_prepare_kwargs",
            "setup_hook_httpntlmauth"
        ],
        "teardown_hooks": [
            "teardown_hook_sleep_1_secs"
        ]
    }
}
```

需要注意的是，在 setup_hooks 和 teardown_hooks 中只需指定 hook 函数的名称，参数部分无需指定，但需要在编写 hook 函数时遵循规范要求。

## 编写 hook 函数

### setup_hooks

hook 函数放置于 debugtalk.py 中，并且必须包含三个参数：

- method: 请求方法，e.g. GET, POST, PUT
- url: 请求 URL
- kwargs: request 的参数字典

e.g.

```python
def setup_hook_prepare_kwargs(method, url, kwargs):
    if method == "POST":
        content_type = kwargs.get("headers", {}).get("content-type")
        if content_type and "data" in kwargs:
            # if request content-type is application/json, request data should be dumped
            if content_type.startswith("application/json"):
                kwargs["data"] = json.dumps(kwargs["data"])

            # if charset is specified in content-type, request data should be encoded with charset encoding
            charset = get_charset_from_content_type(content_type)
            if charset:
                kwargs["data"] = kwargs["data"].encode(charset)

def setup_hook_httpntlmauth(method, url, kwargs):
    if "httpntlmauth" in kwargs:
        from requests_ntlm import HttpNtlmAuth
        auth_account = kwargs.pop("httpntlmauth")
        kwargs["auth"] = HttpNtlmAuth(
            auth_account["username"], auth_account["password"])
```

### teardown_hooks

teardown_hooks 函数放置于 debugtalk.py 中，并且必须包含一个参数：

- resp_obj: requests.Response 实例


e.g.

```python
def teardown_hook_sleep_1_secs(resp_obj):
    """ sleep 1 seconds after request
    """
    time.sleep(1)
```
