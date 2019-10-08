# Mask image generator for VoTT

This directory is for generating mask images which can be used for training semantic / instance segmentation models from [VoTT (Visual Object Tagging Tool)](https://github.com/microsoft/VoTT) output label data.

| Original image                                         | Mask image                               |
| ------------------------------------------------------ | ---------------------------------------- |
| ![mailbox](output_processors/docs/images/mailbox1.jpg) | ![mailbox-mask](tests/data/mailbox1.png) |
| ![pencil](output_processors/docs/images/pencil1.jpg)   | ![pencil-mask](tests/data/pencil1.png)   |

## Prerequisites

### Prepare label data

Use [VoTT (Visual Object Tagging Tool)](https://github.com/microsoft/VoTT)'s **Draw Polygon** mode to label image.

Set **VoTT JSON** in **Provider** in **Export Settings** when you export labeled data and generate JSON file as output.

## Usage

### With container

1. Build container

```sh
sudo docker build . -t vott-output-processors
```

2. Create directory to mount to container

```sh
mkdir YOUR_DIRECOTRY_TO_MOUNT
```

Move your JSON label data under the directory you created above.

3. Run container and run script inside

```sh
sudo docker run -it --mount type=bind,src=/YOUR_DIRECOTRY_TO_MOUNT,dst=/YOUR_DIRECOTRY_TO_MOUNT vott-output-processors bash
python output_processors/vott2mask.py ../YOUR_DIRECOTRY_TO_MOUNT/YOUR_LABEL.json ../YOUR_DIRECOTRY_TO_MOUNT/DIRECOTRY_TO_STORE_MASK
```


### Without container

This repository is only tested with Python 3.7.4

```sh
pip install -r requirements.txt
python vott2mask.py YOUR_LABEL_PATH DIRECOTRY_TO_STORE_MASK
```

## How to run tests

### With container

```sh
sudo docker run -it vott-output-processors bash
python -m pytest --cov output_processors tests
```

### Without container

```sh
pip install -r requirements.txt
python -m pytest --cov output_processors tests
```
