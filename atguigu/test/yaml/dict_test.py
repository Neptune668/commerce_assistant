dict_data = {
    "id": "flow_1",
    "description": "这是第一个流程"
}

dict_data2 = {
    "id": "flow_1"
}


set_data = set(dict_data)
print(set_data.intersection(dict_data2))