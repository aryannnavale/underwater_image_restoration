import os
import cv2
from adaptive_exposure_map import adaptiveExposureMap, applyAdaptiveMap
from GB_dehazing import GBDehaze
from R_correction import correctRChannel

def restore_image(input_image_path):
    windowSize = 9
    result_folder = 'static/output'
    os.makedirs(result_folder, exist_ok=True)

    img = cv2.imread(input_image_path)
    if img is None:
        raise ValueError("Could not read input image")

    i_min = img.min()
    i_max = img.max()
    img = (img - i_min) / (i_max - i_min) * 255

    prefix = os.path.splitext(os.path.basename(input_image_path))[0]

    restored_gb = GBDehaze(img, windowSize, result_folder, prefix)
    cv2.imwrite(os.path.join(result_folder, prefix + '_GBDehazed.jpg'), restored_gb)

    restored = correctRChannel(img, restored_gb)
    cv2.imwrite(os.path.join(result_folder, prefix + '_RCorrection.jpg'), restored)

    S_x = adaptiveExposureMap(img, restored)
    restored = applyAdaptiveMap(restored, S_x)

    output_filename = prefix + '_final.jpg'
    output_path = os.path.join(result_folder, output_filename)
    cv2.imwrite(output_path, restored)

    return output_filename
