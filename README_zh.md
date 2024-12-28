<!--
 MIT License
 
 Copyright (c) 2024 - 2024 Wick Dynex
 
 许可在此免费授予任何获得此软件及其相关文档文件（以下简称“软件”）副本的人，  
 可以在不受限制的情况下使用、复制、修改、合并、发布、分发、再许可和/或销售软件的副本，并且允许向其提供该软件的人执行上述操作。

 上述版权声明和本许可声明应包含在软件的所有副本或实质性部分中。
-->

# AutoLicense

一个用于自动向目标目录中的源代码文件添加许可头的 Python 工具。该工具根据用户指定的参数生成许可头，按照文件类型进行格式化，且仅在文件缺少许可头时才会添加。

## 功能

- **自动添加许可头**：将可定制的许可头添加到目标目录中支持的文件。
- **许可文本生成**：根据输入参数（例如许可类型、作者、开始年份）动态生成许可文本。
- **文件类型检测**：自动检测文件类型（例如 Python、Java、C++），并应用适当的注释样式。
- **许可头存在检查**：检查文件是否已经存在许可头，避免重复添加。
- **批量处理**：支持一次性向目录中的多个文件添加许可头。

## 要求

- Python 3.x

## 使用方法

运行以下命令将许可头添加到目标文件夹中的所有支持文件：

```bash
python main.py  --license-file=LICENSE_FILE 
                --license-type=LICENSE_TYPE 
                --start-year=START_YEAR
                --author=AUTHOR 
                --target-folder=TARGET_FOLDER 
                [--end-year=END_YEAR] 
                [--detail]
```

## 命令行参数

以下参数是工具正常运行所必需的：

- `--license-file=LICENSE_FILE`:  
  描述：许可文件的路径（例如 `data/license.json`）。  
  注意：此 JSON 文件必须包含需要添加的许可类型。

- `--license-type=LICENSE_TYPE`:  
  描述：指定要添加的许可类型。该许可类型必须在提供的 `.json` 文件中定义（例如 `MIT License`、`Apache License 2.0`）。  
  注意：许可类型必须存在于 JSON 文件中的 "licenses" 对象内。

- `--start-year=START_YEAR`:  
  描述：许可头的开始年份（例如 `2024`）。  
  注意：这是一个必需的参数，且必须小于或等于 `--end-year`。

- `--end-year=END_YEAR`:  
  描述：许可头的结束年份（可选）。  
  注意：如果未指定，则 `end-year` 默认为当前年份。

- `--author=AUTHOR`:  
  描述：作者或组织的名称（例如 "John Wick"）。  
  注意：这是一个必需的参数。

- `--target-folder=TARGET_FOLDER`:  
  描述：需要添加许可头的目标目录或文件路径。  
  注意：这必须是一个有效且可写的目录或文件路径。

- `--detail`:  
  描述：如果包括此参数，将提供详细输出，显示哪些文件被修改以及添加的许可文本。  
  默认情况下，输出是简洁的（即不显示详细信息）。

## 示例

### 示例用法

运行脚本并向目标文件夹中的文件添加许可头，使用以下命令：

```bash
python main.py  --license-file="data/license.json" 
                --license-type="MIT License"
                --start-year=1998 
                --end-year=2023 
                --author="John Wick" 
                --target-folder="./folder"
```

### 预期输出

```bash
License file: data/license.json
License type: MIT License
Start year: 1998
End year: 2023
Author: John Wick
Target folder: ./folder
Show details: False
```

## 许可证

- 本项目采用 [MIT License](https://opensource.org/licenses/MIT) 许可证。
