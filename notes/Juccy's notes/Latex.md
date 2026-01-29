
# LaTeX 基本框架

## 文档类型 `\documentclass{...}`
1.  `article`
        *   **用途**：最基础的短篇文档格式，适合写论文、报告、短文、期刊文章、作业等篇幅较短、结构相对简单的内容。
        *   **特点**：没有 `\chapter` 层级，只有 `\section`、`\subsection` 等；排版简洁，默认单栏，适合快速产出学术短文。
2.  `book`
        *   **用途**：专门用于编写书籍、长篇专著、毕业论文等需要完整书籍结构的文档。
        *   **特点**：支持 `\chapter` 层级，自带书籍特有的元素（如扉页、目录、前言、附录、索引等），默认双栏排版，适合多章节、多部分的大型作品。
3.  `beamer`
        *   **用途**：用来制作演示文稿（幻灯片）的文档类，生成的 PDF 可以直接用于课堂、会议演讲。
        *   **特点**：以 `\frame` 为单位组织每页幻灯片，内置大量主题、模板、动画和导航功能，支持分点展示、代码高亮、图表嵌入，是学术圈做报告的首选工具。
*   **简单总结**：
        *   写小论文 / 作业 → `article`
        *   写书 / 长篇论文 → `book`
        *   做幻灯片 / 演讲 → `beamer`

