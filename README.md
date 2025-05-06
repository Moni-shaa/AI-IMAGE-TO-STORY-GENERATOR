# AI Image-to-Story Generator

## Overview
The AI Image-to-Story Generator is an interactive, multilingual storytelling application that transforms images into imaginative narratives with voice output. It combines cutting-edge models for image captioning (BLIP), story generation (GPT4All Mistral), and multilingual translation (Google Translate API), delivering a personalized experience suitable for education, accessibility, and creative engagement.

## Features
- 🖼️ Image captioning with BLIP (HuggingFace Transformers)
- ✍️ Story generation using GPT4All (Mistral model)
- 🌐 Multilingual support via Google Translate API
- 🔊 Text-to-Speech narration with gTTS, including gender/age-based voice selection
- 🎛️ Interactive UI built with Streamlit
- 🐳 Dockerized for easy deployment across environments
- 🎨 Animated frontend with real-time image preview and audio controls

## Use Cases
- Language learning and early literacy
- Accessibility for visually impaired users
- Creative story generation for kids and educators
- Integration with digital libraries or e-learning tools

## Installation

```bash
git clone https://github.com/your-username/ai-image-story-generator.git
cd ai-image-story-generator
docker build -t image-story-app .
docker run -p 8501:8501 image-story-app

#Architecture
Frontend: Streamlit (UI)

Backend:

BLIP (image captioning)

GPT4All Mistral (story generation)

Google Translate API (translation)

gTTS (audio narration)

#License
This project is licensed under the MIT License. See LICENSE for details.
