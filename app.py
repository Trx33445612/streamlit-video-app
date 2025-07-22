import streamlit as st
import os
from datetime import datetime
import hashlib

# 配置页面
st.set_page_config(
    page_title="视频共享平台",
    page_icon="🎬",
    layout="wide"
)

# 手动设置云端域名（部署后必须修改！）
CLOUD_URL = "https://app-video-app-eaqca3urpvkh8xbdfgappub.streamlit.app"  # ⚠️请替换为你的实际部署地址

# 生成唯一文件名
def generate_unique_filename(original_filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_object = hashlib.md5(original_filename.encode())
    hash_str = hash_object.hexdigest()[:8]
    return f"{timestamp}_{hash_str}_{original_filename}"

def main():
    st.title("🎬 免费视频共享平台")
    st.markdown("上传视频并获取链接，其他用户可以在任何设备上观看")

    # 警告本地运行提示
    if "streamlit.app" not in CLOUD_URL:
        st.warning("⚠️ 当前为本地测试模式，生成的链接无法跨设备访问。部署后请修改代码中的 `CLOUD_URL`")

    # 上传视频
    uploaded_file = st.file_uploader(
        "选择视频文件 (MP4, WebM, OGG)", 
        type=["mp4", "webm", "ogg"],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        # 保存文件
        unique_filename = generate_unique_filename(uploaded_file.name)
        temp_filepath = os.path.join("temp_videos", unique_filename)
        
        with open(temp_filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("视频上传成功!")
        st.video(temp_filepath)
        
        # 生成云端链接（始终使用预设的CLOUD_URL）
        share_url = f"{CLOUD_URL}/?video={unique_filename}"
        
        st.markdown("### 🌐 跨设备分享链接")
        st.code(share_url, language="text")
        
        # 简化复制操作
        st.markdown(f"""
        <a href="{share_url}" target="_blank"><button style="color: white; background-color: #FF4B4B; border: none; padding: 0.5rem 1rem; border-radius: 0.5rem;">点击测试链接</button></a>
        <span style="margin-left: 1rem;">或手动复制上方链接</span>
        """, unsafe_allow_html=True)

    # 视频播放逻辑
    query_params = st.experimental_get_query_params()
    if "video" in query_params:
        video_path = os.path.join("temp_videos", query_params["video"][0])
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.error("视频已过期或不存在")

# 初始化目录和清理
if not os.path.exists("temp_videos"):
    os.makedirs("temp_videos")
main()
        
