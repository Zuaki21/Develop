import os
import subprocess
import json
from datetime import datetime, timezone, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']),
    extensions=['jinja2.ext.i18n']
)


def collect_links():
    links = []
    for root, dirs, files in os.walk("."):
        if root.count(os.sep) == 1:
            for file in files:
                if file == "index.html":
                    path = os.path.join(root, file)
                    project_name = os.path.basename(os.path.dirname(path))
                    dir = os.path.dirname(path)
                    timeText, dayTime = get_last_updated(dir)
                    # 更新日時をリンクに追加する
                    link = f'<a href="{path}">{project_name}</a> ({timeText})'
                    # リンクと更新日時をタプルにしてリストに追加する
                    links.append((dayTime, link))
    # リストを更新日時でソートする
    return [link[1] for link in sorted(links, reverse=True, key=lambda x: x[0])]


def render_template(links):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("IndexGenerator/template.html")
    data = {"links": links}
    output = template.render(data)
    with open("index.html", "w") as f:
        f.write(output)


def get_last_updated(dir):
    # ファイルの存在を確認する
    if os.path.exists(dir+"/repo_info.json"):
        # dirからファイルパスを取得する
        with open(dir+"/repo_info.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        last_updated = data["last_updated"]
        # 更新日時をDateTime型に変換する
        dayTime = datetime.strptime(last_updated, '%Y/%m/%d %H:%M')
        return last_updated+"更新", dayTime
    else:
        return "更新日時不明", None


if __name__ == "__main__":
    links = collect_links()
    render_template(links)
