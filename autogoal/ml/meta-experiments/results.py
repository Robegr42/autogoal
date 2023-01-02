from tools import get_best_fn, from_str_to_dict, extract, get_first_best_pos, get_list_tuple
from statistics import mean, median
import os

def print_result(p,pgemean, pgemedian, k10mean, k10median, k25mean, k25median, k50mean, k50median):

    print(f"\n----P{p}----")
    print(f"P{p} PGE MEAN BEST FITNESS ITERATION: {pgemean}")
    print(f"P{p} PGE MEDIAN BEST FITNESS ITERATION: {pgemedian}")
    print(f"P{p} META MEAN BEST FITNESS ITERATION WITH K = 10: {k10mean}")
    print(f"P{p} META MEDIAN BEST FITNESS ITERATION WITH K = 10: {k10median}")
    print(f"P{p} META MEAN BEST FITNESS ITERATION WITH K = 25: {k25mean}", )
    print(f"P{p} META MEDIAN BEST FITNESS ITERATION WITH K = 25: {k25median}")
    print(f"P{p} META MEAN BEST FITNESS ITERATION WITH K = 50: {k50mean}")
    print(f"P{p} META MEDIAN BEST FITNESS ITERATION WITH K = 50: {k50median}")


#region First Problems

print("-"*15 + "First Problems" + "-"*15)

#region P1PGE

p1_PGE_logs = []
p1_PGE_files = list(os.walk("PGE/P1/"))[0][2]
p1_PGE = []

for i in p1_PGE_files:
    for j in from_str_to_dict(extract("PGE/P1/"+i)):
        p1_PGE_logs.append(j)
    p1_PGE.append(get_best_fn(p1_PGE_logs))
    p1_PGE_logs.clear()

p1_PGE_mean = mean(get_list_tuple(p1_PGE,1))
p1_PGE_median = median(get_list_tuple(p1_PGE,1))


#endregion

#region P2PGE

p2_PGE_logs = []
p2_PGE_files = list(os.walk("PGE/P2/"))[0][2]
p2_PGE = []

for i in p2_PGE_files:
    for j in from_str_to_dict(extract("PGE/P2/"+i)):
        p2_PGE_logs.append(j)
    p2_PGE.append(get_best_fn(p2_PGE_logs))
    p2_PGE_logs.clear()

p2_PGE_mean = mean(get_list_tuple(p2_PGE,1))
p2_PGE_median = median(get_list_tuple(p2_PGE,1))

#endregion

#region P3PGE

p3_PGE_logs = []
p3_PGE_files = list(os.walk("PGE/P3/"))[0][2]
p3_PGE = []

for i in p3_PGE_files:
    for j in from_str_to_dict(extract("PGE/P3/"+i)):
        p3_PGE_logs.append(j)
    p3_PGE.append(get_best_fn(p3_PGE_logs))
    p3_PGE_logs.clear()

p3_PGE_mean = mean(get_list_tuple(p3_PGE,1))
p3_PGE_median = median(get_list_tuple(p3_PGE,1))

#endregion

#region P4PGE

p4_PGE_logs = []
p4_PGE_files = list(os.walk("PGE/P4/"))[0][2]
p4_PGE = []

for i in p4_PGE_files:
    for j in from_str_to_dict(extract("PGE/P4/"+i)):
        p4_PGE_logs.append(j)
    p4_PGE.append(get_best_fn(p4_PGE_logs))
    p4_PGE_logs.clear()

p4_PGE_mean = mean(get_list_tuple(p4_PGE,1))
p4_PGE_median = median(get_list_tuple(p4_PGE,1))

#endregion

#region P1META_K10

p1_META_K10_logs = []
p1_META_10_files = list(os.walk("TRAINING_LOGS_10/P1/"))[0][2]
p1_META_K10 = []

for i in p1_META_10_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_10/P1/"+i)):
        p1_META_K10_logs.append(j)
    p1_META_K10.append(get_first_best_pos(10,p1_META_K10_logs))
    p1_META_K10_logs.clear()

p1_META_K10_mean = mean(p1_META_K10)
p1_META_K10_median = median(p1_META_K10)


#endregion

#region P2META_K10

p2_META_K10_logs = []
p2_META_10_files = list(os.walk("TRAINING_LOGS_10/P2/"))[0][2]
p2_META_K10 = []

