import argparse
import json
from pathlib import Path
from typing import Any, Dict, Tuple, List

import numpy as np
from PIL import Image, ImageColor, ImageDraw
from tqdm import tqdm


def vott_to_masks(annotation_file: Path, mask_dir: Path):
    """Converts VoTT's generic JSON schema output to mask images

    Args:
        annotation_file (Path): Path to VoTT JSON annotation file
        mask_dir (Path): Path to save mask files
    """
    mask_dir.mkdir(exist_ok=True)
    with annotation_file.open('r') as annotation_json:
        annotations = json.load(annotation_json)

        tags = annotations['tags']
        # Starting from 1 because 0 (black) is reserved for background
        mapping = {tag['name']: i + 1 for i, tag in enumerate(tags)}
        # Add black for the background in the front
        colors = [(0, 0, 0)] + [
            ImageColor.getrgb(color_str)
            for color_str in [tag['color'] for tag in tags]
        ]
        image_annotations = annotations['assets']

        for image_annotation in tqdm(image_annotations.values()):

            img_shape = (int(image_annotation['asset']['size']['width']),
                         int(image_annotation['asset']['size']['height']))
            img_name = image_annotation['asset']['name']
            # We want to save images in P (palettised) mode which PNG supports
            mask_path = mask_dir / img_name.replace('jpg', 'png')

            mask_img = label_to_mask(img_shape=img_shape,
                                     regions=image_annotation['regions'],
                                     name_to_index=mapping,
                                     colors=colors)
            mask_img.save(mask_path)


def label_to_mask(img_shape: Tuple[int, int], regions: List[Dict[str, Any]],
                  name_to_index: Dict[str, int],
                  colors: List[Tuple[int, int, int]]) -> Image:
    """Generate image mask with its label from image shape

    Args:
        img_shape (Tuple[int, int]): Image shape
        regions (List[Dict[str, Any]]): Annotation meta data for mask by VoTT
        name_to_index (Dict[str, int]): mapping from class name to index
        colors (List[Tuple[int, int, int]]): List of color code for classes

    Returns:
        Image: Mask image
    """
    mask_img = Image.new(mode='P', size=img_shape, color=0)
    mask_img.putpalette(np.array(colors).astype(np.uint8))

    draw = ImageDraw.Draw(mask_img)
    for region in regions:
        points = region['points']
        coordinates = [(point['x'], point['y']) for point in points]
        label_name = str(region['tags'][0])
        region_type = region['type']
        label_id = name_to_index[label_name]
        draw_mask(draw, label_id, coordinates, region_type)
    return mask_img


def draw_mask(draw: ImageDraw, label_id: int,
              coordinates: List[Tuple[float, float]], region_type: str):
    """Draw mask on a provided image

    Args:
        draw (ImageDraw): Image to draw in
        label_id (int): class id which will be used for color representation
        coordinates (List[Tuple[float, float]]): List of point coordinates
         which form polygon
        region_type (str): Anotated region's shape type
    """
    if region_type == 'POLYGON':
        if (len(coordinates) > 2):
            draw.polygon(xy=coordinates, outline=label_id, fill=label_id)
        else:
            ValueError('Polygon must have points more than 2')
    else:
        ValueError(f'{region_type} is not supported')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'annotation_file',
        type=Path,
        help='VoTT generated annotation file path to produce mask images')
    parser.add_argument('mask_dir',
                        type=Path,
                        help='Directory to save mask-convered images')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    vott_to_masks(args.annotation_file, args.mask_dir)
    print('Mask images generation completed')
