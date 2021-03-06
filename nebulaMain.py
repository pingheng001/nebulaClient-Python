# -*- coding:utf-8 -*-

# from nebula.graph import ttypes
# from nebula.ConnectionPool import ConnectionPool
# from nebula.Client import GraphClient
from nebula2.gclient.net import ConnectionPool
from nebula2.graph import ttypes
from nebula2.Config import Config
import prettytable
import json


def print_resp(resp):
    assert resp.is_succeeded()
    output_table = prettytable.PrettyTable()
    output_table.field_names = resp.keys()
    for recode in resp:
        value_list = []
        for col in recode:
            if col.is_empty():
                value_list.append('__EMPTY__')
            elif col.is_null():
                value_list.append('__NULL__')
            elif col.is_bool():
                value_list.append(col.as_bool())
            elif col.is_int():
                value_list.append(col.as_int())
            elif col.is_double():
                value_list.append(col.as_double())
            elif col.is_string():
                value_list.append(col.as_string())
            elif col.is_time():
                value_list.append(col.as_time())
            elif col.is_date():
                value_list.append(col.as_date())
            elif col.is_datetime():
                value_list.append(col.as_datetime())
            elif col.is_list():
                value_list.append(col.as_list())
            elif col.is_set():
                value_list.append(col.as_set())
            elif col.is_map():
                value_list.append(col.as_map())
            elif col.is_vertex():
                value_list.append(col.as_node())
            elif col.is_edge():
                value_list.append(col.as_relationship())
            elif col.is_path():
                value_list.append(col.as_path())
            else:
                print('ERROR: Type unsupported')
                return
        output_table.add_row(value_list)
    print(output_table)

def json_value(resp):
    all_values = []
    assert resp.is_succeeded()
    for recode in resp:
        value_list = []
        for col in recode:
            if col.is_empty():
                value_list.append('__EMPTY__')
            elif col.is_null():
                value_list.append('__NULL__')
            elif col.is_bool():
                value_list.append(col.as_bool())
            elif col.is_int():
                value_list.append(col.as_int())
            elif col.is_double():
                value_list.append(col.as_double())
            elif col.is_string():
                value_list.append(col.as_string())
            elif col.is_time():
                value_list.append(col.as_time())
            elif col.is_date():
                value_list.append(col.as_date())
            elif col.is_datetime():
                value_list.append(col.as_datetime())
            elif col.is_list():
                value_list.append(col.as_list())
            elif col.is_set():
                value_list.append(col.as_set())
            elif col.is_map():
                value_list.append(col.as_map())
            elif col.is_vertex():
                value_list.append(col.as_node())
            elif col.is_edge():
                value_list.append(col.as_relationship())
            elif col.is_path():
                value_list.append(col.as_path())
            else:
                print('ERROR: Type unsupported')
                return
        all_values.append(value_list)
    return json.dumps(all_values, ensure_ascii=False)

