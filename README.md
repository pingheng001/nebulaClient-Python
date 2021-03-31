Nebula python 客户端使用说明
--------------------------------------------
环境需求

```bash
    python==3.7
    prettytable==2.1.0
    nebula2-python==2.0.0
```	
## 根据特定「名称+类别」的实体，从数据库中获取概念数据

```bash
    nebula = Nebula()
    concept_resp = nebula.getEntityConcept(name, type, steps=3)
```

## 根据特定「名称+类别」的实体，从数据库中获取上位实体数据

```bash
    nebula = Nebula()
    entity_resp = nebula.getEntityUpEntity(name, type)
```


## 根据特定「名称+类别」的实体，从数据库中获取同义实体数据

```bash
    nebula = Nebula()
    synonym_resp = synonym_resp = nebula.getEntitySonEntity(name, type)
```

## 根据特定「名称+类别」的实体，从数据库中获取同概念下其他实体

```bash
    nebula = Nebula()
    concept_resp = nebula.getCommonConceptEntity(name, type, steps=3, limit=10)
```

## 根据特定「名称+类别」的实体，从数据库中获取相同上位实体下的其他实体

```bash
    nebula = Nebula()
    entity_resp = nebula.getCommonUpEntity(name, type, limit=10)
```


## 结果输出
# 制表
```bash
print_resp(concept_resp)
```

# json
```bash
json_value(concept_resp)
```