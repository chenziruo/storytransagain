# import re

# def extract_and_convert_requirements(conda_file_path, pip_file_path):
#     with open(conda_file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     pip_requirements = []

#     # 正则表达式匹配包名、版本号和pypi_0 (假设文件格式始终是包名=版本号=pypi_0)
#     conda_pattern = re.compile(r"^\s*([a-zA-Z0-9\-\_]+)=([\d\.]+)=pypi_0\s*$")

#     for line in lines:
#         match = conda_pattern.match(line)
#         if match:
#             # 提取包名和版本号，并修改等号为双等号
#             pip_requirements.append(f"{match.group(1)}=={match.group(2)}\n")

#     # 将结果写入新的 pip_requirements.txt 文件
#     with open(pip_file_path, 'w', encoding='utf-8') as pip_file:
#         pip_file.writelines(pip_requirements)

#     print(f"Extracted pip requirements have been saved to {pip_file_path}")

# # 使用示例
# conda_file_path = 'requirement.txt'  # 你的 Conda 格式的文件路径
# pip_file_path = 'pip_requirement.txt'  # 输出的 Pip 格式文件路径

# extract_and_convert_requirements(conda_file_path, pip_file_path)

# # 打开文件读取和写入
# with open('requirement.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()

# # 去除每行末尾的 =pypi_0
# with open('requirementWithoutPipy.txt', 'w', encoding='utf-8') as file:
#     for line in lines:
#         # 如果行末以 '=pypi_0' 结尾，则去除它
#         if line.endswith('=pypi_0\n'):
#             file.write(line[:-8] + '\n')  # 去除末尾的 '=pypi_0'
#         else:
#             file.write(line)  # 不修改其他行


# 读取requirements.txt并提取包名和版本
import re

# 读取requirements.txt并提取包名和版本
with open('requirementWithoutPipy.txt') as req_file:
    required_packages = {}
    for line in req_file:
        line = line.strip()
        if line and not line.startswith("#"):  # 排除注释
            # 提取包名和版本
            match = re.match(r'([a-zA-Z0-9\-]+)(==(.+))?', line)
            if match:
                package = match.group(1)
                version = match.group(3) if match.group(3) else None
                required_packages[package] = version

# 读取installed_packages.txt并提取已安装的包名和版本
with open('installed_packages.txt') as installed_file:
    installed_packages = {}
    for line in installed_file:
        line = line.strip()
        if line and not line.startswith("#"):  # 排除注释
            # 匹配包名和版本，忽略路径信息
            match = re.match(r'([a-zA-Z0-9\-]+)(==(.+))?', line)
            if match:
                package = match.group(1)
                version = match.group(3) if match.group(3) else None
                installed_packages[package] = version

# 查找缺失的包并加上版本信息
missing_packages = []
for package, required_version in required_packages.items():
    installed_version = installed_packages.get(package)
    # 如果版本不匹配或未安装该包
    if installed_version != required_version:
        if required_version:
            missing_packages.append(f"{package}=={required_version}")
        else:
            missing_packages.append(package)

# 输出未安装的包
with open('missing_packages.txt', 'w') as output_file:
    output_file.write("\n".join(missing_packages))

# 打印缺失的包
print("Missing packages:", missing_packages)
