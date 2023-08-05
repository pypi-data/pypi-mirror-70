# Winney 面向对象的 HTTP 请求  

## Tutorial
``` python
wy = Winney(host="www.baidu.com")
wy.add_url(method="get", uri="/", function_name="download")
wy.download()
t = wy.get_bytes()
print(t)
```
