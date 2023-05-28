# import categories
import Brand_category
import data_extract_one_profile as usersdata


#print(data.dictUN)

for key in Brand_category.dictUN:

        for j in range(len(Brand_category.dictUN[key])):

            user = Brand_category.dictUN[key][j]
            usersdata.getData(user)