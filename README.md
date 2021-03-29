Nebula python 客户端使用说明
--------------------------------------------

## 根据特定「名称+类别」的实体，从数据库中获取概念、上位实体、同意实体等关系数据


```bash
    name = "苹果手机"
    type = "PRODUCT"
    nebula = Nebula()
    nebula.getEntityConcept(name, type)
```

## 根据特定「名称+类别」的实体，从数据库中获取同概念下其他实体、相同上位实体下的其他实体


```bash
    name = "苹果手机"
    type = "PRODUCT"
    nebula = Nebula()
    nebula.getCommonEntityConcept(name, type)
```