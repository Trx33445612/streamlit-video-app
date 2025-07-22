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

# 获取当前应用的完整URL（关键改进）
def get_current_app_url():
    try:
        # 如果是Streamlit Cloud部署
        from streamlit.web.server.server import Server
        server = Server.get_current()
        if server:
            return f"https://{server.config.browserServerAddress}"
    except:
        pass
    # 本地运行时默认URL
    return "http://localhost:8501"

# 创建临时目录存储视频
if not os.path.exists("temp_videos"):
    os.makedirs("temp_videos")

# 生成唯一文件名（保持不变）
def generate_unique_filename(original_filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_object = hashlib.md5(original_filename.encode())
    hash_str = hash_object.hexdigest()[:8]
    return f"{timestamp}_{hash_str}_{original_filename}"

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
        
        # 生成完整的可直接打开的URL（关键改进）
        app_url = get_current_app_url().rstrip('/')
        share_url = f"{app_url}/?video={unique_filename}"
        
        st.markdown("### 分享链接（复制后可直接在浏览器打开）")
        st.code(share_url, language="text")
        
        # 复制按钮（提示用户手动复制）
        if st.button("点击复制链接"):
            st.experimental_set_query_params(video=unique_filename)
            st.success(f"已生成链接！请手动复制上方内容到剪贴板")

    # 从URL参数读取视频
    query_params = st.experimental_get_query_params()
    if "video" in query_params:
        video_filename = query_params["video"][0]
        video_path = os.path.join("temp_videos", video_filename)
        
        if os.path.exists(video_path):
            st.markdown(f"### 正在播放: {video_filename.split('_')[-1]}")  # 显示原始文件名
            st.video(video_path)
        else:
            st.error("视频不存在或已过期")

# 清理旧文件（保持不变）
def cleanup_old_videos():
    now = datetime.now()
    for filename in os.listdir("temp_videos"):
        filepath = os.path.join("temp_videos", filename)
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        if (now - file_time).days > 1:
            try:
                os.remove(filepath)
            except:
                pass

cleanup_old_videos()
main()
