import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage
import os
from datetime import timedelta

# 初始化 Firebase（需提前配置）
if not firebase_admin._apps:
    # 从 Streamlit Secrets 获取 Firebase 密钥
    firebase_key = st.secrets["firebase"]
    cred = credentials.Certificate(firebase_key)
    firebase_admin.initialize_app(cred, {
        'storageBucket': "your-project-id.appspot.com"  # 替换为你的 Firebase 存储桶名称
    })

# 页面设置
st.set_page_config(page_title="共享视频平台", page_icon="🎥")
st.title("🎥 跨设备视频共享")
st.markdown("用户A上传视频 → 用户B通过链接播放")

# 文件上传
uploaded_file = st.file_uploader("上传视频 (MP4/AVI/MOV)", type=["mp4", "avi", "mov"])

if uploaded_file:
    # 显示文件信息
    file_name = uploaded_file.name
    file_size = f"{uploaded_file.size / (1024 * 1024):.2f} MB"
    st.success(f"已接收视频: {file_name} ({file_size})")

    # 上传到 Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(f"videos/{file_name}")
    blob.upload_from_string(uploaded_file.read(), content_type=uploaded_file.type)
    
    # 生成可公开访问的链接（有效期 1 年）
    video_url = blob.generate_signed_url(
        expiration=timedelta(days=365),
        method='GET'
    )
    
    # 显示播放器和共享链接
    st.video(video_url)
    st.markdown(f"**共享链接（永久有效）:**\n\n`{video_url}`")