class Nebula:
    '''
    Nebula Python ?????????
    '''
    def __init__(self):
        # define a config
        config = Config()
        config.max_connection_pool_size = 10
        # init connection pool
        connection_pool = ConnectionPool()
        # if the given servers are ok, return true, else return false
        ok = connection_pool.init([('10.141.186.105', 3699)], config)

        # option 1 control the connection release yourself
        # get session from the pool
        self.session = connection_pool.get_session('root', 'nebula')

        # select space
        self.session.execute('USE adeci_test')

        # show tags
        # result = self.session.execute('SHOW TAGS')
        # print(result)

    def __del__(self):
        self.session.release()

    def getEntityConcept(self, name, type, steps=1, limit=-1):
        '''
        # ?????????????????????+??????????????????????????????????????????????????????
        :param name:
        :param type:
        :param steps:???????????????
        :param limit:?????????????????????
        :return:
        '''
        executeStr = 'LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO 1 TO {} STEPS FROM $-.VertexID OVER isA WHERE length($$.concept.name) != 0 YIELD \
            DISTINCT $-.name as name, $$.concept.name as conceptName'.format(name, type, steps)
        if limit >= 1:
            executeStr += "| LIMIT {};".format(limit)
        else:
            executeStr += ";"
        # ??????
        concept_resp = self.session.execute(executeStr)

        return concept_resp

    def getEntityUpEntity(self, name, type, steps=1, limit=-1):
        # ?????????????????????+????????????????????????????????????????????????????????????
        # ????????????
        executeStr = 'LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO 1 TO {} STEPS FROM $-.VertexID OVER isA WHERE length($$.entity.name) != 0 YIELD \
            DISTINCT $-.name as name, $$.entity.name as entityName'.format(name, type, steps)
        if limit >= 1:
            executeStr += "| LIMIT {};".format(limit)
        else:
            executeStr += ";"
        entity_resp = self.session.execute(executeStr)
        return entity_resp

    def getEntitySonEntity(self, name, type, steps=1, limit=-1):
        # ?????????????????????+????????????????????????????????????????????????????????????
        # ????????????
        executeStr = 'LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO 1 TO {} STEPS FROM $-.VertexID OVER synonym YIELD DISTINCT $-.name as name, \
            $$.entity.name as entityName'.format(name, type, steps)
        if limit >= 1:
            executeStr += "| LIMIT {};".format(limit)
        else:
            executeStr += ";"
        synonym_resp = self.session.execute(executeStr)
        return synonym_resp

    def getCommonConceptEntity(self, name, type, steps=1, limit=-1):
        '''
        # ?????????????????????+??????????????????????????????????????????????????????????????????
        :param name:
        :param type:
        :param steps:???????????????
        :param limit:?????????????????????
        :return:
        '''
        executeStr = 'LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO 1 TO {} STEPS FROM $-.VertexID OVER isA WHERE length($$.concept.name) != 0 YIELD \
            DISTINCT $-.name as name, $$.concept.name as conceptName, isA._dst as id | GO FROM $-.id OVER isA REVERSELY\
             YIELD DISTINCT $-.conceptName as name, $$.entity.name as commonName'.format(name, type, steps)
        if limit >= 1:
            executeStr += "| LIMIT {};".format(limit)
        else:
            executeStr += ";"
        # ??????
        concept_resp = self.session.execute(executeStr)

        return concept_resp

    def getCommonUpEntity(self, name, type, steps=1, limit=-1):
        # ?????????????????????+??????????????????????????????????????????????????????????????????????????????
        # ????????????
        executeStr = 'LOOKUP ON entity WHERE entity.name == "{}" AND entity.type == "{}" YIELD \
            entity.name AS name | GO 1 TO {} STEPS FROM $-.VertexID OVER isA WHERE length($$.entity.name) != 0 YIELD \
            DISTINCT $-.name as name, $$.entity.name as entityName, isA._dst as id | GO FROM $-.id OVER isA REVERSELY \
            YIELD DISTINCT $-.entityName as name, $$.entity.name as commonName'.format(name, type, steps)
        if limit >= 1:
            executeStr += "| LIMIT {};".format(limit)
        else:
            executeStr += ";"
        entity_resp = self.session.execute(executeStr)
        return entity_resp


if __name__ == "__main__":
    name = "????????????"
    type = "PRODUCT"
    # name = "??????"
    # type = "PLACE"

    nebula = Nebula()

    concept_resp = nebula.getEntityConcept(name, type, steps=3)
    entity_resp = nebula.getEntityUpEntity(name, type)
    synonym_resp = nebula.getEntitySonEntity(name, type)

    print("??????")
    print_resp(concept_resp)
    print("????????????")
    print_resp(entity_resp)
    print("????????????")
    print_resp(synonym_resp)

    # json ??????
    print(json_value(concept_resp))

    concept_resp = nebula.getCommonConceptEntity(name, type, steps=3, limit=10)
    entity_resp = nebula.getCommonUpEntity(name, type, limit=10)
    # concept_resp, entity_resp = nebula.getCommonEntityConcept(name, type, steps=3, limit=2000)
    print("??????")
    print_resp(concept_resp)
    print("????????????")
    print_resp(entity_resp)




