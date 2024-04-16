import os


def count_lines_of_code(directory):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # 只统计 Python 文件
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    total_lines += len(lines)
    return total_lines


if __name__ == "__main__":
    project_directory = "E:\PycharmProjects\问答系统\APP"  # 替换为你的项目文件夹路径
    lines_of_code = count_lines_of_code(project_directory)
    print("Total lines of code:", lines_of_code)
