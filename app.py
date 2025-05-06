import os
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from gtts import gTTS
from gpt4all import GPT4All
from googletrans import Translator
import tempfile

# Page config
st.set_page_config(page_title="🌐 AI Image Story Generator", layout="wide")

# Load captioning model
@st.cache_resource
def load_blip():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

# Load GPT4All model
@st.cache_resource
def load_gpt4all():
    try:
        return GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf", allow_download=True)
    except Exception as e:
        st.error("⚠ Failed to load GPT4All model. Please check your model path or internet connection.")
        st.stop()

processor, caption_model = load_blip()
gpt4all_model = load_gpt4all()
translator = Translator()

# Languages and Voices
LANGUAGES = {
    "English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr",
    "German": "de", "Arabic": "ar", "Chinese": "zh-cn", "Tamil": "ta", "Bengali": "bn"
}

VOICES = {
    "Male Voice": "en-US-Michael",
    "Female Voice": "en-US-Jenny",
    "Child Voice": "en-US-Kevin"
}

# UI Header
st.title("📖 AI Image-to-Multilingual Story Generator")
st.markdown("Upload an image and let the AI generate a story. Choose the output language and hear it in your selected voice!")

# Upload UI
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
selected_lang = st.selectbox("Choose output language", list(LANGUAGES.keys()))
voice_choice = st.selectbox("Choose Voice", list(VOICES.keys()))

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Generate Story"):
        with st.spinner("Processing..."):

            # Step 1: Image Captioning
            inputs = processor(images=image, return_tensors="pt")
            output = caption_model.generate(**inputs)
            caption = processor.decode(output[0], skip_special_tokens=True)
            st.markdown(f"🖼 *Caption:* {caption}")

            # Step 2: Story Generation
            prompt = f"Write a short, imaginative story based on this image caption: '{caption}'"
            try:
                story_en = gpt4all_model.generate(prompt, max_tokens=300).strip()
            except Exception as e:
                st.error("⚠ GPT4All failed to generate a story. Please check your model setup.")
                st.stop()

            st.markdown("📘 *Story (English):*")
            st.write(story_en)

            # Step 3: Translation
            target_lang_code = LANGUAGES[selected_lang]
            if target_lang_code != "en":
                translated = translator.translate(story_en, dest=target_lang_code).text
                st.markdown(f"🌐 *Translated Story ({selected_lang}):*")
                st.write(translated)
            else:
                translated = story_en

            # Step 4: Text to Speech (TTS)
            tts = gTTS(text=translated, lang=target_lang_code, slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                st.markdown("🎧 *Listen to the Story:*")
                st.audio(tmp.name, format="audio/mp3")

# Custom CSS and Animations
st.markdown("""
<style>
/* Title animation */
.css-1vq2fdd {
    font-size: 30px;
    font-weight: bold;
    color: #4B8B3B;
    animation: slideIn 2s ease-out;
}
/* Zoom-in effect for image */
.stImage {
    animation: zoomIn 1.5s ease-in-out;
}
/* Button styling */
.stButton button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 18px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}
.stButton button:hover {
    background-color: #45a049;
    transform: scale(1.1);
}
/* Fade-in content */
.css-1v1nzwk {
    animation: fadeIn 1.5s ease-in-out;
    opacity: 0;
}
/* Audio button styling */
.stAudio button {
    background-color: #ff6f61;
    color: white;
    padding: 10px 15px;
    border-radius: 8px;
    font-size: 16px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}
.stAudio button:hover {
    background-color: #ff3d39;
    transform: scale(1.05);
}
/* Keyframes */
@keyframes slideIn {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(0); }
}
@keyframes zoomIn {
    0% { transform: scale(0.8); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# JavaScript fade-in
st.markdown("""
<script>
setTimeout(function() {
    var element = document.querySelector('.css-1v1nzwk');
    if(element) {
        element.style.opacity = '1';
        element.style.transition = 'opacity 1s ease-in-out';
    }
}, 2000);
</script>
""", unsafe_allow_html=True)