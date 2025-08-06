# NiceGUI Elements 核心组件翻译任务提示词

## 任务概述
请帮助我翻译 NiceGUI 项目中 `nicegui/elements/` 目录下的 Python 文件中的文档字符串，将英文翻译为中文。这些文件是 NiceGUI 框架的核心UI组件实现文件。

## 目标目录
`nicegui/elements/` - NiceGUI 核心UI组件实现文件

## 已完成的翻译工作
请先查看 `translation_progress.md` 文件了解已完成的翻译进度：
- 已翻译69个UI组件文档文件（website/documentation/content/）
- 已翻译核心文件 nicegui/element.py

## 当前任务重点
翻译 `nicegui/elements/` 目录中的核心组件实现文件的文档字符串。这些是实际的组件类定义文件，与之前翻译的文档展示文件不同。

## 翻译范围

### 1. 主要翻译内容
- **类的文档字符串**：组件类的主要描述
- **方法的文档字符串**：所有公共方法的功能说明
- **参数文档**：所有参数的类型和用途说明
- **属性文档**：重要属性的功能描述
- **使用示例**：代码中的示例和注释
- **版本信息**：版本更新说明

### 2. 不需要翻译的内容
- 函数名、变量名、类名
- 参数类型注解
- 代码逻辑部分
- HTML/CSS 类名和样式
- JavaScript 代码片段

## 翻译质量标准

### 1. 技术术语一致性
保持与已翻译文件相同的术语对照：
- element → 元素
- component → 组件
- props → 属性
- event → 事件
- handler → 处理器
- callback → 回调函数
- client → 客户端
- update → 更新
- render → 渲染
- binding → 绑定
- slot → 插槽
- template → 模板

### 2. UI组件特定术语
- button → 按钮
- input → 输入框
- label → 标签
- card → 卡片
- dialog → 对话框
- table → 表格
- grid → 网格
- column → 列
- row → 行
- menu → 菜单
- tab → 选项卡
- icon → 图标
- image → 图像
- video → 视频
- audio → 音频

### 3. Quasar 组件术语
- QButton → Q按钮组件
- QInput → Q输入框组件
- QCard → Q卡片组件
- QTable → Q表格组件
- QDialog → Q对话框组件
- QMenu → Q菜单组件

## 翻译示例

### 类文档字符串示例
```python
# 英文原文
class Button(Element):
    """A clickable button component.
    
    This component creates a button that can be clicked to trigger actions.
    It supports various styles and can contain text or icons.
    """

# 中文翻译
class Button(Element):
    """可点击的按钮组件。
    
    此组件创建一个可以点击以触发操作的按钮。
    它支持各种样式，可以包含文本或图标。
    """
```

### 方法文档字符串示例
```python
# 英文原文
def on_click(self, handler: Callable[[], None]) -> Self:
    """Register a click event handler.
    
    :param handler: function to call when the button is clicked
    :return: the button instance for method chaining
    """

# 中文翻译
def on_click(self, handler: Callable[[], None]) -> Self:
    """注册点击事件处理器。
    
    :param handler: 按钮被点击时调用的函数
    :return: 用于方法链式调用的按钮实例
    """


### 第二步：选择文件进行翻译
1. 从基础组件开始
2. 优先翻译使用频率高的组件
3. 每次专注翻译一个文件

### 第三步：翻译检查清单
- [ ] 类的主要文档字符串已翻译
- [ ] 所有公共方法的文档字符串已翻译
- [ ] 参数说明完整且准确
- [ ] 保持了原有的代码结构
- [ ] 技术术语使用一致
- [ ] 版本信息已保留

## 特殊注意事项

### 1. 保持代码功能性
- 绝对不要修改类名、方法名、变量名
- 保持所有的类型注解不变
- 维持原有的缩进和代码格式

### 2. Vue.js 和 Quasar 集成
- 理解Vue组件的属性传递机制
- 正确翻译Quasar组件的功能描述
- 保持对前端概念的准确理解

### 3. 事件处理系统
- 准确翻译事件类型和处理机制
- 理解客户端-服务器通信模式
- 保持回调函数概念的清晰

### 4. 组件生命周期
- 理解组件的创建、更新、销毁过程
- 准确翻译生命周期相关的方法

## 完成后更新
翻译完成每个文件后，请更新 `translation_progress.md` 文件，在 "核心框架文件 (nicegui/)" 部分添加新翻译的文件。
