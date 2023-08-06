# 电商分词

## 安装
`pip install ducut`

## 使用方式
```python
from ducut import DuCut
resource_path = '<自定义的资源文件>'
dc = DuCut(resource_path)
line = '万斯 板鞋白红'
cu = dc.cut_query(line)
print(f"brand:{cu.brand},series:{cu.series},color:{cu.color},category:{cu.category},word:{cu.word},proper:{cu.proper}")

# 加载自定义词典
dc.add_word_file("<词典路径>")
# 加载自定义单词
dc.add_word('川久保玲')
```

## 思路
- 语义实体：主要用于一些系统尚未识别的实体词，干预后，该词的切分总是能保持一致，不受其所在的上下文影响。
- 语义切分：用于指定在特定上下文中，短语的切分方式，而不影响该短语在其他上下文中的切分方式

## 参考资料
- [OpenSearch电商分词](https://developer.aliyun.com/article/659778)