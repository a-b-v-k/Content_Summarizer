import io
import os
os.system("pip install streamlit --upgrade")
from process_media import MediaProcessor
import streamlit as st
from summarizer import BARTSummarizer
from  Utils import fetch_article_text, get_text_from_youtube_url

st.markdown(
"""
<style>
section[data-testid="stSidebar"]  div[role="radiogroup"] label {
    padding: 0px 0px 20px 20px;
}
section[data-testid="stSidebar"] h2 {
    margin: 10px;
}
section.main div[role="radiogroup"] label {
    padding: 10px 10px 10px 0px;
}
</style>
""",
unsafe_allow_html=True,
)

with st.sidebar:
    st.header("CHOOSE INPUT TYPE")
    input_type = st.radio("", ["Text", "Media"], label_visibility = "hidden")


text_to_summarize = None

if input_type == "Text":

    st.header("Summarize from text or URL")

    text_type = st.radio("", ["Raw Text", "URL", "Document"], key="text_type", horizontal=True, label_visibility = "hidden")

    if text_type == "Raw Text":
        text = st.text_area("Enter raw text here", height=240, max_chars=10000, placeholder="Enter a paragraph to summarize")
        if text:
            text_to_summarize = text
        
    elif text_type == "URL":
        url = st.text_input("Enter URL here", placeholder="Enter URL to an article, blog post, etc.")
        if url:
            article_text = fetch_article_text(url)
            if article_text:
                st.markdown("#### Text from url:")
                st.write(article_text)
                text_to_summarize = article_text
    else:
        ## TODO: Add file upload option
        pass

elif input_type == "Media":

    st.header("Summarize from file or YouTube URL")

    media_type = st.radio("", ["Audio file", "Video file", "Youtube video link"], key="media_type", horizontal=True, label_visibility = "hidden")

    if media_type == "Audio file":
        audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"], label_visibility="visible")
        if audio_file is not None:
            with st.spinner("Fetching text from audio..."):
                # print(audio_file.read())
                wav_bytes = None
                media_processor = MediaProcessor()
                if audio_file.type == "audio/mpeg":
                    wav_bytes = media_processor.get_wav_from_audio(audio_file.read())
                else:
                    wav_bytes = audio_file.read()
                text = media_processor.process_audio(wav_bytes)
                st.markdown("#### Text from audio:")
                st.write(text)
    elif media_type == "Video file":
        video_file = st.file_uploader("Upload a video file", type=["mp4"], label_visibility="visible")
        if video_file is not None:
            with st.spinner("Fetching text from video..."):
                media_processor = MediaProcessor()
                text = media_processor.process_video(video_file.read())
                st.markdown("#### Text from video:")
                st.write(text)
    else:
        youtube_url = st.text_input("Enter YouTube URL here", placeholder="Enter URL to an YouTube video", label_visibility="visible")
        if youtube_url:
            with st.spinner("Fetching text from video..."):
                try:
                    text_to_summarize = get_text_from_youtube_url(youtube_url)
                    st.markdown("#### Text from video:")
                    st.markdown('<div style="height: 300px; overflow: auto; margin-bottom: 20px;">' + text_to_summarize + '</div>', unsafe_allow_html=True)
                except:
                    st.error("Unable to fetch text from video. Please try a different video.")
                    text_to_summarize = None

if text_to_summarize is not None:
    overall_summary = st.button("Overall summary")
    auto_chapters_summary = st.button("Auto Chapters summary")
    if overall_summary:
        with st.spinner("Summarizing..."):
            # time.sleep(2)
            # st.write(text_to_summarize)
            summarizer = BARTSummarizer()
            summary = summarizer.chunk_summarize(text_to_summarize)
            st.markdown("#### Summary:")
            st.write(summary)
    elif auto_chapters_summary:
        with st.spinner("Summarizing..."):
            # time.sleep(2)
            # st.write(text_to_summarize)
            summarizer = BARTSummarizer()
            summary = summarizer.auto_chapters_summarize(text_to_summarize)
            st.markdown("#### Summary:")
            st.write(summary)