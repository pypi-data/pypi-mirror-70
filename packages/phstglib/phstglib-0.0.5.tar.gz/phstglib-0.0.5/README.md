http://MANIFEST.in表示打包时不会被自动包含进去的附加文件清单
# 打包上传
```shell script
python3 setup.py sdist # 进行打包
pip3 install twine     # 如果已经安装twine，跳过次步骤
python3 -m twine upload dist/*
```
