from jinja2 import Template

tpl = Template("用户:{{name}}，年龄:{{age}}")
result = tpl.render(name="张三", age=18)
print(result)