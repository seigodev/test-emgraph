from collections import defaultdict
import os
import glob
import re
import pprint
import json

def get_mml_version():
    cwd = os.getcwd()
    try:
        os.chdir("mml")
        mml_version = glob.glob("**/", recursive=True)
    finally:
        os.chdir(cwd)
    mml_version = [re.sub("/", "", version) for version in mml_version ]
    mml_version.remove("2003-12-24")
    mml_version.remove("2005-05-31")

    return sorted(mml_version)


def get_ranking_auth_minus_pagerank_txt():
    cwd = os.getcwd()
    try:
        os.chdir("result_pagerank_auth")
        ranking_auth_minus_pagerank_txt = glob.glob('*.txt')
    finally:
        os.chdir(cwd)

    ranking_auth_minus_pagerank_txt.remove('MML(2003-12-24)_auth_minus_pagerank.txt')
    ranking_auth_minus_pagerank_txt.remove('MML(2005-05-31)_auth_minus_pagerank.txt')

    return sorted(ranking_auth_minus_pagerank_txt)


def find_article_required_refactoring():
    node2ranking_each_mml_version = dict()
    ranking_auth_minus_pagerank_txt = get_ranking_auth_minus_pagerank_txt()
    for txt in ranking_auth_minus_pagerank_txt:
        with open(os.path.join("result_pagerank_auth/", txt), 'rt',
                  encoding='utf-8', errors="ignore") as f:
            node_and_value = f.readlines()
            node2ranking = dict()
            ranking = 1
            for v in node_and_value:
                n = v.split()
                node2ranking[n[0]] = ranking
                ranking += 1
            version = txt[4:14]
        node2ranking_each_mml_version[version] = node2ranking

    node2displacement_between_two_version_ranking_down = \
        calc_displacement_between_two_version_ranking_down(node2ranking_each_mml_version)
    with open("research_data/displacement/displacement_between_two_version_ranking_down.txt", "w") as f:
        f.write(pprint.pformat(sorted(node2displacement_between_two_version_ranking_down.items(), 
                                      key=lambda x:x[1], reverse=False)))

    node2displacement_between_two_version_ranking_up = \
        calc_displacement_between_two_version_ranking_up(node2ranking_each_mml_version)
    with open("research_data/displacement/displacement_between_two_version_ranking_up.txt", "w") as f:
        f.write(pprint.pformat(sorted(node2displacement_between_two_version_ranking_up.items(), 
                                      key=lambda x:x[1], reverse=False)))

    node2displacement_in_all_version_ranking_down = \
        calc_displacement_in_all_version_ranking_down(node2ranking_each_mml_version)
    for k in node2displacement_in_all_version_ranking_down.keys():
        node2displacement_in_all_version_ranking_down[k]["old_ver"] = node2displacement_in_all_version_ranking_down[k]["min_ver"]
        node2displacement_in_all_version_ranking_down[k]["new_ver"] = node2displacement_in_all_version_ranking_down[k]["max_ver"]
        del(node2displacement_in_all_version_ranking_down[k]["min_ver"])
        del(node2displacement_in_all_version_ranking_down[k]["max_ver"])
    with open("research_data/displacement/displacement_in_all_version_ranking_down.txt", "w") as f:
        f.write(pprint.pformat(sorted(node2displacement_in_all_version_ranking_down.items(),
                                      key=lambda x:x[1]["score"], reverse=False)))
    with open("research_data/displacement/displacement_in_all_version_ranking_down.json", "w") as f:
        f.write(json.dumps(node2displacement_in_all_version_ranking_down, indent=4))

    node2displacement_in_all_version_ranking_up = \
        calc_displacement_in_all_version_ranking_up(node2ranking_each_mml_version)
    for k in node2displacement_in_all_version_ranking_up.keys():
        node2displacement_in_all_version_ranking_up[k]["old_ver"] = node2displacement_in_all_version_ranking_up[k]["max_ver"]
        node2displacement_in_all_version_ranking_up[k]["new_ver"] = node2displacement_in_all_version_ranking_up[k]["min_ver"]
        del(node2displacement_in_all_version_ranking_up[k]["max_ver"])
        del(node2displacement_in_all_version_ranking_up[k]["min_ver"])
    with open("research_data/displacement/displacement_in_all_version_ranking_up.txt", "w") as f:
        f.write(pprint.pformat(sorted(node2displacement_in_all_version_ranking_up.items(),
                                      key=lambda x:x[1]["score"], reverse=True)))
    with open("research_data/displacement/displacement_in_all_version_ranking_up.json", "w") as f:
        f.write(json.dumps(node2displacement_in_all_version_ranking_up, indent=4))


def calc_displacement_between_two_version_ranking_down(node2ranking_each_mml_version):
    mml_version = get_mml_version()
    node2score = dict()
    for i in range(len(mml_version)-1):
        current_version = mml_version[i]
        next_version = mml_version[i+1]
        for k,v in node2ranking_each_mml_version[current_version].items():
            if not k in node2score.keys():
                node2score[k] = 0
            if k in node2ranking_each_mml_version[next_version].keys():
                node2score[k] = min(node2score[k], v - node2ranking_each_mml_version[next_version][k])

    return node2score


