import os
import torch
from diffusers import StableDiffusionPipeline

# =========================================================
# Force ALL HuggingFace caches into current directory
# =========================================================
local_cache = os.path.abspath("./hf_cache")

os.environ["HF_HOME"] = local_cache
os.environ["TRANSFORMERS_CACHE"] = local_cache
os.environ["HUGGINGFACE_HUB_CACHE"] = local_cache
os.environ["HF_DATASETS_CACHE"] = local_cache
os.environ["TORCH_HOME"] = local_cache

print(f"Using local cache folder: {local_cache}")

print("Loading model... (downloads only first time)")

# Load lightweight Tiny-SD model
pipe = StableDiffusionPipeline.from_pretrained(
    "segmind/tiny-sd",
    torch_dtype=torch.float16
)

# Use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)

# Reduce VRAM usage
if device == "cuda":
    pipe.enable_attention_slicing()

# Prompt
#prompt = "A 2D rubber hose style cartoon biker riding a bicycle, wearing a helmet and biker gear"

print("Generating image...")

# Generate image
image = pipe(
    prompt="2D rubber hose cartoon style, vintage animation, biker riding a bicycle, wearing motorcycle helmet and leather biker jacket, dynamic pose, clean lines, colorful, retro 1930s cartoon, high quality illustration",
    
    negative_prompt="blurry, low quality, distorted face, extra limbs, bad anatomy, cropped, watermark, text, deformed hands",
    
    num_inference_steps=25,
    guidance_scale=7.5
).images[0]

# Save image in current directory
output_path = "./generated_image2.png"
image.save(output_path)

print(f"Image saved successfully at: {output_path}")