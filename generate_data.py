# DMQL Project Data creation script
import json
import random


def generate_data(conf_path, output_path):
    with open(conf_path, encoding='utf-8') as f:
        conf = json.load(f)

    print("Config successfully loaded")
    tables = conf["tables"]
    ptrns = conf["patterns"]
    tbl_keys = list(tables.keys())
    tbl_keys.append("orderitems")

    for table in tbl_keys:
        tbl = tables[table]
        iter = [col for col in tbl.keys() if "iterator" in tbl[col]][0]  # set iter to primary key col
        iter_range = list(map(int, tbl[iter][9:-1].split(",")))  # parse lower & upper limit of range
        num_of_records = len(range(*iter_range))
        print(f"Creating {num_of_records} records for table {table}")

        statements = []
        for i in range(*iter_range):
            insert_st = f"insert into {table} values({i}, "  # create insert statement
            for col in tbl.keys():
                if col == iter:  # primary key
                    continue
                elif tbl[col][0:6] == "range(":  # range valued columns
                    temp_rng = list(map(int, tbl[col][6:-1].split(","))) # parse lower & upper limit of range
                    insert_st += str(random.randint(*temp_rng)) + ", "

                else:  # generate value acc to pattern
                    if col in ('email','contact_no', 'address', 'website') and random.random() < 0.1:
                        insert_st += "NULL, "
                        continue

                    if tbl[col] not in ptrns:  # error handling
                        raise Exception(f"Col {col} pattern {tbl[col]} not in patterns")

                    ptrn = ptrns[tbl[col]]

                    if type(ptrn) == type([1, 2]):  # pattern is list of choices
                        if "name" in col:
                            name = random.choice(ptrns[tbl[col]])
                            insert_st += "'" + name + "', "
                            name = ''.join(e.lower() for e in name if e.isalnum())
                        else:
                            insert_st += "'" + random.choice(ptrns[tbl[col]]) + "', "

                    elif type(ptrn) == type("abc"):  # pattern is string
                        if "f'" in ptrn:  # fstring
                            insert_st += "'" + eval(ptrn) + "', "
                        elif ptrn == "phone":  # generate random phone number
                            insert_st += "".join([str(random.randrange(10)) for i in range(10)]) + ", "

                    else:
                        raise Exception("Pattern not decoded")

            insert_st = insert_st[:-2] + ");"
            statements.append(insert_st)
        # write to file
        with open(output_path, 'a+', encoding='utf-8') as f:
            f.write("\n".join(statements))
    return 1


generate_data("conf.json", "load.sql")


