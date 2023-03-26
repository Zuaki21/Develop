import os
import subprocess
import json
from datetime import datetime, timezone, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pytz
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
                    timeText, dayTime, description = get_last_updated(dir)
                    # 更新日時をリンクに追加する
                    link = make_link(path, project_name,
                                     timeText, dayTime, description)
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

        # 説明を取得する
        description = data["description"]
        if description is "" or description is None:
            description = "説明文なし"

        return last_updated+"更新", dayTime, description
    else:
        return "更新日時不明", None, "説明文不明"


def make_link(path, project_name, timeText, dayTime, description):
    text_color = "text-gray-400"

    # dayTimeがNoneでない場合
    if dayTime is not None:
        # 日本時間のタイムゾーンオブジェクトを作成
        jst = pytz.timezone('Asia/Tokyo')
        # dayTimeを日本時間に変換
        dayTime = jst.localize(dayTime)
        # 1日以内の場合
        if dayTime > datetime.now(jst) - timedelta(days=1):
            text_color = "text-green-300"

    # 更新日時をリンクに追加する
    link = f'''
    <a
        class="border border-white rounded-lg p-4 h-full hover:bg-gray-800 flex flex-col block"
        href="{path}"
    >
        <p class="text-white font-bold mb-2">{project_name}</p>
        <p class="text-gray-400 text-sm mb-2">
            {description}
        </p>
        <p class="{text_color} text-sm mt-auto ml-auto">
            ({timeText})
        </p>
    </a>'''
    return link


if __name__ == "__main__":
    links = collect_links()
    render_template(links)
