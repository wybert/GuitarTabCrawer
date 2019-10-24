# GuitarTabCrawer
下载吉他社吉他谱

## 安装

下载 guitar_dl.py

```bash
git clone https://github.com/wybert/GuitarTabCrawer.git
```

将`guitar_dl.py`copy到python安装路径下的`Lib`文件夹下

## 使用帮助

```bash
python guitar_dl.py --help
python -m guitar_dl --help

Usage: guitar_dl.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  download  A tools for download tabs from jitashe.org
  search    search tabs from jitashe.org
```

## 搜索谱子

```bash
python guitar_dl.py search --help
Usage: guitar_dl.py search [OPTIONS]

  search tabs from jitashe.org

Options:
  --keywords TEXT  the keywords you want to search
  --help           Show this message and exit.
```

使用例子
 
```bash
python guitar_dl.py search --keywords "女儿情"
```

## 下载谱子

```bash
python guitar_dl.py download --help
Usage: guitar_dl.py download [OPTIONS]

  A tools for download tabs from jitashe.org

Options:
  --url TEXT  the url of one guitar tab
  --help      Show this message and exit.
```

使用例子

```bash
python guitar_dl.py download --url "https://www.jitashe.org/tab/21669/"
```

## TODO

1. 打包应用程序
2. 批量下载功能
3. 省略参数的设置



