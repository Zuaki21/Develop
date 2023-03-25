import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


def collect_links():
    links = []
    for root, dirs, files in os.walk("."):
        if root.count(os.sep) == 1:
            for file in files:
                if file == "index.html":
                    path = os.path.join(root, file)
                    project_name = os.path.basename(os.path.dirname(path))
                    # ファイルの更新日時を取得し、日付時刻オブジェクトに変換する
                    mod_time = os.path.getmtime(path)
                    dt_object = datetime.fromtimestamp(mod_time)
                    # 更新日時をリンクに追加する
                    link = f'<a href="{path}">{project_name}</a> ({dt_object.strftime("%Y/%m/%d %H:%M")}更新)'
                    links.append((dt_object, link))
    # 更新日時でソートされたリンクのリストを返す(最近更新された順)
    return [link[1] for link in sorted(links, reverse=True)]


def render_template(links):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("IndexGenerator/template.html")
    data = {"links": links}
    output = template.render(data)
    with open("index.html", "w") as f:
        f.write(output)


if __name__ == "__main__":
    links = collect_links()
    render_template(links)