for i in p2_META_10_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_10/P2/"+i)):
        p2_META_K10_logs.append(j)
    p2_META_K10.append(get_first_best_pos(10, p2_META_K10_logs))
    p2_META_K10_logs.clear()

p2_META_K10_mean = mean(p2_META_K10)
p2_META_K10_median = median(p2_META_K10)


#endregion

#region P3META_K10

p3_META_K10_logs = []
p3_META_10_files = list(os.walk("TRAINING_LOGS_10/P3/"))[0][2]
p3_META_K10 = []

for i in p3_META_10_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_10/P3/"+i)):
        p3_META_K10_logs.append(j)
    p3_META_K10.append(get_first_best_pos(10,p3_META_K10_logs))
    p3_META_K10_logs.clear()

p3_META_K10_mean = mean(p3_META_K10)
p3_META_K10_median = median(p3_META_K10)


#endregion

#region P4META_K10

p4_META_K10_logs = []
p4_META_10_files = list(os.walk("TRAINING_LOGS_10/P4/"))[0][2]
p4_META_K10 = []

for i in p4_META_10_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_10/P4/"+i)):
        p4_META_K10_logs.append(j)
    p4_META_K10.append(get_first_best_pos(10,p4_META_K10_logs))
    p4_META_K10_logs.clear()

p4_META_K10_mean = mean(p4_META_K10)
p4_META_K10_median = median(p4_META_K10)


#endregion

#region P1META_K25

p1_META_K25_logs = []
p1_META_25_files = list(os.walk("TRAINING_LOGS_25/P1/"))[0][2]
p1_META_K25 = []

for i in p1_META_25_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_25/P1/"+i)):
        p1_META_K25_logs.append(j)
    p1_META_K25.append(get_first_best_pos(25,p1_META_K25_logs))
    p1_META_K25_logs.clear()

p1_META_K25_mean = mean(p1_META_K25)
p1_META_K25_median = median(p1_META_K25)


#endregion

#region P2META_K25

p2_META_K25_logs = []
p2_META_25_files = list(os.walk("TRAINING_LOGS_25/P2/"))[0][2]
p2_META_K25 = []

for i in p2_META_25_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_25/P2/"+i)):
        p2_META_K25_logs.append(j)
    p2_META_K25.append(get_first_best_pos(25,p2_META_K25_logs))
    p2_META_K25_logs.clear()

p2_META_K25_mean = mean(p2_META_K25)
p2_META_K25_median = median(p2_META_K25)


#endregion

#region P3META_K25

p3_META_K25_logs = []
p3_META_25_files = list(os.walk("TRAINING_LOGS_25/P3/"))[0][2]
p3_META_K25 = []

for i in p3_META_25_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_25/P3/"+i)):
        p3_META_K25_logs.append(j)
    p3_META_K25.append(get_first_best_pos(25,p3_META_K25_logs))
    p3_META_K25_logs.clear()

p3_META_K25_mean = mean(p3_META_K25)
p3_META_K25_median = median(p3_META_K25)


#endregion

#region P4META_K25

p4_META_K25_logs = []
p4_META_25_files = list(os.walk("TRAINING_LOGS_25/P4/"))[0][2]
p4_META_K25 = []

for i in p4_META_25_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_25/P4/"+i)):
        p4_META_K25_logs.append(j)
    p4_META_K25.append(get_first_best_pos(25,p4_META_K25_logs))
    p4_META_K25_logs.clear()

p4_META_K25_mean = mean(p4_META_K25)
p4_META_K25_median = median(p4_META_K25)


#endregion

#region P1META_K50

p1_META_K50_logs = []
p1_META_50_files = list(os.walk("TRAINING_LOGS_50/P1/"))[0][2]
p1_META_K50 = []

for i in p1_META_50_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_50/P1/"+i)):
        p1_META_K50_logs.append(j)
    p1_META_K50.append(get_first_best_pos(50,p1_META_K50_logs))
    p1_META_K50_logs.clear()

p1_META_K50_mean = mean(p1_META_K50)
p1_META_K50_median = median(p1_META_K50)


#endregion

#region P2META_K50

p2_META_K50_logs = []
p2_META_50_files = list(os.walk("TRAINING_LOGS_50/P2/"))[0][2]
p2_META_K50 = []

