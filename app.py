import streamlit as st
from github import Github  # 需安装 PyGithub

# GitHub 配置（替换为你的信息）
GITHUB_TOKEN = st.secrets["github"]["token"]
REPO_NAME = "你的用户名/你的仓库名"
BRANCH = "main"

# 初始化 GitHub 客户端
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

st.title("🎥 视频共享平台")
st.markdown("上传视频 → 自动保存到GitHub → 内嵌播放")

# 文件上传
uploaded_file = st.file_uploader("选择MP4文件（<25MB）", type=["mp4"])

if uploaded_file:
    file_name = uploaded_file.name
    file_content = uploaded_file.read()

    try:
        # 上传到 GitHub
        repo.create_file(
            path=f"videos/{file_name}",
            message=f"Add video: {file_name}",
            content=file_content,
            branch=BRANCH
        )
        
        # 生成 Raw URL
        raw_url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/videos/{file_name}"
        st.success("上传成功！")
        
        # ---- 关键播放代码 ----
        st.subheader("播放器")
        video_html = f"""
        <div style="border: 2px solid #eee; border-radius: 5px; padding: 10px;">
          <video width="100%" controls autoplay muted>
            <source src="{raw_url}" type="video/mp4">
          </video>
        </div>
        """
        st.components.v1.html(video_html, height=500)
        # ---------------------
        
        st.markdown(f"**共享链接：**\n\n`{raw_url}`")
        
    except Exception as e:
        st.error(f"上传失败: {e}")
        
