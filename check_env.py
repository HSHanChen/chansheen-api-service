# """
# @Author: Chan Sheen
# @Date: 2025/6/17 15:04
# @File: check_env.py
# @Description:
# """
# import os
# from dotenv import load_dotenv
#
# def validate_env_vars(required_vars):
#     print("🔍 开始加载 .env 文件...")
#     # 这里不传路径，默认从运行目录及其父目录查找 .env 文件
#     env_loaded = load_dotenv()
#     print(f"✅ .env 文件加载状态: {'成功' if env_loaded else '未找到 .env 文件'}")
#
#     # 打印 .env 文件的实际路径（如果能找到）
#     dotenv_path = os.getenv("DOTENV_PATH", "未检测到环境变量 DOTENV_PATH")
#     print(f"🔗 环境变量来源路径: {dotenv_path}")
#
#     print("\n📝 关键环境变量检查:")
#     missing_vars = []
#     for var in required_vars:
#         value = os.getenv(var)
#         if value is None or value.strip() == "":
#             print(f"❌ 缺少环境变量: {var}")
#             missing_vars.append(var)
#         else:
#             # 出于安全考虑，密码部分隐藏
#             if "PASS" in var.upper() or "SECRET" in var.upper():
#                 show_val = value[:3] + "****" + value[-3:] if len(value) > 6 else "****"
#             else:
#                 show_val = value
#             print(f"✔ {var} = {show_val}")
#
#     if missing_vars:
#         print("\n⚠️ 请确保上述缺失环境变量已正确配置于 .env 文件或系统环境变量中！")
#         return False
#     else:
#         print("\n🎉 所有必需环境变量均已加载！")
#         return True
#
# if __name__ == "__main__":
#     required_variables = [
#         "DB_USER",
#         "DB_PASSWORD",
#         "DB_HOST",
#         "DB_PORT",
#         "DB_NAME",
#         # 如果有别的环境变量，也可以加进来
#     ]
#
#     success = validate_env_vars(required_variables)
#     if not success:
#         print("环境变量校验未通过，程序退出！")
#         exit(1)
#     else:
#         print("环境变量校验通过，程序可继续运行。")