## 宏包 `\usepackage{}`
 *   **示例**：`\usepackage{graphicx}` （用于插入图片）
 *   **Tips**：`%` 后为注释
 *   **概念**：类似插件与浏览器的关系，用来扩展/增强LaTeX的功能。
        *   一般加在 `\begin{document}` 之前。
 *   **示例：实现中文支持**
        *   **方法一（CJK宏包）**:
            ```latex
            \documentclass{article}
            \usepackage{CJKutf8}
            \begin{document}
            \begin{CJK}{UTF8}{gkai}
            你好， LaTeX!
            \end{CJK}
            \end{document}
            ```
            *   正文放在 `\begin{CJK}{UTF8}{gkai}` 与 `\end{CJK}` 之间。
        *   **方法二（ctex文档类）**:
            ```latex
            \documentclass{ctexart}

## 标题信息
 *   命令：
        *   `\title{你好， LaTeX!}`
        *   `\author{JUJU}`
        *   `\date{\today}` （`\today` 会自动输出编译当天的日期）
*   **位置**：只能放在**导言区**（即 `\documentclass` 与 `\begin{document}` 之间的区域）。
*   **显示**：通过 `\maketitle` 命令将标题信息展现出来。

## 目录
 *   在正文合适位置（通常紧随 `\maketitle` 之后）添加命令：`\tableofcontents`

## 文章段落与结构
 *   **章节命令**：
        *   `\section{第一章}`
        *   `\subsection{第一小节}`
        *   `\section*{第一节}` （带 `*` 号表示不编号，也不列入目录）
*   **换行与分段**：
        *   单纯换行（不空行）在源码中不会被识别为新段落。
        *   空一行表示开始新的段落。
    *   **强制换页**：`\newpage`
    *   **公式中插入文字**：使用 `\text{}` 命令。
    *   **特殊字体**：
        | 字体 | 命令 |
        | :--- | :--- |
        | 直立 | `\textup{}` |
        | 意大利 | `\textit{}` |
        | 倾斜 | `\textsl{}` |
        | 小型大写 | `\textsc{}` |
        | 加宽加粗 | `\textbf{}` |

## 插入图片
*   **前提**：需要使用 `graphicx` 宏包 (`\usepackage{graphicx}`)。
  *   **方式一：带编号的浮动体（推荐）**
      ```latex
        \begin{figure}[htbp]
            \centering
            \includegraphics[width=8cm]{tu1.jpg}
            \caption{等比定律}
        \end{figure}
        ``` 
 *  `[htbp]`：位置参数，自动选择插入图片的最优位置。
 *   `\centering`：让图片居中。
 *   `[width=8cm]`：设置图片宽度。
 *   `\caption{}`：设置图片的标题（会自动编号）。
  *   **方式二：居中环境（无编号）**
        ```latex
        \begin{center}
            \includegraphics[width = .88\textwidth]{tu1.jpg}
            图1\quad 等比定律 % \quad 是一个大空格，\qquad 更长
        \end{center}
        ```
        *   `tu1.jpg` 必须和 `.tex` 文件在同一文件夹下，否则需指定路径。x
*  *   Overleaf 中需先上传图片文件。
* Sim Exp:VS Code中，使用 \graphicspath 设置搜索路径
     在导言区设置相对路径
        latex

        \documentclass{article}
        \usepackage{graphicx}

        % 设置图片搜索路径（可以设置多个，按顺序查找）
        \graphicspath{
         {./}                    % 当前目录
         {../figures/}           % 上一级的figures文件夹
            {../../figures/}        % 上两级的figures文件夹
            {../../../figures/}     % 上三级的figures文件夹
         {figures/}              % 当前目录下的figures文件夹
        }
        \begin{document}

        % 现在只需要写文件名，LaTeX会自动在以上路径中查找
        \includegraphics[width=0.8\textwidth]{fig1_concentration_trend.pdf}

        \end{document}
       
    *   **多图并列插入（使用子图）**
        *   需要 `subfigure` 宏包：`\usepackage{subfigure}`
        ```latex
        \begin{figure}[htbp]
            \centering
            \subfigure[浮子的位移和速度随时间的关系图]{
                \includegraphics[width = .47\textwidth]{2-1.png}
            }
            \quad
            \subfigure[振子的位移和速度随时间的关系图]{
                \includegraphics[width = .47\textwidth]{2-2.png}
            }
            \caption{情况2时的浮子与振子的垂荡位移和速度}
        \end{figure}
        ```

## 列表与表格

### 列表
  1.  **无序列表 (`itemize`)**
        ```latex
        \begin{itemize}
            \item[*] 第一点
            \item[+] 第二点
            \item[.] 第三点
        \end{itemize}
        ```
  2.  **有序列表 (`enumerate`)**
        ```latex
        \begin{enumerate}
            \item 第一点
            \item 第二点
        \end{enumerate}
        ```
  3.  **描述列表 (`description`)**
        ```
        latex
        \begin{description}
            \item[术语1] 描述1
            \item[术语2] 描述2
        \end{description}
        ```
*   **对比总结**：
     | 命令 | 列表类型 | 核心特征 | 典型用途 |
     | :--- | :--- | :--- | :--- |
     | `enumerate` | 有序列表 | 自动生成编号（1.、2.、A.） | 步骤、流程、排序 |
    | `itemize` | 无序列表 | 自动生成符号（・、□、△） | 并列要点、注意事项 |
    | `description` | 描述列表 | 突出「术语」+ 解释 | 概念定义、术语说明 |

### 表格
 *   **基本表格示例**：
        ```latex
        \begin{table}[htbp]
            \centering % 居中
            \caption{符号说明} % 自动生成带编号的标题（如“表 1 符号说明”）
            \label{tab:symbol} % 加标签，方便正文用 `\ref{tab:symbol}` 引用。必须放在 `\caption{}` 之后。
            \setlength\tabcolsep{40pt} % 设置列间距
            \renewcommand{\arraystretch}{1.4} % 设置行高
            \begin{tabular}{c c} % 列对齐方式：c居中，l左对齐，r右对齐
            \hline
            符号 & 含义 \\ \hline
            $E_i$ & 第 $i$ 个企业 \\
            $r_i$ & 企业 $E_i$ 的评价指标向量 \\
            \hline
            \end{tabular}
        \end{table}
        ```
*   **使用 `booktabs` 宏包美化表格**：
    *   导入宏包：`\usepackage{booktabs}`
    *   用 `\toprule`（粗顶线）、`\midrule`（细中线）、`\bottomrule`（粗底线）替代 `\hline`，使横线更有层次感。
        ```latex
        \begin{tabular}{c c}
            \toprule
            符号 & 含义 \\
            \midrule
            $E_i$ & 第 $i$ 个企业 \\
            $r_i$ & 企业 $E_i$ 的评价指标向量 \\
            \bottomrule
        \end{tabular}
        ```
* 1st Sim Exp：
  * 表格内容多，右侧溢出的处理：
     * 首选用tabularx自动调整列宽
      ```latex
      \usepackage{tabularx} % 在导言区添加此包
     \begin{tabularx}{\textwidth}{l>{\raggedright}Xc>{\raggedright\arraybackslash}X}
     ```
  * tabularx环境中的X列会自动调整宽度以填满指定的总宽度（\textwidth）
  * 表格内容，字比较多的，换行不好看，可以考虑scale缩放，不行再改字体、 \small或斜体、调整列宽 
  * 直接scale更方便，在\label{}之后加上```
      \resizebox{0.95\linewidth}{!}{
      \begin{tabular}{ll}
      然后记得
      \end{tabular}之后加上右括号‘}’
      最后才\end{table}
  - 就想把字体放小：在**表格环境（table）内部、开始tabular/tabularx之前**添加```\small```命令

## 插入代码
*   **前提**：调用 `listings` 宏包 (`\usepackage{listings}`)。
*   **基本用法**：
    ```latex
    \begin{lstlisting}[language=Python] % language 选项用于语法高亮
    # 你的代码放在这里
    print("Hello, LaTeX!")
    \end{lstlisting}
    ```
  * 注意：默认设置下代码块内不能直接输入中文（会报错）。
*   **美化**：可以在导言区进行更多预设调整（参考 LaTeX `listings` 宏包文档）。

## 插入伪代码/算法
 *   **简单方法（使用 `algorithm` 宏包）**：
        ```latex
        \begin{algorithm}
            \caption{算法标题}
            \label{alg:algorithm-label}
            \begin{algorithmic}
                ... 你的伪代码 ...
            \end{algorithmic}
        \end{algorithm}
        ```
  -  `algorithm` 环境使算法部分成为一个浮动体，防止跨页。
