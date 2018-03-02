
## 概述

HttpRunner 的测试用例支持两种文件格式：YAML 和 JSON。

JSON 和 YAML 格式的测试用例完全等价，包含的信息内容也完全相同。

- 对于新手来说，推荐使用 JSON 格式，虽然描述形式上稍显累赘，但是不容易出错（大多编辑器都具有 JSON 格式的检测功能）；
- 对于熟悉 YAML 格式的人来说，编写维护 YAML 格式的测试用例会更简洁，但前提是要保证 YAML 格式没有语法错误。

对于两种格式的展示差异，可以对比查看 [demo-quickstart-6.json](data/demo-quickstart-6.json) 和 [demo-quickstart-6.yml](data/demo-quickstart-6.yml) 获取初步的印象。

后面为了更清晰的描述，统一采用 JSON 格式作为示例。

## 测试用例组织形式

在 HttpRunner 中，测试用例组织主要基于两种概念（在不考虑用例分层概念的情况下）：

- 测试用例集（testset）：单个或多个测试用例的集合，存储形式为一个 YAML/JSON 文件
- 测试用例（testcase）：单次请求、响应、校验过程，对应 YAML/JSON 文件中的一个 test

对于单个 YAML/JSON 文件来说，数据存储结构为 `list of dict` 的形式，其中可能包含一个全局配置项（config）和若干个测试用例（test）；测试用例存在顺序关系，运行时将从前往后依次运行。

对应的 JSON 格式如下所示：

```json
[
  {
    "config": {...}
  },
  {
    "test": {...}
  },
  {
    "test": {...}
  }
]
```

具体方面：

- config：作为整个测试用例集的全局配置项
- test：对应单个测试用例

## 变量空间（context）作用域

在变量空间作用域方面，HttpRunner 进行了清晰的划分。

- config：作为整个测试用例集的全局配置项，作用域为整个测试用例集；
- test：变量空间（context）会继承 config 中定义的内容；
    - 若某变量在 config 中定义了，在某 test 中没有定义，则该 test 会继承该变量
    - 若某变量在 config 和某 test 中都定义了，则该 test 中使用自己定义的变量值
- 各个测试用例（test）的变量空间相对独立，互不影响；
- 如需在多个测试用例（test）中传递参数值，则需要使用 extract 关键字，并且只能从前往后传递

## config

### name

- 必填：测试用例集的名称

### variables

### parameters

### request

- base_url
- headers

### output

## test

### name

- 必填：测试用例的名称

### variables

### request

### extract

### validate

