import streamlit as st
import tempfile
import os

# 设置页面标题、图标和布局
st.set_page_config(
    page_title="视频上传与播放器",
    page_icon="🎬",
    layout="wide"
)

# 标题和说明
st.title("🎥 在线视频播放器")
st.markdown("""
上传你的视频文件（支持 MP4/MOV/AVI），即可直接在网页播放  
⚠️ **注意**：视频仅在当前会话有效，刷新页面会丢失
""")

# 自定义样式：隐藏 Streamlit 默认菜单和页脚
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 文件上传区域
uploaded_file = st.file_uploader(
    label="选择视频文件",
    type=["mp4", "mov", "avi", "mkv"],
    accept_multiple_files=False,
    help="最大支持 200MB 的文件"
)

# 如果上传了文件
if uploaded_file is not None:
    # 显示文件信息
    file_details = {
        "文件名": uploaded_file.name,
        "文件类型": uploaded_file.type,
        "文件大小": f"{uploaded_file.size / (1024 * 1024): .2f} MB"
    }
    st.json(file_details)

    # 临时保存文件（仅用于播放）
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name

    # 显示成功消息和播放器
    st.success("视频上传成功！")
    st.subheader("播放器")

    # 使用两列布局：左侧播放器，右侧控制选项
    col1, col2 = st.columns([3, 1])

    with col1:
        # 播放视频（使用HTML5 video标签增强兼容性）
        video_bytes = uploaded_file.read()
        st.video(video_bytes)

    with col2:
        st.markdown("**控制选项**")
        autoplay = st.checkbox("自动播放", value=False)
        muted = st.checkbox("静音", value=False)

        # 显示下载按钮（可选）
        st.download_button(
            label="下载视频",
            data=video_bytes,
            file_name=uploaded_file.name,
            mime=uploaded_file.type
        )

    # 清理临时文件
    os.unlink(tmp_path)
