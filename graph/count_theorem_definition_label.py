import os
import glob
import pprint
import json
import re

def make_mizar_file_path(mml_version):
    cwd = os.getcwd()
    try:
        os.chdir("mml/" + mml_version + "/")
        miz_files = glob.glob("*.miz")  # mmlディレクトリの.mizファイルを取り出す

    finally:
        os.chdir(cwd)
    
    return miz_files

def classify_theorem_definition_and_other_label(inner_labels):
    """article内を参照するlabelをtheorem,definitionとそれ以外に分ける．

    Args:
        inner_labels ([type]): [description]

    Returns:
        [type]: [description]
    """
    inner_theorems_and_definitions = list()
    not_inner_theorems_and_definitions = list()
    for label in inner_labels:
        if re.fullmatch(r"[a-zA-Z]\d*|Lm\d*|lm\d*|[a-zA-Z]\d?[a-zA-Z]", label):
            not_inner_theorems_and_definitions.append(label)
        else:
            inner_theorems_and_definitions.append(label)
    return inner_theorems_and_definitions, not_inner_theorems_and_definitions

def classify_inner_label_and_outer_label(theorems_definitions_and_labels):
    labels = list()
    non_labels = list()
    for word in theorems_definitions_and_labels:
        if ":" in word:
            non_labels.append(word)
        else:
            labels.append(word)
    return labels, non_labels
    
def count_theorem_and_definition(miz_file_contents):
    thoerem_or_definition2number = dict()
    theorems_definitions_and_labels = extract_theorem_definition_and_label(miz_file_contents)
    _, non_labels = classify_inner_label_and_outer_label(theorems_definitions_and_labels)
    for i in non_labels:
        if not i in thoerem_or_definition2number.keys():
            thoerem_or_definition2number[i] = 1
        else:
            thoerem_or_definition2number[i] += 1
    return thoerem_or_definition2number

def count_label(miz_file_contents, only_theorem_and_definition=True):
    label2number = dict()
    theorems_definitions_and_labels = extract_theorem_definition_and_label(miz_file_contents)
    labels, _ = classify_inner_label_and_outer_label(theorems_definitions_and_labels)
    if only_theorem_and_definition:
        labels, _ = classify_theorem_definition_and_other_label(labels)
    for i in labels:
        if not i in label2number.keys():
            label2number[i] = 1
        else:
            label2number[i] += 1
    return label2number

def calc_average_of_labels_num(miz_file2label):
    total_label = make_total_or_definition2number(miz_file2label)
    total_miz_file = len(miz_file2label.keys())
    total = 0
    for num in total_label.values():
        total += num
    return total / total_miz_file

def make_total_or_definition2number(miz_file2theorem_or_definition2number):
    total_theorem_or_definition2number = dict()
    for k1 in miz_file2theorem_or_definition2number.keys():
        for k2, v2 in miz_file2theorem_or_definition2number[k1].items():
            if not k2 in total_theorem_or_definition2number.keys():
                total_theorem_or_definition2number[k2] = v2
            else:
                total_theorem_or_definition2number[k2] += v2
    return total_theorem_or_definition2number

def calc_average_of_theorems_and_definitions(miz_file2theorems_and_definitions):
    total_theorem_or_definition2number = make_total_or_definition2number(miz_file2theorems_and_definitions)
    total_miz_file = len(miz_file2theorems_and_definitions.keys())
    total = 0
    for num in total_theorem_or_definition2number.values():
        total += num
    return total / total_miz_file

def extract_theorem_definition_and_label(article):
    file_words = re.findall(r"\w+:*|\n|::|;|\.=|:\w+", article)
    is_comment = False
    is_theorem_or_label = False
    theorem_definition_and_label = list()

    # mizファイルからbyで引用するtheorem,labelを取得する
    for word in file_words:
        # コメント行の場合
        if word == "::" and not is_comment:
            is_comment = True
            continue
        # コメント行の終了
        if re.search(r"\n", word) and is_comment:
            is_comment = False
            continue
        # byの検索
        if word == "by" and not is_comment:
            is_theorem_or_label = True
            continue
        # byで引用する構文の終了
        if (re.search(r";", word) or re.search(r"\.=", word)) and is_theorem_or_label:
            is_theorem_or_label = False
            continue
        # byで引用するtheorem, labelを取得
        if is_theorem_or_label and word != "\n":
            if theorem_definition_and_label:
                if re.search(r":$|:def$", theorem_definition_and_label[-1]):
                    theorem_definition_and_label[-1] = theorem_definition_and_label[-1] + word
                    continue
                elif re.match(r"\d+", word):
                    if re.search(r":def\d+$|:\d+$", theorem_definition_and_label[-1]):
                        new_theorem = theorem_definition_and_label[-1]
                        theorem_definition_and_label.append(re.sub(r"\d+$", word, new_theorem))
                    continue
                elif re.match(r".+:.+", theorem_definition_and_label[-1]) and re.match(r"def", word):
                    new_definition = theorem_definition_and_label[-1]
                    theorem_definition_and_label.append(re.sub(r":.+$", ":def", new_definition))
                    continue
                elif re.match(r":def", word):
                    theorem_definition_and_label[-1] = theorem_definition_and_label[-1] + word
                    continue
            theorem_definition_and_label.append(word)
        
    return theorem_definition_and_label

