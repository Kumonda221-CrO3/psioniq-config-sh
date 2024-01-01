# psioniq-config-sh
> psioniq File Header 配置生成脚本

这是一个用于生成**源代码文件头**配置文件的脚本。  
主要用于向源代码文件的头部插入 LICENSE 信息。  
该脚本所生成的配置文件适用于 (Visual Studio Code) **psioniq File Header** 插件。 

## **0. 开始之前**  
- 确保你已在你的 Visual Studio Code 工作环境中安装了 **psioniq File Header** 插件。
- 确保你的工作环境可以运行 python 脚本。  

## **1. 工作目录**
- **./licenses/**  
所有可供使用的 **LICENSE 文件头模板** 文本文件(.txt) 都应存放在此目录下。  
该目录下默认提供了一些常用的 LICENSE 文本。
- **./psi-config.ini**  
主要配置文件。  
- **./psi-config.py**  
主要脚本文件。
- **./psi-config.sh**  
自定义脚本文件。  

## **2. 使用方法**  
### **2.1 配置文件**  
此脚本的配置文件为 **INI 格式**。  
如果对 INI 格式 有疑问请查阅网上的资料。  
配置文件的基本结构如下：
```ini
[default]
license = mulanpsl-2-0
year = 2024
holder0 = Kumonda 221 <kumonda@kucro3.org>

[danny-and-jake-love-mit]
license = mit
year = 2024
holder0 = Danny
holder1 = Jake
year1 = 2023
```  

### **2.1 配置文件中的 ```license``` 键**  
你可以在配置文件的某一节中，使用 ```license``` 键来指定使用的 LICENSE 文本。  
该文本必须存在于 ```licenses/``` 目录中，并且文件名必须为为 ```<license>.txt```。  

### **2.2 配置文件中的 ```year``` 键**  
你可以在配置文件的某一节中，使用 ```year``` 键来指定版权信息的年份。  
如果 ```year``` 在配置文件中没有指定，则默认为当前的年份，格式为 ```yyyy```。  
例如当前日期如果为 ```2023-12-31```，则在未指定时的默认值为 ```2023```。  
该键的值类型总是为字符串，也就是说你不需要保证它遵循任何的格式（从使用脚本的层面来说）。例如你想要在 ```year``` 中指定一个年份的范围，按照你自己的格式尽情填写就好了。  

### **2.3 配置文件中的 ```holder<n> (0~7)``` 键**  
你可以在配置文件的某一节中，使用 ```holder0``` (0~7) 键来添加版权所有者信息。  
该键后的编号不总是需要从```0```开始的，但不可以大于```7```，数字只是为了区分不同的版权所有者，并确定他们之间出现的顺序。  
**注意：** 如果你在文件中编写了两个或多个 ```holder0``` （或其他数字相同的）键，脚本可能不会报错，此时的输出行为是不确定的。  
如果你编写了某个 ```holder<n>``` 键，且它对应的值为空，例如：  
```ini
holder0 = Colton 
holder1 = 
holder2 = David
```  
那么他将不会在最终的输出中产生单独的一行。此例中其输入如下：  
```cpp
/**
 * Copyright (c) 2024 Colton
 * Copyright (c) 2024 David
 *
...
```  

### **2.4 配置文件中的 ```year<n>``` 键**  
你可以在配置文件的某一节中，使用 ```year0``` (0~7) 键来单独指定某个版权所有者的时间信息。  
该键后的编号不总是需要从```0```开始的，但不可以大于```7```，并且应当存在对应的 ```holder<n>``` 键，否则将不会生效。  
**注意：** 如果你在文件中编写了两个或多个 ```year0``` （或其他数字相同的）键，脚本可能不会报错，此时的输出行为是不确定的。  
如果未指定 ```year<n>```，则对应的年份信息则会使用默认或全局指定的。即在 ```year``` 键存在时，默认使用 ```year``` 键对应的值；若 ```year``` 也不存在，则默认使用当前的年份，见 **2.2** 节。  
如果你编写了某个 ```holder<n>``` 键，且它对应的值为空，则不会生效。  
例如：
```ini
year = 2024       
holder0 = Lumos Maxima
holder1 = Avada Kedavra
year1 = 2017-2019
```  
对应的输出为：
```cpp
/**
 * Copyright (c) 2024      Lumos Maxima
 * Copyright (c) 2017-2019 Avada Kedavra
 *
...
```
注意：在脚本中对于不同长度的年份信息自动进行了对齐，并总是对齐为最长的年份信息。

### **2.5 使用参数 ```-c``` ```--config``` 来重定向配置文件**  
在运行脚本时，可以通过 ```-c``` 或 ```--config``` 参数来指定其他的配置文件路径。  
默认情况下脚本会使用当前目录下的 ```psi-config.ini``` 文件。 

### **2.6 使用参数 ```-s``` ```--section``` 来使用不同的配置组**
你可以在配置文件中同时保留多个不同的小节，以此来通过脚本灵活地配置各自的文件头。  
在运行脚本时，可以通过 ``-s`` 或 ``--section`` 参数来指定启用的配置小节。  
在默认情况下，即没有指定 ``-s`` 或 ``--section`` 参数时，则会默认使用 **[default]** 小节中的配置信息。  
例如，对于 **2.1** 节中列出的配置，用参数 ``-s danny-and-jake-love-mit`` 启动脚本后，你在 VSCode 中可以得到类似如下的文件头：
```cpp
/**
 * Copyright (c) 2024 Danny
 * Copyright (c) 2023 Jake
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of 
 * this software and associated documentation files (the “Software”), to deal in 
 * the Software without restriction, including without limitation the rights to use, 
 * copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
 * Software, and to permit persons to whom the Software is furnished to do so, 
 * subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all 
 * copies or substantial portions of the Software.
...
```

### **2.7 使用参数 ```-l``` ```--license``` 来指定默认 LICENSE 文本**
在运行脚本时，可以通过 ```-l``` 或 ```--license``` 参数来额外指定默认的 LICENSE 文本。   
如果配置文件的某节中没有指定 ```license``` 键，那么该节就会使用默认的 LICENSE 文本。  
默认情况下为 ```default``` 文本。  

### **2.8 使用参数 ```-o``` ```--output``` 来指定输出文件**  
在运行脚本时，可以通过 ```-o``` 或 ```--output``` 参数来指定配置的输出目标。  
默认情况下输出到 ```./psi-config-out.json```。  
> **注意：**  
> - 如果指定的 **JSON 文件** 不存在，则会创建一个。  
> - 如果指定的 **JSON 文件** 已经存在，那么会保留其中原有的其他项，并在其基础上额外添加、覆盖脚本输出的配置项。  
> - 如果指定的文件**不是合法的 JSON 格式**，那么脚本可能出错。  

## **3 TIPS**
### **3.1 直接输出到 VSCode settings.json**  
脚本支持直接将输出重定向到**已经存在的合法 JSON 文件**，所以你可以直接将输出目标参数写为 ```-o YOUR_VS_CODE_PROJECT_ROOT/.vscode/settings.json```，而不用担心丢失你原有的 VSCode 设置。

