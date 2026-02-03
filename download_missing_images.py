#!/usr/bin/env python3
"""
Download missing images from the original leonardoflores.net site
"""
import os
import urllib.request
import urllib.parse
from pathlib import Path

BASE_URL = "https://leonardoflores.net/wp-content/uploads"
LOCAL_BASE = "images/wp-content/uploads"

# All images referenced in HTML files
NEEDED_IMAGES = [
    "2014/01/ELO_LEO.gif",
    "2020/04/Screen-Shot-2020-04-10-at-8.17.57-AM-2048x1080.png",
    "2021/01/spectrums-of-dh-poster.jpg",
    "2021/06/SantosOlvidadosPerfil.png",
    "2021/10/SLSApresentationslide.png",
    "2022/01/digital-colonialism-featured.png",
    "2022/02/DEFCONlogo.png",
    "2022/04/Digital-Divide-Featured.png",
    "2022/07/llamado.png",
    "2022/11/DALL·E-2022-11-25-08.22.05-african-robot-poet.png",
    "2023/01/leo-elo.jpg",
    "2023/01/virtual-conference-flyer.jpg",
    "2023/02/EADLW-Featured-2048x1446.png",
    "2023/05/Its-Complicated.jpg",
    "2023/05/Screenshot-2023-05-16-at-11.13.44-AM.png",
    "2023/08/juracan.png",
    "2023/10/Event-Guest-scaled.jpg",
    "2023/12/Fulbright-letter.png",
    "2024/01/Screenshot-2024-01-05-at-15-52-08-Cyborg-Authors-and-the-Eliza-Effect.png",
    "2024/04/Screenshot-2024-04-05-at-9.48.02 AM.png",
    "2024/05/Screenshot-2024-05-06-at-11.35.38 AM.png",
    "2024/05/Screenshot-2024-05-14-at-7.57.39 AM.png",
    "2024/05/Screenshot-2024-05-29-at-11.02.34 AM.png",
    "2024/06/Cyborg-writer.png",
    "2024/06/Screenshot-2024-06-26-at-3.46.42 PM-2048x1156.png",
    "2024/07/CyberLeo-Teaching.png",
    "2024/09/cyberleosavesacademia.png",
    "2024/12/dharti-featured-image.png",
    "2025/01/young-cyberleo.png",
    "2025/02/Empowering.png",
    "2025/02/Wordhack.jpg",
    "2025/04/DrCyberLeo.png",
    "2025/05/LeoISEA-3.png",
    "2025/05/leo-ia.jpeg",
    "2025/05/peering.png",
    "2025/05/webinar.png",
    "2025/07/leo-at-ELO.png",
    "2025/08/lecturefeatured.png",
    "2025/08/leoiitjodhpur.png",
    "2025/09/Screenshot-2025-09-19-at-12.47.15-PM.png",
    "2026/01/Leo-Toronto.png",
]

def download_image(image_path):
    """Download a single image if it doesn't exist locally"""
    local_path = Path(LOCAL_BASE) / image_path

    if local_path.exists():
        return False  # Already exists

    # Create directory if needed
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # URL encode the path (handle spaces and special chars)
    encoded_path = urllib.parse.quote(image_path)
    url = f"{BASE_URL}/{encoded_path}"

    try:
        print(f"  Downloading: {image_path}")
        urllib.request.urlretrieve(url, local_path)
        return True
    except Exception as e:
        print(f"  ERROR downloading {image_path}: {e}")
        return False

def main():
    print("Downloading missing images...\n")

    downloaded = 0
    errors = 0

    for image_path in NEEDED_IMAGES:
        local_path = Path(LOCAL_BASE) / image_path
        if local_path.exists():
            continue

        if download_image(image_path):
            downloaded += 1
        else:
            errors += 1

    print(f"\n+ Downloaded {downloaded} images")
    if errors:
        print(f"! {errors} errors")

if __name__ == '__main__':
    main()
