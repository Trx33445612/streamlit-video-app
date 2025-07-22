import streamlit as st
import os
from datetime import datetime
import hashlib
import pyperclip  # 用于复制到剪贴板

# 配置页面
st.set_page_config(
    page_title="视频共享平台",
    page_icon="🎬",
    layout="wide"
)

# 创建临时目录存储视频
if not os.path.exists("temp_videos"):
    os.makedirs("temp_videos")

# 生成唯一文件名
def generate_unique_filename(original_filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_object = hashlib.md5(original_filename.encode())
    hash_str = hash_object.hexdigest()[:8]
    return f"{timestamp}_{hash_str}_{original_filename}"

# 获取当前部署的URL
def get_app_url():
    try:
        # 从Streamlit配置获取URL
        from streamlit.web.server.websocket_handler import _get_app_url_from_config
        return _get_app_url_from_config()
    except:
        # 本地运行时使用默认URL
        return "http://localhost:8501"

# 主应用
def main():
    st.title("🎬 免费视频共享平台")
    st.markdown("上传视频并获取链接，其他用户可以在任何设备上观看")
    
    # 上传视频
    uploaded_file = st.file_uploader(
        "选择视频文件 (MP4, WebM, OGG)", 
        type=["mp4", "webm", "ogg"],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        # 保存上传的视频
        unique_filename = generate_unique_filename(uploaded_file.name)
        temp_filepath = os.path.join("temp_videos", unique_filename)
        
        with open(temp_filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 显示视频
        st.success("视频上传成功!")
        st.video(temp_filepath)
        
        # 生成正确的分享链接
        app_url = get_app_url().rstrip('/')
        share_url = f"{app_url}/?video={unique_filename}"
        
        st.markdown("### 分享链接")
        st.code(share_url, language="text")
        
        # 复制链接按钮
        if st.button("复制链接到剪贴板"):
            try:
                pyperclip.copy(share_url)
                st.success("链接已复制! 发送这个链接给其他人即可观看视频")
            except:
                st.warning("无法自动复制，请手动复制上面的链接")

    # 检查URL参数是否有视频
    query_params = st.experimental_get_query_params()
    if "video" in query_params:
        video_filename = query_params["video"][0]
        video_path = os.path.join("temp_videos", video_filename)
        
        if os.path.exists(video_path):
            st.markdown(f"### 正在播放: {video_filename}")
            st.video(video_path)
        else:
            st.error("找不到指定的视频文件")

# 定期清理旧视频
def cleanup_old_videos():
    now = datetime.now()
    for filename in os.listdir("temp_videos"):
        filepath = os.path.join("temp_videos", filename)
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        if (now - file_time).days > 1:  # 保留1天内的文件
            try:
                os.remove(filepath)
            except:
                pass

# 运行清理和主应用
cleanup_old_videos()
main()