for i in p2_META_50_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_50/P2/"+i)):
        p2_META_K50_logs.append(j)
    p2_META_K50.append(get_first_best_pos(50,p2_META_K50_logs))
    p2_META_K50_logs.clear()

p2_META_K50_mean = mean(p2_META_K50)
p2_META_K50_median = median(p2_META_K50)


#endregion

#region P3META_K50

p3_META_K50_logs = []
p3_META_50_files = list(os.walk("TRAINING_LOGS_50/P3/"))[0][2]
p3_META_K50 = []

for i in p3_META_50_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_50/P3/"+i)):
        p3_META_K50_logs.append(j)
    p3_META_K50.append(get_first_best_pos(50,p3_META_K50_logs))
    p3_META_K50_logs.clear()

p3_META_K50_mean = mean(p3_META_K50)
p3_META_K50_median = median(p3_META_K50)


#endregion

#region P4META_K50

p4_META_K50_logs = []
p4_META_50_files = list(os.walk("TRAINING_LOGS_50/P4/"))[0][2]
p4_META_K50 = []

for i in p4_META_50_files:
    for j in from_str_to_dict(extract("TRAINING_LOGS_50/P4/"+i)):
        p4_META_K50_logs.append(j)
    p4_META_K50.append(get_first_best_pos(50,p4_META_K50_logs))
    p4_META_K50_logs.clear()

p4_META_K50_mean = mean(p4_META_K50)
p4_META_K50_median = median(p4_META_K50)

#endregion


print_result(1, p1_PGE_mean, p1_PGE_median, p1_META_K10_mean, p1_META_K10_median, p1_META_K25_mean, p1_META_K25_median, p1_META_K50_mean, p1_META_K10_median)

print_result(2, p2_PGE_mean, p2_PGE_median, p2_META_K10_mean, p2_META_K10_median, p2_META_K25_mean, p2_META_K25_median, p2_META_K50_mean, p2_META_K10_median)

print_result(3, p3_PGE_mean, p3_PGE_median, p3_META_K10_mean, p3_META_K10_median, p3_META_K25_mean, p3_META_K25_median, p3_META_K50_mean, p3_META_K10_median)

print_result(4, p4_PGE_mean, p4_PGE_median, p4_META_K10_mean, p4_META_K10_median, p4_META_K25_mean, p4_META_K25_median, p4_META_K50_mean, p4_META_K10_median)

print("\n")
print("-"*15 + "New Problems" + "-"*15)


#region NEW_P1PGE

p1_PGE_logs = []
p1_PGE_files = list(os.walk("NEW_TEST_PGE/P1/"))[0][2]
p1_PGE = []

for i in p1_PGE_files:
    for j in from_str_to_dict(extract("NEW_TEST_PGE/P1/"+i)):
        p1_PGE_logs.append(j)
    p1_PGE.append(get_best_fn(p1_PGE_logs))
    p1_PGE_logs.clear()

p1_PGE_mean = mean(get_list_tuple(p1_PGE,1))
p1_PGE_median = median(get_list_tuple(p1_PGE,1))


#endregion

#region NEW_P2PGE

p2_PGE_logs = []
p2_PGE_files = list(os.walk("NEW_TEST_PGE/P2/"))[0][2]
p2_PGE = []

for i in p2_PGE_files:
    for j in from_str_to_dict(extract("NEW_TEST_PGE/P2/"+i)):
        p2_PGE_logs.append(j)
    p2_PGE.append(get_best_fn(p2_PGE_logs))
    p2_PGE_logs.clear()

p2_PGE_mean = mean(get_list_tuple(p2_PGE,1))
p2_PGE_median = median(get_list_tuple(p2_PGE,1))

#endregion

#region NEW_P3PGE

p3_PGE_logs = []
p3_PGE_files = list(os.walk("NEW_TEST_PGE/P3/"))[0][2]
p3_PGE = []

for i in p3_PGE_files:
    for j in from_str_to_dict(extract("NEW_TEST_PGE/P3/"+i)):
        p3_PGE_logs.append(j)
    p3_PGE.append(get_best_fn(p3_PGE_logs))
    p3_PGE_logs.clear()

p3_PGE_mean = mean(get_list_tuple(p3_PGE,1))
p3_PGE_median = median(get_list_tuple(p3_PGE,1))