*   **常用组合**：
       *   `algorithm` + `algorithmicx` + `algpseudocode` 等。

## 标号与引用
*   分为三类引用：
        1.  **公式引用**
        2.  **表格引用**
        3.  **图片引用**
 *   **通用方法**：
    1.  为需要引用的对象（公式、表格、图片）使用 `\label{标签名}` 命令添加标签。
    2.  在正文中需要引用的位置使用 `\ref{标签名}` 命令进行引用，LaTeX 会自动替换为对应的编号。

## 参考文献
* **方法一：直接在 `.tex` 文件中编写 (`thebibliography` 环境)**
     ```latex
        \usepackage{natbib} % 可选，提供更多引用样式
        \begin{document}
        正文中引用：比如推理、决策等\cite{a}。
        \begin{thebibliography}{99}
            \bibitem{a} 邱锡鹏. \emph{神经网络与深度学习}[M]. 机械工业出版社， 2020.
            \bibitem{b} 周志华， 王珏. \emph{机器学习及其应用 2009}[M]. 清华大学出版社， 2009.
            \bibitem{c} 蒋宗礼. \emph{人工神经网络导论}[M]. 北京：高等教育出版社， 2008: 40-44.
        \end{thebibliography}
        \end{document}
      ```
* `\cite{a}`：花括号里的字母与 `\bibitem{}` 后的标签保持一致即可引用。
* *   `\emph{}`：将书名、期刊名变为斜体，符合学术排版规范。
*   **方法二：使用独立的 `.bib` 文件管理（更专业、方便）**
    *   使用 `BibTeX` 或 `Biber` 工具进行编译。
     *   在文档中通过 `\bibliographystyle{样式}` 和 `\bibliography{文件名}` 命令导入。

---

**便捷操作**：在大多数 LaTeX 编辑器（如 Overleaf）中，选中多行后按 `Ctrl` + `/` 可一键批量添加/取消注释。
- 🔍 三种常见横线对比：

| 输入代码 | 输出符号 | 名称 | 用途 |
|----------|----------|------|------|
| `-`      | -        | hyphen（连字符） | 单词断行、复合词（如 `state-of-the-art`） |
| `--`     | –        | en dash（短破折号） | 表示范围（1896–1950, pages 10–15）✅ |
| `---`    | —        | em dash（长破折号） | 插入语、强调（The result—surprisingly—was null.） |
# 美赛论文撰写注意事项
> 📌 **规范提示**：在学术写作（包括美赛 MCM/ICM 论文）中，日期或数字范围必须使用 en dash（–），这是排版基本规范。
> 范围 → “--”
## **数学符号**
必须用 LaTeX 命令

    乘号：\times（生成 ×）
    除号：\div（生成 ÷）
    不等号：\geq（生成 ≥）
    （禁止直接输入符号或字母）
    注意都要前后加上‘$’!

  - 空格规范
>
    正确：2.1 $ \times $ （无空格）
    错误：2.1  $ \times $ （多空格破坏数字连贯性）
    （美赛论文要求数字与符号无缝衔接）
## 页码
- 注意：content开始是第二页，要手动调一下（因为模板中title页单独出来了）
  ```\end{abstract} 和 \tableofcontents 之间加：\setcounter{page}{2}```
- 编译完后未显示总页数，总页数那是“？？”
  - 检查导言区（\begin{document} 之前的部分）是否包含```\usepackage{lastpage}``` 如果没有，加上这行代码，然后再重新编译两次
## 段落
- 首行缩进 模板中第一段不缩进SOL:引入 indentfirst 宏包
  在文件的导言区（即 \documentclass 之后，\begin{document} 之前）添加：
     ``` \usepackage{indentfirst} % 强制让每一章节的第一段也进行首行缩进```
  - 对需要单独调的summary部分：在 \begin{abstract} 后面紧跟一个 ```\indent```
  - 手动控制：如果引入宏包后某一段仍未缩进（说是极少数情况 实际总遇到），可以在该段开头手动输入``` \indent```或```\setlength{\parindent}{1.5em}```；反之，若想让某段不缩进，使用 ```\noindent```
## 插入图表 
- 要强制某一位置[H] ,导言区记得加宏包```\usepackage{float}```
## MEMORANDUM 
- 新开一页来放，没页眉 → 在```\newpage```和```\section{Memorandum}```之间加```\thispagestyle{fancy}```
- 落款，右对齐实现:用 ```flushright ```环境包裹落款，实现右对齐
        \begin{flushright}
        Respectfully submitted,\\
        Team 2613942
        \end{flushright}  

## ASSUMPTION 部分
- Justification前面加箭头用```$\rightarrow\ $ ```

# 典型报错处理
-  “Missing $ inserted”
   -  核心问题是“特征名称中的下划线未正确处理”——LaTeX中 plain text（普通文本）里的下划线_默认是“数学模式下的下标符号”，若直接写global_point_idx，LaTeX会误认为你在使用数学下标，却未找到对应的数学环境（$...$）