Nebula python 客户端使用说明
--------------------------------------------
环境需求

```bash
    python==3.7
    prettytable==2.1.0
    nebula2-python==2.0.0
```	

## 根据特定「名称+类别」的实体，从数据库中获取概念、上位实体、同意实体等关系数据


```bash
    name = "苹果手机"
    type = "PRODUCT"
    nebula = Nebula()
    concept_resp, entity_resp, synonym_resp = nebula.getEntityConcept(name, type)
```

## 根据特定「名称+类别」的实体，从数据库中获取同概念下其他实体、相同上位实体下的其他实体


```bash
    name = "苹果手机"
    type = "PRODUCT"
    nebula = Nebula()
    concept_resp, entity_resp = nebula.getCommonEntityConcept(name, type)
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