#endregion

#region NEW_P4PGE

p4_PGE_logs = []
p4_PGE_files = list(os.walk("NEW_TEST_PGE/P4/"))[0][2]
p4_PGE = []

for i in p4_PGE_files:
    for j in from_str_to_dict(extract("NEW_TEST_PGE/P4/"+i)):
        p4_PGE_logs.append(j)
    p4_PGE.append(get_best_fn(p4_PGE_logs))
    p4_PGE_logs.clear()

p4_PGE_mean = mean(get_list_tuple(p4_PGE,1))
p4_PGE_median = median(get_list_tuple(p4_PGE,1))

#endregion

#region NEW_P1META_K10

p1_META_K10_logs = []
p1_META_10_files = list(os.walk("TEST_META_10/P1/"))[0][2]
p1_META_K10 = []

for i in p1_META_10_files:
    for j in from_str_to_dict(extract("TEST_META_10/P1/"+i)):
        p1_META_K10_logs.append(j)
    p1_META_K10.append(get_first_best_pos(10,p1_META_K10_logs))
    p1_META_K10_logs.clear()

p1_META_K10_mean = mean(p1_META_K10)
p1_META_K10_median = median(p1_META_K10)


#endregion

#region NEW_P2META_K10

p2_META_K10_logs = []
p2_META_10_files = list(os.walk("TEST_META_10/P2/"))[0][2]
p2_META_K10 = []

for i in p2_META_10_files:
    for j in from_str_to_dict(extract("TEST_META_10/P2/"+i)):
        p2_META_K10_logs.append(j)
    p2_META_K10.append(get_first_best_pos(10, p2_META_K10_logs))
    p2_META_K10_logs.clear()

p2_META_K10_mean = mean(p2_META_K10)
p2_META_K10_median = median(p2_META_K10)


#endregion

#region NEW_P3META_K10

p3_META_K10_logs = []
p3_META_10_files = list(os.walk("TEST_META_10/P3/"))[0][2]
p3_META_K10 = []

for i in p3_META_10_files:
    for j in from_str_to_dict(extract("TEST_META_10/P3/"+i)):
        p3_META_K10_logs.append(j)
    p3_META_K10.append(get_first_best_pos(10,p3_META_K10_logs))
    p3_META_K10_logs.clear()

p3_META_K10_mean = mean(p3_META_K10)
p3_META_K10_median = median(p3_META_K10)


#endregion

#region NEW_P4META_K10

p4_META_K10_logs = []
p4_META_10_files = list(os.walk("TEST_META_10/P4/"))[0][2]
p4_META_K10 = []

for i in p4_META_10_files:
    for j in from_str_to_dict(extract("TEST_META_10/P4/"+i)):
        p4_META_K10_logs.append(j)
    p4_META_K10.append(get_first_best_pos(10,p4_META_K10_logs))
    p4_META_K10_logs.clear()

p4_META_K10_mean = mean(p4_META_K10)
p4_META_K10_median = median(p4_META_K10)


#endregion

#region NEW_P1META_K25

p1_META_K25_logs = []
p1_META_25_files = list(os.walk("TEST_META_25/P1/"))[0][2]
p1_META_K25 = []

for i in p1_META_25_files:
    for j in from_str_to_dict(extract("TEST_META_25/P1/"+i)):
        p1_META_K25_logs.append(j)
    p1_META_K25.append(get_first_best_pos(25,p1_META_K25_logs))
    p1_META_K25_logs.clear()

p1_META_K25_mean = mean(p1_META_K25)
p1_META_K25_median = median(p1_META_K25)


#endregion

#region NEW_P2META_K25

p2_META_K25_logs = []
p2_META_25_files = list(os.walk("TEST_META_25/P2/"))[0][2]
p2_META_K25 = []

for i in p2_META_25_files:
    for j in from_str_to_dict(extract("TEST_META_25/P2/"+i)):
        p2_META_K25_logs.append(j)
    p2_META_K25.append(get_first_best_pos(25,p2_META_K25_logs))
    p2_META_K25_logs.clear()

p2_META_K25_mean = mean(p2_META_K25)
p2_META_K25_median = median(p2_META_K25)


#endregion

#region NEW_P3META_K25

p3_META_K25_logs = []
p3_META_25_files = list(os.walk("TEST_META_25/P3/"))[0][2]
p3_META_K25 = []

