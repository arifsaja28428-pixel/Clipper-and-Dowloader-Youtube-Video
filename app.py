import streamlit as st
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy import VideoFileClip
import os
import re
import streamlit.components.v1 as components
import glob

# --- VERIFIKASI GOOGLE ---
# Kode ini akan langsung terdeteksi oleh Google Search Console di Streamlit Cloud
st.write('<meta name="google-site-verification" content="mSNlY9Ov_9hLMrsA1nTq-3O7So0X-aoEUqsRbBRYRfE" />', unsafe_allow_html=True)

# Konfigurasi Halaman
st.set_page_config(page_title="ClipViral AI - Pro Downloader", page_icon="✂️")

# --- FUNGSI PEMBERSIH ---
def hapus_sampah_video():
    for f in glob.glob("*.mp4"):
        try:
            os.remove(f)
        except:
            pass

# --- JUDUL WEB ---
st.title("✂️ ClipViral AI Pro")
st.subheader("YouTube Downloader & Auto-Shorts")

# --- IKLAN NATIVE (ADSTERRA) ---
components.html("""
    <div style="text-align:center;">
        <script async="async" data-cfasync="false" src="https://pl28773812.effectivegatecpm.com/f3e16d1e59129834e7369b3d15378b28/invoke.js"></script>
        <div id="container-f3e16d1e59129834e7369b3d15378b28"></div>
    </div>
""", height=250)

# --- AREA INPUT ---
url = st.text_input("Tempel Link YouTube:", placeholder="https://youtube.com/watch?v=...")

if url:
    video_id_match = re.search(r"(?:v=|\/|be\/|shorts\/)([a-zA-Z0-9_-]{11})", url)
    if video_id_match:
        v_id = video_id_match.group(1)
        
        # PILIHAN KUALITAS
        format_pilihan = st.selectbox("Pilih Kualitas Video:", ["720p (Stabil)", "480p (Cepat)", "1080p (HD)"])
        res = "720"
        if "480p" in format_pilihan: res = "480"
        if "1080p" in format_pilihan: res = "1080"

        if st.button(f"🚀 Proses & Download {res}p"):
            hapus_sampah_video()
            try:
                with st.spinner("Sedang mengambil data video dari YouTube..."):
                    # OPSI ANTI-BLOCK & DNS FIX
                    ydl_opts = {
                        'format': f'best[height<={res}][ext=mp4]',
                        'outtmpl': 'full_video.mp4',
                        'overwrites': True,
                        'nocheckcertificate': True,
                        'geo_bypass': True,
                        'quiet': True,
                        'no_warnings': True,
                        # Menyamar sebagai Browser agar tidak Error 403
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

                    # --- PROSES KLIP OTOMATIS (9:16) ---
                    st.write("### ✂️ Klip Viral Otomatis:")
                    cols = st.columns(3)
                    video_full = VideoFileClip("full_video.mp4")
                    
                    # Cari Momen Penting
                    momen = [15, 75, 140]
                    try:
                        ts = YouTubeTranscriptApi.get_transcript(v_id, languages=['id', 'en'])
                        momen = [t['start'] for t in ts if any(k in t['text'].lower() for k in ['wah','keren','gila','rahasia','tips'])][:3]
                        if len(momen) < 3: momen = [10, 60, 120]
                    except: pass

                    for i, start in enumerate(momen):
                        dur = video_full.duration
                        if start >= dur: start = 0
                        end_time = min(start + 55, dur)
                        
                        clip = video_full.subclip(start, end_time)
                        
                        # Resize & Crop ke 9:16
                        w, h = clip.size
                        target_w = h * 9 / 16
                        final = clip.cropped(x1=(w-target_w)/2, y1=0, width=target_w, height=h)
                        
                        out_name = f"clip_{i+1}.mp4"
                        final.write_videofile(out_name, codec="libx264", audio_codec="aac", fps=24, logger=None)
                        
                        with cols[i]:
                            st.video(out_name)
                            with open(out_name, "rb") as f:
                                st.download_button(f"📥 Download {i+1}", f, file_name=f"shorts_{i+1}.mp4", key=f"dl_{i}")

                    video_full.close()

                    # --- DOWNLOAD FULL VIDEO ---
                    st.markdown("---")
                    st.write(f"### 📺 Video Original {res}p:")
                    with open("full_video.mp4", "rb") as f_full:
                        st.download_button(f"📥 Download Video Utuh", f_full, file_name=f"original_{res}p.mp4", use_container_width=True)

                st.success("Berhasil diproses!")

            except Exception as e:
                st.error(f"Terjadi Kendala: {e}")
                hapus_sampah_video()
    else:
        st.error("Link YouTube tidak valid.")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 ClipViral AI - Cloud Hosting Version")

# --- IKLAN SOCIAL BAR (ADSTERRA) ---
components.html("""
    <script src="https://pl28773816.effectivegatecpm.com/72/34/5f/72345f53f09912e7e221655eb41baf9b.js"></script>
""", height=0)
