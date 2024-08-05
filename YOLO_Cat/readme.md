## 1 Environment requirement
### 1.1 Ultralytics requirement

numpy>=1.23.0,<2.0.0，

matplotlib>=3.3.0，

opencv-python>=4.6.0,

pillow>=7.1.2,

pyyaml>=5.3.1,

requests>=2.23.0,

scipy>=1.4.1,

torch>=1.8.0,

torchvision>=0.9.0,

tqdm>=4.64.0,

psutil,

py-cpuinfo, 
pandas>=1.1.4,

seaborn>=0.11.0

### 1.2 ConvNext requirement

transformers

**You can install on demand in an existing pytorch environment, or use pip install -r requirement.txt to install all dependencies in a new environment**

## 2. Run Demo program

Replace --img_path with the path of the image to be tested in demo.sh

Run sh demo.sh

The xxx_annotated.jpg image will be generated in the original image path, which is the labeled image at the end of the pipeline run.

The xxx_detection.jpg image will be generated in the original image path, which is the image labeled by YOLO.

In the directory of demo.sh, a series of crop images will be generated.

**NOTE: The first time you use it, you need to wait for Ultralytics to download the fonts for drawing, which may cause some lag**