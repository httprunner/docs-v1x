
## 项目脚手架

创建项目时，可使用`--startproject`脚手架功能。

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

$ tree demo -a
demo
├── .env
├── api
├── debugtalk.py
├── reports
├── testcases
└── testsuites

4 directories, 2 files
```

## 文件类型说明

在自动化测试项目中，主要存在如下几类文件：

- `YAML/JSON`：测试用例文件，一个文件对应一条测试用例
- `debugtalk.py`：脚本函数，存储项目中逻辑运算函数
- `.env`：项目环境变量
- `.csv`：项目数据文件，用于进行数据驱动
