## 介绍

在自动化测试中，经常会遇到如下场景：

- 测试搜索功能，只有一个搜索输入框，但有10种不同类型的搜索关键字；
- 测试账号登录功能，需要输入用户名和密码，按照等价类划分后有20种组合情况。

这里只是随意找了两个典型的例子，相信大家都有遇到过很多类似的场景。总结下来，就是在我们的自动化测试脚本中存在参数，并且我们需要采用不同的参数去运行。

经过概括，参数基本上分为两种类型：

- 单个独立参数：例如前面的第一种场景，我们只需要变换搜索关键字这一个参数
- 多个具有关联性的参数：例如前面的第二种场景，我们需要变换用户名和密码两个参数，并且这两个参数需要关联组合

然后，对于参数而言，我们可能具有一个参数列表，在脚本运行时需要按照不同的规则去取值，例如顺序取值、随机取值、循环取值等等。

这就是典型的参数化和数据驱动。

如需了解 HttpRunner 参数化数据驱动机制的实现原理和技术细节，可前往阅读[《HttpRunner 实现参数化数据驱动机制》](http://debugtalk.com/post/httprunner-data-driven/)。

## 数据驱动作用域

从 1.5.11 版本开始，HttpRunner 不再支持测试步骤（teststep）层级的参数化数据驱动，只支持测试用例（testcase）层级的参数化驱动配置。

配置方式包括三个部分：参数定义、数据源指定、数据源准备。

## 参数定义 & 数据源指定

在 YAML/JSON 测试用例的 config 模块中，新增一个`parameters`字段，参数化的定义均放置在该字段下。

定义内容包括参数名称和数据源指定。

参数名称的定义分为两种情况：

- 独立参数单独进行定义；
- 多个参数具有关联性的参数需要将其定义在一起，采用短横线（`-`）进行连接。

数据源指定支持三种方式：

- 在 YAML/JSON 中直接指定参数列表
- 通过内置的 parameterize（可简写为P）函数引用 CSV 文件
- 调用 debugtalk.py 中自定义的函数生成参数列表

示例如下：

```yaml
- config:
    name: "demo"
    parameters:
        - user_agent: ["iOS/10.1", "iOS/10.2", "iOS/10.3"]
        - user_id: ${P(user_id.csv)}
        - username-password: ${get_account(10)}
```

在这三种方式中，第一种方式最为简单易用，适合参数列表比较小的情况；第二种方式只需要准备 CSV 数据文件，即可实现复杂的数据驱动机制；第三种方式最为灵活，可在 debugtalk.py 通过自定义 Python 函数实现任意场景的数据驱动机制。

三种方式可根据实际项目需求进行灵活选择，同时支持多种方式的组合使用。假如测试用例中定义了多个参数，那么测试用例在运行时会对参数进行笛卡尔积组合，覆盖所有参数组合情况。

## 数据源准备

针对数据源的不同指定方式，参数的准备方式也各不相同。

### 直接指定参数列表

对于参数列表比较小的情况，最简单的方式是直接在 YAML/JSON 中指定参数列表内容。

例如，对于独立参数 user_agent，参数列表为 `["iOS/10.1", "iOS/10.2", "iOS/10.3"]`，那么就可以按照如下方式进行配置：

```yaml
- config:
    parameters:
        - user_agent: ["iOS/10.1", "iOS/10.2", "iOS/10.3"]
```

进行该配置后，测试用例集在运行时就会对 user_agent 实现数据驱动，即分别使用 "iOS/10.1"、"iOS/10.2"、"iOS/10.3" 三个值运行测试用例集。

对于具有关联性的多个参数，例如 username 和 password，那么就可以按照如下方式进行配置：

```yaml
- config:
    parameters:
        - username-password:
            - ["user1", "111111"]
            - ["user2", "222222"]
            - ["user3", "333333"]
```

进行该配置后，测试用例集在运行时就会对 username 和 password 实现数据驱动，并且保证参数值总是成对使用。

### 引用 CSV 数据文件

对于已有参数列表，并且数据量比较大的情况，比较适合的方式是将参数列表值存储在 CSV 数据文件中。

对于 CSV 数据文件，需要遵循如下几项约定的规则：

- 文件需放置在与测试用例文件相同的目录中；
- CSV 文件中的第一行必须为参数名称，从第二行开始为参数值，每个（组）值占一行；
- 若同一个 CSV 文件中具有多个参数，则参数名称和数值的间隔符需实用英文逗号。

例如，user_id 的参数取值范围为 1001～2000，那么我们就可以创建 user_id.csv，并且在文件中按照如下形式进行描述。

```csv
user_id
1001
1002
...
1999
2000
```

然后在 YAML/JSON 测试用例文件中，就可以通过内置的 parameterize（可简写为P）函数引用 CSV 文件。

```yaml
- config:
    parameters:
        - user_id: ${parameterize(user_id.csv)}
        - user_id: ${P(user_id.csv)}    # 简写方式
```

对于具有关联性的多个参数，例如 username 和 password，那么就可以创建 [account.csv](/data/account.csv)，并在文件中按照如下形式进行描述。

```csv
username,password
test1,111111
test2,222222
test3,333333
```

然后在 YAML/JSON 测试用例文件中，就可以通过内置的 parameterize（可简写为P）函数引用 CSV 文件。

```yaml
- config:
    parameters:
        - username-password: ${parameterize(account.csv)}
        - username-password: ${P(account.csv)}  # 简写方式
```

需要说明的是，在 parameters 中指定的参数名称必须与 CSV 文件中第一行的参数名称一致，顺序可以不一致，参数个数也可以不一致。

例如，在 [account.csv](/data/account.csv) 文件中可以包含多个参数，username、password、phone、age：

```csv
username,password,phone,age
test1,111111,18600000001,21
test2,222222,18600000002,22
test3,333333,18600000003,23
```

而在 YAML/JSON 测试用例文件中指定参数时，可以只使用部分参数，并且参数顺序无需与 CSV 文件中参数名称的顺序一致。

```yaml
- config:
    parameters:
        - phone-username: ${parameterize(account.csv)}
        - phone-username: ${P(account.csv)}  # 简写方式
```

### 自定义函数生成参数列表

对于没有现成参数列表，或者需要更灵活的方式动态生成参数的情况，可以通过在 debugtalk.py 中自定义函数生成参数列表，并在 YAML/JSON 引用自定义函数的方式。

例如，若需对 user_id 进行参数化数据驱动，参数取值范围为 1001～1004，那么就可以在 debugtalk.py 中定义一个函数，返回参数列表。

```python
def get_user_id():
    return [
        {"user_id": 1001},
        {"user_id": 1002},
        {"user_id": 1003},
        {"user_id": 1004}
    ]
```

然后，在 YAML/JSON 的 parameters 中就可以通过调用自定义函数的形式来指定数据源。

```yaml
- config:
    parameters:
        - user_id: ${get_user_id()}
```

另外，通过函数的传参机制，还可以实现更灵活的参数生成功能。

例如，在 debugtalk.py 中定义函数 get_account，可生成指定数量的参数列表。

```python
def get_account(num):
    accounts = []
    for index in range(1, num+1):
        accounts.append(
            {"username": "user%s" % index, "password": str(index) * 6},
        )

    return accounts
```

那么在 YAML/JSON 的 parameters 中就可以调用自定义函数生成指定数量的参数列表。

```yaml
- config:
    parameters:
        - username-password: ${get_account(10)}
```

> 需要注意的是，在自定义函数中，生成的参数列表必须为 `list of dict` 的数据结构，该设计主要是为了与 CSV 文件的处理机制保持一致。

## 参数化运行

完成以上参数定义和数据源准备工作之后，参数化运行与普通测试用例的运行完全一致。

采用 hrun 命令运行自动化测试：

```bash
$ hrun tests/data/demo_parameters.yml
```

采用 locusts 命令运行性能测试：

```bash
$ locusts -f tests/data/demo_parameters.yml
```

区别在于，测试用例集在运行时会分别运行每一种组合情况；自动化测试时遍历一遍后会终止执行，性能测试时每个用户都会循环遍历。

## 案例演示

假设我们有一个获取token的接口，我们需要使用 user_agent 和 app_version 这两个参数来进行参数化数据驱动。

YAML 测试用例的描述形式如下所示：

```yaml
- config:
    name: "user management testcase."
    parameters:
        - user_agent: ["iOS/10.1", "iOS/10.2", "iOS/10.3"]
        - app_version: ${P(app_version.csv)}
        - os_platform: ${get_os_platform()}
    variables:
        - user_agent: 'iOS/10.3'
        - device_sn: ${gen_random_string(15)}
        - os_platform: 'ios'
        - app_version: '2.8.6'
    request:
        base_url: http://127.0.0.1:5000
        headers:
            Content-Type: application/json
            device_sn: $device_sn

- test:
    name: get token with $user_agent, $os_platform, $app_version
    request:
        url: /api/get-token
        method: POST
        headers:
            app_version: $app_version
            os_platform: $os_platform
            user_agent: $user_agent
        json:
            sign: ${get_sign($user_agent, $device_sn, $os_platform, $app_version)}
    extract:
        - token: content.token
    validate:
        - eq: [status_code, 200]
        - eq: [headers.Content-Type, application/json]
        - eq: [content.success, true]
```

其中，[app_version](/data/app_version.csv) 的数据源列表为：

```csv
app_version
2.8.5
2.8.6
```

获取 os_platform 的自定义函数为：

```python
def get_os_platform():
    return [
        {"os_platform": "ios"},
        {"os_platform": "android"}
    ]
```

那么，经过笛卡尔积组合，应该总共有 `3*2*2` 种参数组合情况。

最终的测试结果如下所示：

```
$ hrun tests/data/demo_parameters.yml
get token with iOS/10.1, ios, 2.8.5
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 12 ms, response_length: 46 bytes
.
get token with iOS/10.1, android, 2.8.5
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 5 ms, response_length: 46 bytes
.
get token with iOS/10.1, ios, 2.8.6
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 3 ms, response_length: 46 bytes
.
get token with iOS/10.1, android, 2.8.6
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 3 ms, response_length: 46 bytes
.
get token with iOS/10.2, ios, 2.8.5
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 3 ms, response_length: 46 bytes
.
get token with iOS/10.2, android, 2.8.5
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 3 ms, response_length: 46 bytes
.
get token with iOS/10.2, ios, 2.8.6
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 4 ms, response_length: 46 bytes
.
get token with iOS/10.2, android, 2.8.6
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 4 ms, response_length: 46 bytes
.
get token with iOS/10.3, ios, 2.8.5
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 20 ms, response_length: 46 bytes
.
get token with iOS/10.3, android, 2.8.5
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 5 ms, response_length: 46 bytes
.
get token with iOS/10.3, ios, 2.8.6
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 6 ms, response_length: 46 bytes
.
get token with iOS/10.3, android, 2.8.6
INFO     POST http://127.0.0.1:5000/api/get-token
INFO     status_code: 200, response_time: 7 ms, response_length: 46 bytes
.

----------------------------------------------------------------------
Ran 12 tests in 0.109s

OK
```
