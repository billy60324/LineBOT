# **中二病少年**

為了保護世界的和平，來自異世界的少年正在奮鬥著

![](https://i.imgur.com/KieLTrC.jpg)

# 功能

1. 學習
2. 忘記
3. 處男
4. 星座
5. 抽圖
6. 選擇
7. 吃啥
8. 答腔

# 資料庫

| Table name   | funtion     | 
| -----------  | ----------- | 
| QA           | 學習、忘記   | 
| MEAL         | 吃啥        |
| IMGUR_GRAPH  | 抽          |
```
CREATE TABLE QA (
    QUESTION    varchar(128) NOT NULL,
    ANSWER      varchar(128) NOT NULL,
    PRIMARY KEY  (QUESTION)
);
```
```
CREATE TABLE MEAL (
    RESTAURANT    varchar(128)    NOT NULL,
    REGION        varchar(128)    NOT NULL,
    BREAKFAST     TINYINT         NOT NULL,
    LUNCH         TINYINT         NOT NULL,
    DINNER        TINYINT         NOT NULL,
    PRIMARY KEY  (RESTAURANT)
);
```
```
CREATE TABLE IMGUR_GRAPH (
    URL    varchar(128)    NOT NULL,
    PRIMARY KEY (URL)
);

```

# 環境

Python2.7/pythonanywhere/mySQL
