#YAARX_GUI

gui implementation of yaarx toolkits 
https://github.com/vesselinux/yaarx

## How to run source code
(tested on Ubuntu18.04)

1.install miniconda

`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`

2.run the install script

`bash Miniconda3-latest-Linux-x86_64.sh`

should hit RETURN several times and type 'y' once.

3.append the Miniconda binaries directory to path (for example .bashrc)

4.activate conda

`conda activate`

5.create a new conda environment

`conda create -n yaarx_gui python=3`

6.activate our  environment

`conda activate yaarx_gui`

after that you can find '(yaarx_gui)' in the input area of your terminal

7.install required packages

`pip install pyQt5`
`pip install toml`

8.run the source code

`python main.py`