def calc_displacement_between_two_version_ranking_up(node2ranking_each_mml_version):
    mml_version = sorted(get_mml_version(), reverse=True)
    node2score = dict()
    for i in range(len(mml_version)-1):
        current_version = mml_version[i]
        old_version = mml_version[i+1]
        for k,v in node2ranking_each_mml_version[current_version].items():
            if not k in node2score.keys():
                node2score[k] = 0
            if k in node2ranking_each_mml_version[old_version].keys():
                node2score[k] = min(node2score[k], v - node2ranking_each_mml_version[old_version][k])

    return node2score


def calc_displacement_in_all_version_ranking_down(node2ranking_each_mml_version):
    node2ranking = dict()
    node2score = dict()

    for version in node2ranking_each_mml_version.keys():
        for k,v in node2ranking_each_mml_version[version].items():
            if not k in node2ranking.keys():
                node2ranking[k] = dict()
                node2ranking[k][0] = dict()
                node2ranking[k][0]["min"] = v
                node2ranking[k][0]["min_ver"] = version
                node2ranking[k][0]["max"] = v
                node2ranking[k][0]["max_ver"] = version
            else:
                key_max = max(node2ranking[k].keys())
                if v < node2ranking[k][key_max]["min"]:
                    node2ranking[k][key_max + 1] = dict()
                    node2ranking[k][key_max + 1]["min"] = v
                    node2ranking[k][key_max + 1]["min_ver"] = version
                    node2ranking[k][key_max + 1]["max"] = v
                    node2ranking[k][key_max + 1]["max_ver"] = version
                else:
                    if v > node2ranking[k][key_max]["max"]:
                        node2ranking[k][key_max]["max"] = v
                        node2ranking[k][key_max]["max_ver"] = version
    
    for k in node2ranking.keys():
        for i in node2ranking[k].keys():
            for j in range(i, len(node2ranking[k].keys())):
                if not k in node2score.keys():
                    node2score[k] = dict()
                    node2score[k]["score"] = node2ranking[k][i]["min"] - node2ranking[k][j]["max"]
                    node2score[k]["min_ver"] = node2ranking[k][i]["min_ver"]
                    node2score[k]["max_ver"] = node2ranking[k][i]["max_ver"]
                else:
                    if node2score[k]["score"] > (node2ranking[k][i]["min"] - node2ranking[k][j]["max"]):
                        node2score[k]["score"] = node2ranking[k][i]["min"] - node2ranking[k][j]["max"]
                        node2score[k]["min_ver"] = node2ranking[k][i]["min_ver"]
                        node2score[k]["max_ver"] = node2ranking[k][j]["max_ver"]
    return node2score


def calc_displacement_in_all_version_ranking_up(node2ranking_each_mml_version):
    node2ranking = dict()
    node2score = dict()
    mml_version_reversed = sorted(get_mml_version(), reverse=True)

    for version in mml_version_reversed:
        for k,v in node2ranking_each_mml_version[version].items():
            if not k in node2ranking.keys():
                node2ranking[k] = dict()
                node2ranking[k][0] = dict()
                node2ranking[k][0]["min"] = v
                node2ranking[k][0]["min_ver"] = version
                node2ranking[k][0]["max"] = v
                node2ranking[k][0]["max_ver"] = version
            else:
                key_max = max(node2ranking[k].keys())
                if v < node2ranking[k][key_max]["min"]:
                    node2ranking[k][key_max + 1] = dict()
                    node2ranking[k][key_max + 1]["min"] = v
                    node2ranking[k][key_max + 1]["min_ver"] = version
                    node2ranking[k][key_max + 1]["max"] = v
                    node2ranking[k][key_max + 1]["max_ver"] = version
                else:
                    if v > node2ranking[k][key_max]["max"]:
                        node2ranking[k][key_max]["max"] = v
                        node2ranking[k][key_max]["max_ver"] = version
    
    for k in node2ranking.keys():
        for i in node2ranking[k].keys():
            if not k in node2score.keys():
                node2score[k] = dict()
                node2score[k]["score"] = node2ranking[k][i]["max"] - node2ranking[k][i]["min"]
                node2score[k]["min_ver"] = node2ranking[k][i]["min_ver"]
                node2score[k]["max_ver"] = node2ranking[k][i]["max_ver"]
            else:
                if (node2ranking[k][i]["max"] - node2ranking[k][i]["min"]) > node2score[k]["score"]:
                    node2score[k]["score"] = node2ranking[k][i]["max"] - node2ranking[k][i]["min"]
                    node2score[k]["min_ver"] = node2ranking[k][i]["min_ver"]
                    node2score[k]["max_ver"] = node2ranking[k][i]["max_ver"]
    return node2score

if __name__ == '__main__':
    node2score = find_article_required_refactoring()
    