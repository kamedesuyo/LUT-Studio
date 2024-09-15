from PIL import Image

resize_scale = [(1920,1080),[3840,2160]]

# イメージのリサイズ
def resize_image(image,WINDOW_SIZE:tuple) -> Image.Image:
    image_size = image.size
    window_size = WINDOW_SIZE
    
    for size in resize_scale:
        # w,hの規定サイズチェック
        w_check = image_size[0] == size[0]
        h_check = image_size[1] == size[1]
        
        # 規定サイズならそのまま出力
        if w_check and h_check:
            return image.resize(window_size)
        # widthが規定でheightが規定でないならheightを調整する
        elif w_check and not h_check:
            result = Image.new(image.mode,size,(0,0,0)) # 16:9の背景を作成
            result.paste(image, (0, ((size[1] - image_size[1])//2))) # 元画像貼り付け
            return result.resize(window_size) # レターボックス形式で出力される
    # それ以外は引き延ばし
    return image.resize(window_size)