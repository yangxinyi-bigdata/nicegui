from nicegui import ui

from . import doc


@doc.demo(ui.markdown)
def main_demo() -> None:
    ui.markdown('This is **Markdown**.')


@doc.demo('带缩进的 Markdown', '''
    通用缩进会自动从每行的开头剥离。
    因此您可以缩进 markdown 元素，它们仍然会正确渲染。
''')
def markdown_with_indentation():
    ui.markdown('''
        ### Example

        This line is not indented.

            This block is indented.
            Thus it is rendered as source code.

        This is normal text again.
    ''')


@doc.demo('带代码块的 Markdown', '''
    您可以使用代码块来显示代码示例。
    如果您在开头的三个反引号后指定语言，代码将会被语法高亮。
    支持的语言列表请参见 [Pygments 网站](https://pygments.org/languages/)。
''')
def markdown_with_code_blocks():
    ui.markdown('''
        ```python
        from nicegui import ui

        ui.label('Hello World!')

        ui.run(dark=True)
        ```
    ''')


@doc.demo('Markdown 表格', '''
    通过激活 "tables" 扩展，您可以使用 Markdown 表格。
    可用扩展列表请参见 [markdown2 文档](https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras)。
''')
def markdown_tables():
    ui.markdown('''
        | First name | Last name |
        | ---------- | --------- |
        | Max        | Planck    |
        | Marie      | Curie     |
    ''', extras=['tables'])


@doc.demo('Mermaid diagrams', '''
    You can use Mermaid diagrams with the "mermaid" extra.
    See the [markdown2 documentation](https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras)
    for a list of available extras.
''')
def mermaid():
    ui.markdown('''
        ```mermaid
        graph TD;
            A-->B;
            A-->C;
            B-->D;
            C-->D;
        ```
    ''', extras=['mermaid'])


@doc.demo('LaTeX formulas', '''
    By activating the "latex" extra, you can use LaTeX formulas.
    This requires markdown2 version >=2.5 as well as latex2mathml to be installed.
''')
def markdown_latex():
    ui.markdown(r'''
        Euler's identity:

        $$e^{i\pi} = -1$$
    ''', extras=['latex'])


@doc.demo('Change Markdown content', '''
    You can change the content of a Markdown element by setting its `content` property or calling `set_content`.
''')
def markdown_new_content():
    markdown = ui.markdown('Sample content')
    ui.button('Change Content', on_click=lambda: markdown.set_content('This is new content'))


@doc.demo('Styling elements inside Markdown', '''
    To style HTML elements inside a `ui.markdown` element, you can add custom CSS rules for the "nicegui-markdown" class.
''')
def markdown_styling():
    ui.add_css('''
        .nicegui-markdown a {
            color: orange;
            text-decoration: none;
        }
        .nicegui-markdown a:hover {
            color: orange;
            text-decoration: underline;
        }
    ''')
    ui.markdown('This is a [link](https://example.com).')


doc.reference(ui.markdown)
