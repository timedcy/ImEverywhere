# ImEverywhere
`Intelligent assistant Robot based on 'Machine Learning'. 'ImEverywhere' means 'I am everywhere'.`
`基于机器学习的智能助手机器人`
`Copyright © 2016 Rain. All Rights Reserved. `

```
支持(Support)：AIML + 机器学习 + 自定义对话场景模板 + API插件 + 用户注册登录
维护(Current Maintainer)：decalogue (1044908508@qq.com)
```

- [x] 本地内核：AIML（支持中文）
    - [x] Python2和Python3实现
    - [x] 机器学习接口
    - [x] API接口
- [ ] 机器学习(考虑Python3处理中文字符编码的优势，先实现Python3版本)
    - [ ] 架构图形学习网络
    - [x] 上下文信息存储
        - [x] 图形数据库neo4j存储
        - [x] 语义依存树的neo4j表示与存储
        - [x] 大规模语料的语义依存树训练，语义与功能标注
        - [ ] LSTM长短期记忆神经网络
    - [x] 语义理解
        - [x] 中文分词(TODO:自定义词典以及训练，新词发现)
        - [x] 词性标注
        - [x] 命名实体识别
        - [x] 关键词提取
        - [x] 依存句法分析
        - [x] 语义角色标注
        - [x] 语义依存分析
        - [x] 由“命名实体+关键词+语义依存树”生成检索请求
    - [ ] 数据库检索
        - [x] 图形数据库neo4j存储
        - [x] 将检索请求加入上下文存储
		- [x] 同义词词库加入数据库
        - [ ] 比对检索关系图(计算“语义依存树+功能标注”的相似度)
        - [x] 返回候选关系图列表
    - [ ] 答案抽取
        - [x] 对候选关系图抽取和提问一致的实体
        - [ ] 根据候选关系图的概率属性排序
    - [ ] 语句生成
        - [x] 对概率最大的候选关系图确定回答句子主干
        - [ ] 随机生成回答句子枝叶
- [ ] API集合
    - [x] Tuling
    - [x] 语音识别ASR
    - [x] 语音合成TTS
    - [x] 腾讯优图
    - [x] 百度糯米
    - [x] 百度地图
    - [ ] 百度云
    - [ ] 印象笔记
- [ ] 网页客户端
    - [ ] Python-Django
    - [ ] Ruby-Ruby on Rails
- [ ] 微信客户端
    - [x] 个人微信号
    - [ ] 订阅号/服务号
- [ ] APP
- [ ] doc 项目的sphinx文档

[樱落清璃-Decalogue的CSDN博客](https://www.decalogue.cn)
