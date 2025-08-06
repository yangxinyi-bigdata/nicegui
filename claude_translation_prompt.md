# NiceGUI 中文翻译任务提示词

## 任务概述
请帮助我继续翻译 NiceGUI 项目中的文档内容。
对website/documentation/content中的代码中的和网站内容相关的英文字符串翻译成中文.

## 已完成的翻译工作
请先查看 `translation_progress.md` 文件了解已完成的翻译进度：
- 已翻译28个主要UI组件文档文件（website/documentation/content/）
- 已翻译核心文件 nicegui/element.py

## 当前任务
继续翻译 `website/documentation/content/` 目录中尚未翻译的文档文件。

## 翻译要求

### 1. 翻译范围
- 所有 `@doc.demo()` 装饰器下的演示说明
- 组件功能描述和使用说明
- 参数说明和示例代码注释
- 最佳实践和注意事项
- 函数和类的文档字符串

### 2. 翻译质量标准
- **技术术语一致性**：保持专业术语的统一性（如 "element" → "元素"，"component" → "组件"）
- **语言自然性**：使用自然流畅的中文表达，避免机器翻译的生硬感
- **准确性**：确保技术内容的准确传达，不遗漏重要信息
- **完整性**：保留所有参数文档、类型注解和版本信息
- **格式保持**：维持原有的代码结构、缩进和格式

### 3. 技术术语对照表
- element → 元素
- component → 组件
- slot → 插槽
- props → 属性
- event → 事件
- handler → 处理器
- callback → 回调函数
- client → 客户端
- server → 服务器
- update → 更新
- render → 渲染
- binding → 绑定
- reactive → 响应式

### 4. 翻译示例
```python
# 英文原文
def on_click(self, handler: Callable) -> None:
    """Register a click event handler.
    
    :param handler: function to call when the element is clicked
    """

# 中文翻译
def on_click(self, handler: Callable) -> None:
    """注册点击事件处理器。
    
    :param handler: 元素被点击时调用的函数
    """
```

## 操作步骤

### 第一步：分析待翻译文件
1. 运行命令查看所有文档文件：
   ```bash
   ls website/documentation/content/*.py
   ```

2. 对比 `translation_progress.md` 中已完成的文件列表

3. 找出尚未翻译的文件

### 第二步：批量翻译
1. 优先翻译重要的UI组件文档
2. 每次翻译一个文件，确保质量
3. 翻译完成后更新 `translation_progress.md`

### 第三步：质量检查
1. 确保翻译后的代码可以正常运行
2. 检查技术术语的一致性
3. 验证文档字符串的完整性

## 特殊注意事项

### 1. 保留代码结构
- 不要修改函数名、变量名、类名
- 保持原有的参数类型注解
- 维持代码的缩进和格式

### 2. Vue.js 相关概念
- slot → 插槽（需要详细解释Vue插槽概念）
- template → 模板
- component → 组件
- props → 属性



## 完成后更新
翻译完成每个文件后，请更新 `translation_progress.md` 文件，添加新翻译的文件到列表中。

---

**开始命令建议**：
```bash
# 查看所有文档文件
ls website/documentation/content/*.py | wc -l

# 找出可能尚未翻译的文件
ls website/documentation/content/*.py | head -10
```

请开始翻译工作。
