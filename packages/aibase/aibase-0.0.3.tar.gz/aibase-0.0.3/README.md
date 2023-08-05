
# 简介
    提供基础方法调用，规范代码风格


# 结构介绍
        aibase
            common # 通用
            middleware # 中间件相关
            utils # 工具
        README.md   # 说明文档
        setup.py # 构建




# 打包上传
## 环境安装
python -m pip install --user --upgrade setuptools wheel
python -m pip install --user --upgrade twine
## 打包
python setup.py sdist bdist_wheel
## 上传
python -m twine upload  dist/*