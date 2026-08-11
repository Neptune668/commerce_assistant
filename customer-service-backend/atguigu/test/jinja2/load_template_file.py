import os

from jinja2 import FileSystemLoader, Environment

# 1. 获取当前文件所在目录
current_dir = os.path.dirname(__file__)
# 2. 文件加载器
file_system_loader = FileSystemLoader(current_dir)
# 3. 初始化jinja2的模版渲染环境
env = Environment(loader=file_system_loader)
# 4. 使用env加载模版文件
tpl = env.get_template("template.jinja2")

# 5. 定义数据
data = {
    "question": "Jinja2和f-string有什么区别？",
    "docs": [
        {"content": "Jinja2是专业第三方模板引擎，支持循环、判断、外部文件"},
        {"content": "f-string是Python原生字符串格式化，仅适合简单文本"}
    ],
    "history": [
        {"role": "user", "content": "什么是Prompt模板？"},
        {"role": "assistant", "content": "用来动态生成发给大模型指令的文本工具"}
    ]
}

# 6. 渲染模板获取最终提示词
full_prompt = tpl.render(**data)

print(full_prompt)