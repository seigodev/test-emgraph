import os
import json
import pprint
import networkx as nx
from retrieve_dependency import make_miz_dependency

def create_article2number_of_referenced(mizar_ver, create_file=False):
    article2dependency_article = make_miz_dependency(mizar_ver)
    article2number_of_referenced = dict()
    for k, dependncy_articles in article2dependency_article.items():
        if not k in article2number_of_referenced.keys():
            article2number_of_referenced[k] = 0
        for v in dependncy_articles:
            if not v in article2number_of_referenced.keys():
                article2number_of_referenced[v] = 1
            else:
                article2number_of_referenced[v] += 1

    if create_file:
        with open("research_data/article2values/article2number_of_referenced("+ mizar_ver +").txt", "w") as f:
            f.write(pprint.pformat(sorted(article2number_of_referenced.items(), key=lambda x:x[1], reverse=True)))
        with open("research_data/article2values/article2number_of_referenced("+ mizar_ver +").json", "w") as f:
            f.write(json.dumps(article2number_of_referenced, indent=4))

    return article2number_of_referenced


def make_article2pagerank_from_graph_attrs(mml_version):
    cwd = os.getcwd()
    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + "_pagerank.json", "r") as f:
            graph = json.load(f)
    finally:
        os.chdir(cwd)
    # networkxのグラフを作成
    G = nx.cytoscape_graph(graph)

    return nx.get_node_attributes(G, "pagerank")


def make_article2authority_from_graph_attrs(mml_version):
    cwd = os.getcwd()
    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + "_hits_authority.json", "r") as f:
            graph = json.load(f)
    finally:
        os.chdir(cwd)
    # networkxのグラフを作成
    G = nx.cytoscape_graph(graph)
    
    return nx.get_node_attributes(G, "authority")


def create_table_pagerank_auth_referenced_articles(mizar_ver):
    with open("research_data/article2values/article2number_of_referenced("+ mizar_ver +").json", "r") as f:
        article2number_of_referenced = json.load(f)
    article2number_of_referenced = sorted(article2number_of_referenced.items(), key=lambda x:x[1], reverse=True)
    article2authority = sorted(make_article2authority_from_graph_attrs(mizar_ver).items(), key=lambda x:x[1], reverse=True)
    article2pagerank = sorted(make_article2pagerank_from_graph_attrs(mizar_ver).items(), key=lambda x:x[1], reverse=True)

    with open("research_data/ranking/table_pagerank_authority_referenced_articles.md", "w") as f:
        f.write("| pagerank | authority | referenced articles |\n")
        f.write("| -------- | --------- | ------------------- |\n")
        for i in range(len(article2authority)):
            f.write("| " + article2pagerank[i][0] + " | " + article2authority[i][0] + " | " + article2number_of_referenced[i][0] + " |\n")


def make_article2authority_minus_pagerank(mml_ver):
    cwd = os.getcwd()
    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_ver + "_authority_minus_pagerank.json", "r") as f:
            graph = json.load(f)
    finally:
        os.chdir(cwd)
     # networkxのグラフを作成
    G = nx.cytoscape_graph(graph)

    return nx.get_node_attributes(G, "auth_minus_pagerank")

    

def create_article2pagerank_authority_referenced_ranking(mml_ver):
    with open("research_data/article2values/article2number_of_referenced("+ mml_ver +").json", "r") as f:
        article2number_of_referenced = json.load(f)
    article2number_of_referenced = sorted(article2number_of_referenced.items(), key=lambda x:x[1], reverse=True)
    article2authority = sorted(make_article2authority_from_graph_attrs(mml_ver).items(), key=lambda x:x[1], reverse=True)
    article2pagerank = sorted(make_article2pagerank_from_graph_attrs(mml_ver).items(), key=lambda x:x[1], reverse=True)
    article2authortiy_minus_pagerank = sorted(make_article2authority_minus_pagerank(mml_ver).items(), key=lambda x:x[1], reverse=True)

    article2number_of_referenced_ranking = dict()
    article2authority_ranking = dict()
    article2pagerank_ranking = dict()
    article2authortiy_minus_pagerank_ranking = dict()

    for i in range(len(article2number_of_referenced)):
        article2number_of_referenced_ranking[article2number_of_referenced[i][0]] = i + 1
    for i in range(len(article2authority)):
        article2authority_ranking[article2authority[i][0]] = i + 1
    for i in range(len(article2pagerank)):
        article2pagerank_ranking[article2pagerank[i][0]] = i + 1
    for i in range(len(article2authortiy_minus_pagerank)):
        article2authortiy_minus_pagerank_ranking[article2authortiy_minus_pagerank[i][0]] = i + 1


    with open("research_data/ranking/article2pagerank_authority_number_of_articles_ranking.md", "w") as f:
        f.write("## article to ranking\n")
        f.write("| article | referenced articles | pagerank | authority | Authority - PageRank | \n")
        f.write("| ------- | ------------------- | -------- | --------- |-------------------------------- | \n")
        for k in article2number_of_referenced_ranking.keys():
            f.write("| " + str(k) + 
                    " | " + str(article2number_of_referenced_ranking[k]) + 
                    " | " + str(article2pagerank_ranking[k]) + 
                    " | " + str(article2authority_ranking[k]) + 
                    " | " + str(article2authortiy_minus_pagerank_ranking[k]) +" |\n")

if __name__ == '__main__':
    create_article2number_of_referenced("2020-06-18", create_file=True)
    create_table_pagerank_auth_referenced_articles("2020-06-18")
    create_article2pagerank_authority_referenced_ranking("2020-06-18")