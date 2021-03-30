# -*- coding:utf-8 -*-

from nebula.graph import ttypes
from nebula.ConnectionPool import ConnectionPool
from nebula.Client import GraphClient
import prettytable
import json


def print_value(column_names, rows):
    output_table = prettytable.PrettyTable()
    if rows:
        output_table.field_names = column_names
        for row in rows:
            value_list = []
            for col in row.columns:
                if col.getType() == ttypes.ColumnValue.__EMPTY__:
                    print('ERROR: type is empty')
                    return
                elif col.getType() == ttypes.ColumnValue.BOOL_VAL:
                    value_list.append(col.get_bool_val())
                elif col.getType() == ttypes.ColumnValue.INTEGER:
                    value_list.append(col.get_integer())
                elif col.getType() == ttypes.ColumnValue.ID:
                    value_list.append(col.get_id())
                elif col.getType() == ttypes.ColumnValue.STR:
                    value_list.append(col.get_str())
                elif col.getType() == ttypes.ColumnValue.DOUBLE_PRECISION:
                    value_list.append(col.get_double_precision())
                elif col.getType() == ttypes.ColumnValue.TIMESTAMP:
                    value_list.append(col.get_timestamp())
                else:
                    print('ERROR: Type unsupported')
                    return
            output_table.add_row(value_list)
        print(output_table)

def json_value(rows):
    all_values = []
    if rows:
        for row in rows:
            value_list = []
            for col in row.columns:
                if col.getType() == ttypes.ColumnValue.__EMPTY__:
                    print('ERROR: type is empty')
                    return
                elif col.getType() == ttypes.ColumnValue.BOOL_VAL:
                    value_list.append(col.get_bool_val())
                elif col.getType() == ttypes.ColumnValue.INTEGER:
                    value_list.append(col.get_integer())
                elif col.getType() == ttypes.ColumnValue.ID:
                    value_list.append(col.get_id())
                elif col.getType() == ttypes.ColumnValue.STR:
                    value_list.append(col.get_str())
                elif col.getType() == ttypes.ColumnValue.DOUBLE_PRECISION:
                    value_list.append(col.get_double_precision())
                elif col.getType() == ttypes.ColumnValue.TIMESTAMP:
                    value_list.append(col.get_timestamp())
                else:
                    print('ERROR: Type unsupported')
                    return
            all_values.append(value_list)
    return json.dumps(all_values, ensure_ascii=False)

class Nebula:
    '''
    Nebula Python 客户端
    '''
    def __init__(self):
        self.connection_pool = ConnectionPool('10.141.186.105', 3699)
        self.client = GraphClient(self.connection_pool)
        self.auth_resp = self.client.authenticate('root', 'nebula')
        # self.query_resp = self.client.execute_query('SHOW SPACES')
        self.client.execute_query("USE adeci_test")

    def __del__(self):
        self.client.sign_out()
        self.connection_pool.close()

    def getEntityConcept(self, name, type):
        '''
        # 根据特定「名称+类别」的实体，从数据库中获取概念、上位实体、同意实体等关系数据
        :param name:
        :param type:
        :return:
        '''
        # 概念
        concept_resp = self.client.execute_query('LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO FROM $-.VertexID OVER isA WHERE $$.concept.name != "" YIELD $-.name as name, $$.concept.name as conceptName;'.format(name, type))
        # 上位实体
        entity_resp = self.client.execute_query('LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO FROM $-.VertexID OVER isA WHERE $$.entity.name != "" YIELD $-.name as name, $$.entity.name as entityName;'.format(name, type))
        # 同义实体
        synonym_resp = self.client.execute_query('LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO FROM $-.VertexID OVER synonym YIELD $-.name as name, $$.entity.name as entityName;'.format(name, type))

        return concept_resp, entity_resp, synonym_resp

    def getCommonEntityConcept(self, name, type):
        '''
        # 根据特定「名称+类别」的实体，从数据库中获取同概念下其他实体、相同上位实体下的其他实体
        :param name:
        :param type:
        :return:
        '''
        # 概念
        concept_resp = self.client.execute_query('LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO FROM $-.VertexID OVER isA WHERE $$.concept.name != "" YIELD $-.name as name, $$.concept.name as conceptName, isA._dst as id | \
            GO FROM $-.id OVER isA REVERSELY YIELD $-.conceptName as name, $$.entity.name as commonName;'.format(name, type))
        # 上位实体
        entity_resp = self.client.execute_query('LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO FROM $-.VertexID OVER isA WHERE $$.entity.name != "" YIELD $-.name as name, $$.entity.name as entityName, isA._dst as id | \
            GO FROM $-.id OVER isA REVERSELY YIELD $-.entityName as name, $$.entity.name as commonName;;'.format(name, type))

        return concept_resp, entity_resp


if __name__ == "__main__":
    name = "苹果手机"
    type = "PRODUCT"

    nebula = Nebula()

    concept_resp, entity_resp, synonym_resp = nebula.getEntityConcept(name, type)
    print "概念"
    print_value(concept_resp.column_names, concept_resp.rows)
    print "上位实体"
    print_value(entity_resp.column_names, entity_resp.rows)
    print "同义实体"
    print_value(synonym_resp.column_names, synonym_resp.rows)

    # json 输出
    # json_value(synonym_resp.rows)

    concept_resp, entity_resp = nebula.getCommonEntityConcept(name, type)
    print "概念"
    print_value(concept_resp.column_names, concept_resp.rows)
    print "上位实体"
    print_value(entity_resp.column_names, entity_resp.rows)




