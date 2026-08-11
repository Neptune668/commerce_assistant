from pathlib import Path


def load_prompt(prompt_file_name: str)-> str:
    """
    根据提示词模版文件的文件名加载模版内容字符串到内存
    :param prompt_file_name:
    :return:
    """

    # 1. 组装模版文件的path路径对象
    prompt_file_path = Path(__file__).resolve().parents[0] / "jinja2" / f"{prompt_file_name}.jinja2"
    # 2. 将模板的内容读取到内存中（尚未渲染占位符）
    return prompt_file_path.read_text(encoding="utf-8")

if __name__ == '__main__':

    result = load_prompt("turn_plan")
    print( result)