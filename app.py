import streamlit as st
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy import VideoFileClip
import os
import re
import streamlit.components.v1 as components
import glob

# --- VERIFIKASI GOOGLE ---
st.write('<meta name="google-site-verification" content="mSNlY9Ov_9hLMrsA1nTq-3O7So0X-aoEUqsRbBRYRfE" />', unsafe_allow_html=True)

# Konfigurasi Halaman
st.set_page_config(page_title="ClipViral AI Pro", page_icon="✂️")

# --- FUNGSI PEMBERSIH ---
def hapus_sampah_video():
    for f in glob.glob("*.mp4"):
        try:
            os.remove(f)
        except:
            pass

# --- JUDUL WEB ---
st.title("✂️ ClipViral AI Pro")
st.subheader("Download & Auto-Clip YouTube")

# --- IKLAN NATIVE ---
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
        format_pilihan = st.selectbox("Pilih Kualitas:", ["720p (Paling Stabil)", "480p", "1080p"])
        res = "720"
        if "480p" in format_pilihan: res = "480"
        if "1080p" in format_pilihan: res = "1080"

        if st.button(f"🚀 Proses Video {res}p"):
            hapus_sampah_video()
            try:
                with st.spinner("Menghubungkan ke jalur alternatif YouTube..."):
                    # OPSI LIGHTWEIGHT & DNS BYPASS
                    ydl_opts = {
                        'format': f'best[height<={res}][ext=mp4]', 
                        'outtmpl': 'full_video.mp4',
                        'overwrites': True,
                        'nocheckcertificate': True,
                        'geo_bypass': True,
                        'socket_timeout': 60,
                        'quiet': True,
                        'no_warnings': True,
                        'check_formats': False, # Melewati pengecekan format untuk hindari error DNS
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

                    # --- PROSES KLIP ---
                    st.write("### ✂️ Hasil Klip Viral (9:16):")
                    cols = st.columns(3)
                    video_full = VideoFileClip("full_video.mp4")
                    
                    momen = [10, 60, 120]
                    try:
                        ts = YouTubeTranscriptApi.get_transcript(v_id, languages=['id', 'en'])
                        momen = [t['start'] for t in ts if any(k in t['text'].lower() for k in ['wah','keren','tips','gila','parah'])][:3]
                        if len(momen) < 3: momen = [15, 70, 130]
                    except: pass

                    for i, start in enumerate(momen):
                        dur = video_full.duration
                        if start >= dur: start = 0
                        end_time = min(start + 55, dur)
                        
                        clip = video_full.subclip(start, end_time)
                        w, h = clip.size
                        target_w = h * 9 / 16
                        final = clip.cropped(x1=(w-target_w)/2, y1=0, width=target_w, height=h)
                        
                        out_name = f"clip_{i+1}.mp4"
                        final.write_videofile(out_name, codec="libx264", audio_codec="aac", fps=24, logger=None)
                        
                        with cols[i]:
                            st.video(out_name)
                            with open(out_name, "rb") as f:
                                st.download_button(f"📥 Download {i+1}", f, file_name=f"clip_{i+1}.mp4", key=f"dl_{i}")

                    video_full.close()

                    # --- DOWNLOAD FULL ---
                    st.markdown("---")
                    with open("full_video.mp4", "rb") as f_full:
                        st.download_button(f"📥 Download Full Video {res}p", f_full, file_name=f"full_{res}p.mp4", use_container_width=True)
                
                st.success("Selesai!")

            except Exception as e:
                st.error(f"Koneksi Hugging Face ke YouTube terganggu: {e}")
                st.warning("SOLUSI: Masuk ke tab SETTINGS lalu klik FACTORY REBOOT di bagian bawah halaman.")
                hapus_sampah_video()
    else:
        st.error("Link tidak valid.")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 ClipViral AI - Emergency Patch")

# --- IKLAN SOCIAL BAR ---
components.html("""<script src="https://pl28773816.effectivegatecpm.com/72/34/5f/72345f53f09912e7e221655eb41baf9b.js"></script>""", height=0)