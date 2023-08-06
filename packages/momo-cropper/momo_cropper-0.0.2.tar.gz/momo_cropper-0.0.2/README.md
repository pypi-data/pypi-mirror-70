## 功能说明

1. 根据用户自定义绘制的边框颜色，自动识别并切割出组件图像

## 快速启动

- 环境配置
  - homebrew
    - `/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"`
  - Python >= 3.6
    > 取消 brew 的自动更新 `export HOMEBREW_NO_AUTO_UPDATE=true`
    - `brew install python3`

- 安装依赖
  - 所需要的库见 requirements.txt, 批量安装 `pip install -r requirements.txt`.
  - 单个安装如下：
    ```
      pip install opencv-python==4.2.0.34
      pip install numpy==1.18.4
      pip install pillow==7.1.2
      pip install setuptools==47.1.1
    ```
  - 如使用国内源安装，则在命令行最后添加参数 `-i https://pypi.tuna.tsinghua.edu.cn/simple`
- 启动
  - 组件边界识别和图像切割
    - `python component_cropping_via_given_borders.py arg1 arg2 `
      - arg1 为本机截图的边框颜色图片
      - arg2 为待识别的视觉稿

- 命令行
  - 执行命令`python setup.py install`，将程序安装到系统
  - 使用命令`cropper`对安装好的程序进行调用，例如`cropper borders/border1.png images/page1.png`

## 相关脚本说明

1. `component_cropping_via_given_borders.py`, 根据指定边框文件模板，提取出边框颜色，然后进行切片
1. `component_cropping_via_given_colors.py`, 根据指定的边框颜色，切割给定图片。
1. `component_matching.py`, 比较图片相似度

## 使用说明

1. 以给定边框模板为例，首先选择白色背景，绘制各类边框颜色，然后保存到`borders`目录;

1. 根据上一步给定的模板边框，通过`tools.img_utils.get_border_colors_from_template(template_file)`函数提取出所有颜色;

1. 提取到所有颜色后，调用`component_cropping_via_given_borders.crop(file, color, color_idx)`切割图片, 切割后的图片保存在`cropped`目录

## 跨语言调用

- **JS调用Python** 

    参照cross-lang/js_caller.js，执行命令`node js_caller.js`即可查看效果。 `js_call.js`中包含了同步与异步两种调用方式，开发者可根据需求进行调整。
