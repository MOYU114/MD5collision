# 密码分析与实践

## MD5碰撞分析的实现与应用

### 项目描述

在本次实验中，通过使用快速MD5碰撞攻击技术，成功实现了Linux提权攻击。该实验通过生成两个不同的信息，使它们在经过MD5运算后生成相同的哈希值，并利用此特性设计了一种新的渗透攻击方法。实验过程中，主要使用了Python和C编程，并在Ubuntu平台上进行攻击测试。最终，成功生成了两个hash值相同但功能不同的可执行文件，实现了提权攻击。

### 使用

#### fastcoll安装

- Windows：直接使用fastcoll.exe即可

- Linux：

  - 首先安装依赖：

    ```
    $ sudo apt-get install libboost-all-dev
    $ sudo apt-get install python3
    ```

  - 进入`./fastcoll/`目录，使用`make`进行编译得到`fastcoll`，并将其移入主目录下

#### 攻击执行

- 样例准备：

  - Windows：编写了在Windows下的测试样例`test.c`，若要测试，将`my_attack.py`中`IS_Linux=False`即可。
  - Linux：编写了在Linux下的测试样例`download_script.c`，若要测试，需要首先将该代码在Linux环境下进行编译（已经提供了32位的ELF程序），将`my_attack.py`中`IS_Linux=True`即可。

- 生成文件：执行`python3 my_attack.py`即可

- 测试样例：

  - Windows：直接在控制台运行`.\good.exe .\evil.exe`即可。

  - Linux：需要为生成的攻击文件赋予执行权限`chmod a+x ./download_script_good ./download_script_evil`。

    