def get_numnber_of_proof(old_article, new_article):
    return count_proof(old_article), count_proof(new_article)

def count_proof(article):
    # 単語、改行、::、;で区切ってファイルの内容を取得
    file_words = re.findall(r"\w+|\n|::", article)
    is_comment = False
    proof_counter = 0

    # mizファイルからbyで引用するtheorem,labelを取得する
    for word in file_words:
        # コメント行の場合
        if word == "::" and not is_comment:
            is_comment = True
            continue
        # コメント行の終了
        if re.search(r"\n", word) and is_comment:
            is_comment = False
        # コメント外でproofが出現
        if not is_comment and word == "proof":
            proof_counter += 1

    return proof_counter

def make_article2number_of_inner_theorems_and_definitions(article2label2number):
    article2number_of_inner_theorems_and_definitions = dict()
    for article, labels in article2label2number.items():
        article2number_of_inner_theorems_and_definitions[article] = 0
        for n in labels.values():
            article2number_of_inner_theorems_and_definitions[article] += n
    return article2number_of_inner_theorems_and_definitions

def make_article2number_of_theorems_or_definitions(article2thorems_and_definition2number):
    article2number_of_theorems_and_definitions = dict()
    for article, labels in article2thorems_and_definition2number.items():
        article2number_of_theorems_and_definitions[article] = 0
        for n in labels.values():
            article2number_of_theorems_and_definitions[article] += n
    return article2number_of_theorems_and_definitions

def main(mml_version):
    miz_file2theorem_or_definition2number = dict()
    miz_file2label2number = dict()
    miz_file2other_label2number = dict()
    mizar_file_path = make_mizar_file_path(mml_version)
    for mizar_file in mizar_file_path:
        with open(os.path.join("mml/" + mml_version + "/", mizar_file), 'rt',
                  encoding='utf-8', errors="ignore") as f:
            contents = f.read()
        miz_file2theorem_or_definition2number[mizar_file] = dict()
        miz_file2theorem_or_definition2number[mizar_file] = count_theorem_and_definition(contents)
        miz_file2label2number[mizar_file] = dict()
        miz_file2label2number[mizar_file] = count_label(contents, only_theorem_and_definition=True)
        miz_file2other_label2number[mizar_file] = dict()
        miz_file2other_label2number[mizar_file] = count_label(contents, only_theorem_and_definition=False)
        for k in miz_file2label2number[mizar_file].keys():
            del miz_file2other_label2number[mizar_file][k]
    with open("research_data/article2values/article2outer_theorems_and_definitions.json", "w") as f:
        f.write(json.dumps(miz_file2theorem_or_definition2number, indent=4))
    total_theorem_or_definition2number = make_total_or_definition2number(miz_file2theorem_or_definition2number)
    with open("th_or_def2num.txt", "w") as f:
        f.write(pprint.pformat(sorted(total_theorem_or_definition2number.items(),
                key=lambda x:x[1], reverse=True)))
        f.write("\n average: " + str(calc_average_of_theorems_and_definitions(miz_file2theorem_or_definition2number)))
    with open("th_or_def2num.json", "w") as f:
        f.write(json.dumps(total_theorem_or_definition2number, indent=4))
    with open("research_data/average_of_number_of_inner_theorems_and_definitions.txt", "w") as f:
        f.write("average: " + str(calc_average_of_labels_num(miz_file2label2number)))
    with open("research_data/article2values/article2inner_theorem_definition_labels.json", "w") as f:
        f.write(json.dumps(miz_file2label2number, indent=4))
    with open("research_data/ranking/most_number_of_theorem_and_definition_ranking.txt", "w") as f:
        f.write(pprint.pformat(sorted(make_article2number_of_theorems_or_definitions(miz_file2theorem_or_definition2number).items(),
                key=lambda x:x[1], reverse=True)))
    with open("research_data/article2values/article2number_of_outer_theorems_and_definitions.json", "w") as f:
        f.write(json.dumps(make_article2number_of_theorems_or_definitions(miz_file2theorem_or_definition2number), indent=4))
    with open("research_data/ranking/most_number_of_labels_ranking.txt", "w") as f:
        f.write(pprint.pformat(sorted(make_article2number_of_inner_theorems_and_definitions(miz_file2label2number).items(),
                key=lambda x:x[1], reverse=True)))
    with open("research_data/article2values/article2number_of_inner_theorems_and_definitions.json", "w") as f:
        f.write(json.dumps(make_article2number_of_inner_theorems_and_definitions(miz_file2label2number), indent=4))
    with open("research_data/article2values/article2other_labels.json", "w") as f:
        f.write(json.dumps(miz_file2other_label2number, indent=4))

if __name__ == "__main__":
    main("2020-06-18")
