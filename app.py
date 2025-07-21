import streamlit as st
import base64
import requests
from github import Github  # 需安装 PyGithub

# GitHub 配置（替换为你的信息）
GITHUB_TOKEN = st.secrets["github"]["token"]  # 从 Streamlit Secrets 获取
REPO_NAME = "你的用户名/你的仓库名"  # 例如 "Tom/Video-Repo"
BRANCH = "main"

# 初始化 GitHub 客户端
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

st.title("🎥 GitHub 视频共享平台")
st.markdown("用户A上传 → 自动保存到GitHub → 用户B直接播放")

# 文件上传
uploaded_file = st.file_uploader("选择视频文件（<25MB）", type=["mp4", "mov"])

if uploaded_file:
    file_name = uploaded_file.name
    file_content = uploaded_file.read()

    # 检查文件大小（GitHub免费版限制单文件<25MB）
    if len(file_content) > 25 * 1024 * 1024:
        st.error("文件需小于25MB（GitHub免费账户限制）")
    else:
        # 上传到 GitHub
        try:
            repo.create_file(
                path=f"videos/{file_name}",
                message=f"Add video: {file_name}",
                content=file_content,
                branch=BRANCH
            )
            st.success("视频已上传到 GitHub！")

            # 生成直链（用户B可播放）
            raw_url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/videos/{file_name}"
            st.video(raw_url)
            st.markdown(f"**共享链接（永久有效）:**\n\n`{raw_url}`")
            
        except Exception as e:
            st.error(f"上传失败: {e}")
            