for i in p3_META_25_files:
    for j in from_str_to_dict(extract("TEST_META_25/P3/"+i)):
        p3_META_K25_logs.append(j)
    p3_META_K25.append(get_first_best_pos(25,p3_META_K25_logs))
    p3_META_K25_logs.clear()

p3_META_K25_mean = mean(p3_META_K25)
p3_META_K25_median = median(p3_META_K25)


#endregion

#region NEW_P4META_K25

p4_META_K25_logs = []
p4_META_25_files = list(os.walk("TEST_META_25/P4/"))[0][2]
p4_META_K25 = []

for i in p4_META_25_files:
    for j in from_str_to_dict(extract("TEST_META_25/P4/"+i)):
        p4_META_K25_logs.append(j)
    p4_META_K25.append(get_first_best_pos(25,p4_META_K25_logs))
    p4_META_K25_logs.clear()

p4_META_K25_mean = mean(p4_META_K25)
p4_META_K25_median = median(p4_META_K25)


#endregion

#region NEW_P1META_K50

p1_META_K50_logs = []
p1_META_50_files = list(os.walk("TEST_META_50/P1/"))[0][2]
p1_META_K50 = []

for i in p1_META_50_files:
    for j in from_str_to_dict(extract("TEST_META_50/P1/"+i)):
        p1_META_K50_logs.append(j)
    p1_META_K50.append(get_first_best_pos(50,p1_META_K50_logs))
    p1_META_K50_logs.clear()

p1_META_K50_mean = mean(p1_META_K50)
p1_META_K50_median = median(p1_META_K50)


#endregion

#region NEW_P2META_K50

p2_META_K50_logs = []
p2_META_50_files = list(os.walk("TEST_META_50/P2/"))[0][2]
p2_META_K50 = []

for i in p2_META_50_files:
    for j in from_str_to_dict(extract("TEST_META_50/P2/"+i)):
        p2_META_K50_logs.append(j)
    p2_META_K50.append(get_first_best_pos(50,p2_META_K50_logs))
    p2_META_K50_logs.clear()

p2_META_K50_mean = mean(p2_META_K50)
p2_META_K50_median = median(p2_META_K50)


#endregion

#region NEW_P3META_K50

p3_META_K50_logs = []
p3_META_50_files = list(os.walk("TEST_META_50/P3/"))[0][2]
p3_META_K50 = []

for i in p3_META_50_files:
    for j in from_str_to_dict(extract("TEST_META_50/P3/"+i)):
        p3_META_K50_logs.append(j)
    p3_META_K50.append(get_first_best_pos(50,p3_META_K50_logs))
    p3_META_K50_logs.clear()

p3_META_K50_mean = mean(p3_META_K50)
p3_META_K50_median = median(p3_META_K50)


#endregion

#region NEW_P4META_K50

p4_META_K50_logs = []
p4_META_50_files = list(os.walk("TEST_META_50/P4/"))[0][2]
p4_META_K50 = []

for i in p4_META_50_files:
    for j in from_str_to_dict(extract("TEST_META_50/P4/"+i)):
        p4_META_K50_logs.append(j)
    p4_META_K50.append(get_first_best_pos(50,p4_META_K50_logs))
    p4_META_K50_logs.clear()

p4_META_K50_mean = mean(p4_META_K50)
p4_META_K50_median = median(p4_META_K50)

#endregion


print_result(1, p1_PGE_mean, p1_PGE_median, p1_META_K10_mean, p1_META_K10_median, p1_META_K25_mean, p1_META_K25_median, p1_META_K50_mean, p1_META_K10_median)

print_result(2, p2_PGE_mean, p2_PGE_median, p2_META_K10_mean, p2_META_K10_median, p2_META_K25_mean, p2_META_K25_median, p2_META_K50_mean, p2_META_K10_median)

print_result(3, p3_PGE_mean, p3_PGE_median, p3_META_K10_mean, p3_META_K10_median, p3_META_K25_mean, p3_META_K25_median, p3_META_K50_mean, p3_META_K10_median)

print_result(4, p4_PGE_mean, p4_PGE_median, p4_META_K10_mean, p4_META_K10_median, p4_META_K25_mean, p4_META_K25_median, p4_META_K50_mean, p4_META_K10_median)
