# update_version_timestamp.py
import datetime
import re

if __name__ == "__main__":
    # open file __main__.py in the same directory of this file
    main_py_file = "stool/__main__.py"
    # 更新version.py文件
    with open(main_py_file, "r") as file:
        content = file.read()

    # 替换时间戳
    now_yyyy_mm_dd_HH_mm_ss = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = re.sub(r'latest_commit_time = ".*"', f'latest_commit_time = "{now_yyyy_mm_dd_HH_mm_ss}"', content)

    with open(main_py_file, "w") as file:
        file.write(content)
