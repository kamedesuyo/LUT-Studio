import cv2
from PIL import ImageEnhance, Image
import numpy as np

# トーンカーブ生成
def create_tone_curve(gamma):
    inv_gamma = 1.0 / gamma
    return np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")

# ガンマ補正
def apply_gamma(image, r_gamma, g_gamma, b_gamma, y_gamma):
    image_np = cv2.LUT(np.array(image), create_tone_curve(y_gamma))  # Yチャンネル補正
    r, g, b = [cv2.LUT(image_np[:, :, i], create_tone_curve(g)) for i, g in enumerate([r_gamma, g_gamma, b_gamma])]
    return Image.fromarray(np.stack([r, g, b], axis=-1))

# 彩度調整
def apply_saturation(image, r_saturation, g_saturation, b_saturation, y_saturation):
    return ImageEnhance.Color(image).enhance(r_saturation)

# コントラスト調整
def apply_contrast(image, contrast_r, contrast_g, contrast_b, contrast_y):
    image = ImageEnhance.Contrast(image).enhance(contrast_y)
    r, g, b = image.split()
    r = ImageEnhance.Contrast(r).enhance(contrast_r)
    g = ImageEnhance.Contrast(g).enhance(contrast_g)
    b = ImageEnhance.Contrast(b).enhance(contrast_b)
    return Image.merge('RGB', [r, g, b])
