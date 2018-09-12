
## 文件类型说明

在 HttpRunner 自动化测试项目中，主要存在如下几类文件：

- `YAML/JSON`（必须）：测试用例文件，一个文件对应一条测试用例
- `debugtalk.py`（可选）：脚本函数，存储项目中逻辑运算函数
    - 该文件存在时，将作为项目根目录定位标记，其所在目录即被视为项目工程的根目录（当前工作目录`CWD`）
    - 该文件不存在时，运行测试的路径将被视为当前工作目录`CWD`
    - 测试用例文件中的相对路径（例如`.csv`）均需基于当前工作目录`CWD`
    - 运行测试后，测试报告文件夹（`reports`）会生成在当前工作目录`CWD`
- `.env`（可选）：存储项目环境变量
- `.csv`（可选）：项目数据文件，用于进行数据驱动

## 项目文件结构

### 简单场景（非测试用例分层结构）

对于接口数比较少，或者测试场景比较简单的项目，组织测试用例时无需分层。在此种情况下，项目文件的目录结构没有任何要求，在项目中只需要一堆 `YAML/JSON` 文件即可，每一个文件单独对应一条测试用例；根据需要，项目中可能还会有 `debugtalk.py`、`.env`等文件。

推荐的项目文件目录结构示例如下：

```bash
$ tree demo -a
demo
├── .env
├── debugtalk.py
├── reports
├── testcase1.yml
└── testcase2.json
```

### 测试用例分层结构

对于接口数比较多，或者测试场景比较复杂的项目，为了使测试用例更便于组织和维护，推荐使用`测试用例分层机制`，即单独维护 API 描述、测试用例和测试场景。

在此种情况下，项目文件的目录结构需要遵循一些规范：

- `debugtalk.py`：该文件所在目录将作为项目工程的根目录，api 和 testcases 文件夹都必须与其放置在相同目录；若没有该文件，
- api 文件夹：存储接口定义描述
- testcases 文件夹：存储测试用例定义描述，可用于组装形成复杂的测试场景
- reports 文件夹：存储 HTML 测试报告

对应的项目文件目录结构示例如下：

```bash
$ tree demo -a
demo
├── .env
├── api
│   └── user.yml
├── debugtalk.py
├── reports
│   └── 1535713039.html
├── testcases
│   ├── login.yml
│   └── logout.yml
└── testsuites
    └── login_and_logout.yml

4 directories, 7 files
```

**项目脚手架**

新建项目时，可使用 `--startproject` 脚手架功能快速创建项目目录结构；模式是采用`测试用例分层机制`。

```bash
$ hrun --startproject demo
Start to create new project: demo
CWD: /Users/debugtalk/MyProjects/examples

created folder: demo
created folder: demo/api
created folder: demo/testcases
created folder: demo/testsuites
created folder: demo/reports
created file: demo/debugtalk.py
created file: demo/.env
```
