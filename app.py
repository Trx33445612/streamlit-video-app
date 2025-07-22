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

# 创建临时目录存储视频
if not os.path.exists("temp_videos"):
    os.makedirs("temp_videos")

# 生成唯一文件名
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
        
        # 生成分享链接（使用当前URL）
        current_url = st.experimental_get_query_params().get('_g', [''])[0]
        share_url = f"{current_url}/?video={unique_filename}" if current_url else f"?video={unique_filename}"
        
        st.markdown("### 分享链接")
        st.code(share_url, language="text")
        
        # 复制链接按钮（不使用pyperclip）
        if st.button("复制链接到剪贴板"):
            st.experimental_set_query_params(video=unique_filename)
            st.success("请手动复制上方链接！分享给其他人即可观看视频")

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
