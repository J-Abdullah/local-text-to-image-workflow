# 🎨 Local AI Image Generation

Generate images locally using AI — no cloud APIs, no subscriptions, no data leaving your machine.

This repo contains **two approaches** depending on your setup:

---

## 📁 What's In This Repo

| File | What it is |
|---|---|
| `Local image gen (flux2-4b).json` | ComfyUI workflow — FLUX.2 Klein 4B image generation |
| `Text-to-image-with-email(n8n).json` | n8n automation workflow — chat → AI image → Gmail |
| `local-image-gen-workflow-guide.pdf` | Full setup guide with screenshots and troubleshooting |
| `python code/` | Standalone Python script — no ComfyUI or n8n needed |

---

## 🚀 Approach 1 — Python Script (Simplest)

No ComfyUI or n8n required. Just Python and a GPU.

Uses **Tiny-SD** (Segmind), a lightweight Stable Diffusion model that downloads automatically on first run.

### Requirements
- Python 3.10+
- NVIDIA GPU (CPU works but is slow)
- ~2GB disk space for model cache

### Install & Run
```bash
pip install torch torchvision diffusers transformers accelerate

python "python code/generate.py"
```

### How it works
- Downloads the model into a local `./hf_cache` folder on first run
- All cache stays in the project directory — nothing written to system folders
- Output saved as `generated_image.png` in the same folder
- Edit the `prompt` variable in the script to change what gets generated

> **Note:** This uses Tiny-SD for speed and low VRAM usage. For higher quality, swap `segmind/tiny-sd` for `runwayml/stable-diffusion-v1-5` or similar.

---

## ⚙️ Approach 2 — ComfyUI + n8n Automation (Full Workflow)

The full pipeline: type a message → Qwen enhances the prompt → FLUX.2 Klein generates the image → Gmail delivers it.

### Stack
- **ComfyUI** — runs FLUX.2 Klein 4B locally on your GPU
- **Ollama + Qwen 3** — local LLM that enhances your prompt before image generation
- **n8n** — automation that connects everything and sends the result via email

### Requirements
- Windows (Ollama image generation requires Windows/macOS)
- NVIDIA GPU with 8GB+ VRAM
- ComfyUI installed and running
- Ollama installed with `qwen3:9b` pulled
- n8n (Docker recommended)

### Model Files Needed in ComfyUI
| File | Folder |
|---|---|
| `flux-2-klein-4b-fp8.safetensors` | `models/unet/` |
| `qwen_3_4b.safetensors` | `models/clip/` |
| `flux2-vae.safetensors` | `models/vae/` |

### Quick Start

**1. Start ComfyUI**
```bash
run_nvidia_gpu.bat
```

**2. Start Ollama**
```bash
ollama serve
```

**3. Import the workflows**
- In ComfyUI → drag and drop `Local image gen (flux2-4b).json`
- In n8n → Import → paste `Text-to-image-with-email(n8n).json`

**4. Configure Gmail credentials in n8n, then activate the workflow**

**5. Open the n8n chat and type your image idea**

---

## 🐳 Running n8n in Docker?

Use `host.docker.internal` instead of `127.0.0.1` in all n8n HTTP Request nodes:

```
# Ollama
http://host.docker.internal:11434/api/chat

# ComfyUI
http://host.docker.internal:8188/prompt
http://host.docker.internal:8188/history/{id}
http://host.docker.internal:8188/view
```

---

## 📖 Full Guide

See **`local-image-gen-workflow-guide.pdf`** for:
- ComfyUI node-by-node breakdown with screenshots
- n8n workflow configuration for all 9 nodes
- Docker networking tips
- Troubleshooting every common error

---

## ⚠️ Known Limitations

- Ollama image generation (FLUX.2 Klein) only works on **macOS and Windows**
- Minimum **8GB VRAM** recommended for FLUX.2 Klein FP8
- ComfyUI must be **manually started** before running the n8n workflow — n8n does not start it automatically

---

## 🛠 Tested On

- Windows 11
- n8n running in Docker
- ComfyUI portable (NVIDIA)
- FLUX.2 Klein 4B FP8
- Ollama Qwen 3 9B
- May 2026
