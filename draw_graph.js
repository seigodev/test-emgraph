/*
createGraph.pyで出力されたファイルとcytoscape.jsを使って
グラフの描画を行う
*/
$(function(){
    $.when(
        $.getJSON('./dot_graph_ver2.json'),
        $.getJSON('./sfdp_graph.json')
    )
    .then((dot_graph, sfdp_graph) => {
        // cytoscapeグラフの作成(初期化)
        let cy = window.cy = cytoscape({
            container: document.getElementById('graph'),
            elements: [],
            boxSelectionEnabled: true,
            autounselectify: false,
            selectionType: "additive"
        });
        let dot_node2pos = {};
        let sfdp_node2pos = {};
        // dot(階層グラフ)の各ノードの座標値を記録
        for(let i in dot_graph[0]["elements"]["nodes"]){
            for(let j in dot_graph[0]["elements"]["nodes"][i]){
                dot_node2pos[dot_graph[0]["elements"]["nodes"][i][j]["name"]] = 
                {'x': (dot_graph[0]["elements"]["nodes"][i][j]["x"] + 1) * 300, 'y': (dot_graph[0]["elements"]["nodes"][i][j]["y"] + 1) * 300}
            }
        }
        // sfdp(クラスタリンググラフ)の各ノードの座標値を記録
        for(let i in dot_graph[0]["elements"]["nodes"]){
            for(let j in dot_graph[0]["elements"]["nodes"][i]){
                sfdp_node2pos[dot_graph[0]["elements"]["nodes"][i][j]["name"]] = 
                {'x': (sfdp_graph[0]["elements"]["nodes"][i][j]["x"] + 1) * 300, 'y': (sfdp_graph[0]["elements"]["nodes"][i][j]["y"] + 1) * 300}
            }
        }
 
        // グラフにノードを追加
        // dot_graph[0], sfdp_graph[0]にグラフデータが入っている
        for(let i in dot_graph[0]["elements"]["nodes"]){
            for(let j in dot_graph[0]["elements"]["nodes"][i]){
                cy.add({
                    group: "nodes",
                    data:{
                        id: dot_graph[0]["elements"]["nodes"][i][j]["id"],
                        name: dot_graph[0]["elements"]["nodes"][i][j]["name"],
                        is_dummy: dot_graph[0]["elements"]["nodes"][i][j]["is_dummy"],
                        href: dot_graph[0]["elements"]["nodes"][i][j]["href"]
                    },
                    position:{
                        x: (dot_graph[0]["elements"]["nodes"][i][j]["x"] + 1) * 300,
                        y: (dot_graph[0]["elements"]["nodes"][i][j]["y"] + 1) * 300
                    }
                });
            }
        }
        // グラフにエッジを追加
        for(let i in dot_graph[0]["elements"]["edges"]){
            for(let j in dot_graph[0]["elements"]["edges"][i]){
                cy.add({
                    group: "edges",
                    data:{
                        source: dot_graph[0]["elements"]["edges"][i][j]["source"],
                        target: dot_graph[0]["elements"]["edges"][i][j]["target"]
                    }
                });
            }
        }

        // グラフのスタイルを決定
        cy.style([
            /* 初期状態のスタイル */
            {
                selector: "node",
                css: {"background-color": "#ff0000", "shape": "ellipse", "width": 150, "height": 150,
                        "content": "data(name)", "font-size": 40, "opacity": 1, "z-index": 1,
                        "text-halign":"center", "text-valign": "center", "font-style": "normal",
                        "font-weight": "bold", "color": "#ffffff",
                        "text-outline-color": "red", "text-outline-opacity": 1, "text-outline-width": 10}  // 0.8 30
            },
            {
                selector: "edge",
                css: {"line-color": "black", "target-arrow-shape": "triangle", "curve-style": "straight",
                "target-arrow-color": "black", "arrow-scale": 3, "width": 5, "opacity": 0.3, "z-index": 1}  //0.3
            },
            /* リンクのないノードは灰色 */
            {
                selector: "node[!href][!is_dummy]",
                css: {"background-color": "#a9a9a9", "z-index": 1}
            },
            /* ノードが左クリックされたときに適応されるスタイル */
            // 選択されたノード全てのスタイル
            {
                selector: "node.highlight",
                css: {"font-size": 20,  "width": 250, "height": 250, "font-size": 100,
                "content": "data(name)", "opacity": 1, "z-index": 10}
            },
            // 選択(左クリック)されたノードのスタイル
            {
                selector: "node.selected",
                css: {"background-color": "#fff100", "color": "#ff0000", "width": 300, "height": 300,
                "text-outline-color": "#fff100", "text-outline-opacity": 1, "text-outline-width": 10
                }
            },
            // 選択された(強調表示する)祖先のスタイル
            {
                selector: "node.selected_ancestors0",
                css: {"background-color": "#fcc800",  "color": "#ffffff",
                "text-outline-color": "#fcc800", "text-outline-opacity": 1, "text-outline-width": 10} 
            },
            {
                selector: "node.selected_ancestors1",
                css: {"background-color": "#f39800",  "color": "#ffffff",
                "text-outline-color": "#f39800", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors2",
                css: {"background-color": "#eb6100", "color": "#ffffff",
                "text-outline-color": "#eb6100", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors3",
                css: {"background-color": "#e60012", "color": "#ffffff",
                "text-outline-color": "#e60012", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors4",
                css: {"background-color": "#ff4477", "color": "#ffffff",
                "text-outline-color": "#ff4477", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors5",
                css: {"background-color": "#ff6699", "color": "#ffffff",
                "text-outline-color": "#ff6699", "text-outline-opacity": 1, "text-outline-width": 10} 
            },
            {
                selector: "node.selected_ancestors6",
                css: {"background-color": "#cc4499", "color": "#ffffff",
                "text-outline-color": "#cc4499", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors7",
                css: {"background-color": "#be0081", "color": "#ffffff",
                "text-outline-color": "#be0081", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors8",
                css: {"background-color": "#920783", "color": "#ffffff",
                "text-outline-color": "#920783", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_ancestors9",
                css: {"background-color": "#601986", "color": "#ffffff",
                "text-outline-color": "#601986", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            // 選択された(強調表示する)子孫のスタイル
            {
                selector: "node.selected_descendants0",
                css: {"background-color": "#cfdb00", "color": "#ffffff",
                "text-outline-color": "#cfdb00", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants1",
                css: {"background-color": "#8fc31f", "color": "#ffffff",
                "text-outline-color": "#8fc31f", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants2",
                css: {"background-color": "#22ac38", "color": "#ffffff",
                "text-outline-color": "#22ac38", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants3",
                css: {"background-color": "#009944", "color": "#ffffff",
                "text-outline-color": "#009944", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants4",
                css: {"background-color": "#009b6b", "color": "#ffffff",
                "text-outline-color": "#009b6b", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants5",
                css: {"background-color": "#009e96", "color": "#ffffff",
                "text-outline-color": "#009e96", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants6",
                css: {"background-color": "#00a0c1", "color": "#ffffff",
                "text-outline-color": "#00a0c1", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants7",
                css: {"background-color": "#00a0e9", "color": "#ffffff",
                "text-outline-color": "#00a0e9", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants8",
                css: {"background-color": "#0086d1", "color": "#ffffff",
                "text-outline-color": "#0086d1", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            {
                selector: "node.selected_descendants9",
                css: {"background-color": "#0068b7", "color": "#ffffff",
                "text-outline-color": "#0068b7", "text-outline-opacity": 1, "text-outline-width": 10}
            },
            // 強調表示されたノードをつなぐエッジのスタイル
            {
                selector: "edge.highlight",
                css: {"line-color": "#006400", "curve-style": "straight",
                "target-arrow-color": "#006400", "arrow-scale": 5, "width": 10, "opacity": 1, "z-index": 20}
            },

            /* ダミーノードを指すエッジが選択された場合 */
            {
                selector: cy.nodes().edgesTo("node.selected[?is_dummy]"),
                css: {"line-color": "green", "target-arrow-shape": "none", "curve-style": "straight",
                "arrow-scale": 10, "width": 5, "z-index": 10, width: 20}  //arrow-scale 0
            },
            // 選択されていないノードの色を変更
            {
                selector: "node.faded",
                css: {"background-color": "#808080"}
            },
            // 選択されていないノードとエッジは薄く表示する
            {
                selector: ".faded",
                css: {"opacity": 0.4, "z-index": 0}  // 0.05, 0
            },
        ]);


        /* 初期状態の設定 */
        all_nodes_positions = cy.nodes().positions();  //ノードの位置を記録　今のところ使ってない
        let all_nodes = cy.nodes();
        let all_elements = cy.elements();
        cy.fit(cy.nodes().orphans());


        // 強調表示する祖先、子孫の世代数の初期化
        let ancestor_generations = 1
        let descendant_generations = 1


        /* 検索機能の追加 */
        // 全ノード名の取得
        let all_article_names = [];
        cy.nodes("[!is_dummy]").forEach(function(node){
            all_article_names.push(node.data("name"));
        });
        all_article_names.sort();
        // datalistに全ノード名を追加
        for (let article_name of all_article_names){
            $("#article_list").append($("<option/>").val(article_name).html(article_name));
        }
        // searchボタンをクリックしたら検索開始
        $("#search").click(function() {
            // dropdownで選択したノード名、または記述したノード名を取得
            let select_node_name = $("#article_name").val();
            let select_node = cy.nodes().filter(function(ele){
                return ele.data("name") == select_node_name;
            });
            // ノードが存在するか確認し、処理
            if(select_node.data("name")){
                reset_elements_style(cy);
                cy.$(select_node).addClass("selected");
                highlight_select_elements(cy, select_node, ancestor_generations, descendant_generations);
                $("#select_article").text("SELECT: " + select_node_name);
            }
            else{
                alert("ERROR: Don't have '" + select_node_name + "' node. Please select existed nodes.");
            }
        });


        // 強調表示したい祖先、子孫の世代数を取得
        $("#ancestor_generations").on("change", function(){
            ancestor_generations = $("#ancestor_generations").val();
        });
        $("#descendant_generations").on("change", function(){
            descendant_generations = $("#descendant_generations").val();
        });


        // 背景をクリックしたときの処理
        cy.on("tap", function(event){
            let clicked_point = event.target;
            if (clicked_point === cy){
                reset_elements_style(cy);
            }
        });


        // ノードをクリックした場合、リンクに飛ぶ(htmlリンクの設定)
        // faded状態ならば反応しない
        cy.nodes().on("cxttap", function(event){
            let clicked_node = event.target;
            try {  // your browser may block popups
                window.open(this.data("href"));
            } catch(e){  // fall back on url change
                window.location.href = this.data("href");
            }
        });


        // クリックしたノードの親と子、自身を色変更
        cy.nodes().on("tap", function(e){
            // 全ノードをクラスから除外
            reset_elements_style(cy);
            // クリックしたノードをselectedクラスに入れる
            let clicked_node = e.target;
            highlight_select_elements(cy, clicked_node, ancestor_generations, descendant_generations);
            let clicked_node_name = clicked_node.data("name");
            $("#select_article").text("SELECT: " + clicked_node_name);
        });


        // reloadボタンでリロードにする
        $(document).ready(function(){
            $("#reload").click(function(){
                location.reload();
            });
        });

        // Hierarchical graphボタンでレイアウトを階層グラフに変更する
        $("#dot_layout").click(function() {
            for(let n in dot_node2pos){
                let node = cy.nodes().filter(function(ele){
                    return ele.data("name") == n;
                });
                cy.$(node).position({x: dot_node2pos[n]['x'], y: dot_node2pos[n]['y']});
            }
        });
        // Clustering graphボタンでレイアウトをクラスタリンググラフに変更する
        $("#sfdp_layout").click(function() {
            for(let n in sfdp_node2pos){
                let node = cy.nodes().filter(function(ele){
                    return ele.data("name") == n;
                });
                cy.$(node).position({x: sfdp_node2pos[n]['x'], y: sfdp_node2pos[n]['y']});
            }
        });

    }, () => {
        alert("ERROR: Failed to read JSON file.");
    });
});


function reset_graph(cy, all_nodes_positions) {
    /**
    * 移動したノードなどを初期の位置に戻す。
    **/
    location.reload();  //画面をリロード
}


/**
 * グラフの要素のスタイルを初期状態(ノード：赤い丸、エッジ：黒矢印)に戻す。
 * ただし、移動したノードの位置は戻らない。
 * @param {cytoscape object} cy グラフ本体
 * @return
**/
function reset_elements_style(cy) {
    let all_class_names = ["highlight",  "faded",  "selected"];
    for(let i=0; i<10; i++){
        all_class_names.push("selected_ancestors" + i);
        all_class_names.push("selected_descendants" + i);
    }
    cy.elements().removeClass(all_class_names);
    cy.nodes().unlock();
}


/**
 * 選択されたノードとそのノードの親子を強調表示させる(selectedクラスに追加する)
 * @param {cytoscape object} cy グラフ本体
 * @param {cytoscape object} select_node cy内の単一のノード
 * @param {int} ancestor_generations 辿りたい祖先の数
 * @param {int} descendant_generations 辿りたい子孫の数
 * @return
**/
function highlight_select_elements(cy, select_node, ancestor_generations, descendant_generations){
    // 選択したノードの処理
    cy.$(select_node).addClass("highlight");
    cy.$(select_node).addClass("selected");

    // 選択したノードの祖先、子孫を強調表示する
    is_ancestor = true;
    highlight_connected_elements(cy, ancestor_generations, select_node, is_ancestor);
    highlight_connected_elements(cy, descendant_generations, select_node, !is_ancestor);

    // highlightクラス以外の物はfadedクラスに入れる
    fade_out_faded_elements(cy);

    // fadedクラスの物は、動かせないようにする
    cy.$(".faded").lock();
    // fadedクラスはイベント無効
    //cy.$(".faded").removeAllListeners();

    console.log(cy.nodes(".highlight").length);

}


/**
 * 選んだ1つのノードに近づく、焦点を当てる。
 * @param {cytoscape object} cy: cytoscapeグラフ本体
 * @param {cytoscape object} selected_node: cyの単一のノード。近づきたいノード。
 * @return
**/
function focus_on_selected_node(cy, selected_node){
    cy.animate({
        fit:{
            eles: selected_node,
            padding: 310
        }
    });
}


/**
 * 選択したノード(select_node)とその祖先または子孫を任意の世代数(generations)までを
 * 強調表示するクラスに追加する。
 * アルゴリズム
 *      次の処理を辿りたい世代数まで繰り返す
            1. node_to_get_connectionの親(もしくは子)ノードとそのエッジを強調表示させるクラスに追加する
            2. 1でクラスに追加したノードをnode_to_get_connectionとして更新する
            3. 2でnode_to_get_connectionが空ならループを中断する
 * @param {cytoscape object} cy cytoscapeのグラフ本体
 * @param {int} generations 辿りたい世代数
 * @param {cytoscape object} select_node 選択したノード
 * @param {boolean} is_ancestor 辿りたいのは祖先かどうか。trueなら祖先、falseなら子孫を強調表示させていく。
 * @return
**/
function highlight_connected_elements(cy, generations, select_node, is_ancestor){
    let node_to_get_connection = cy.collection();  // 親(もしくは子)を取得したいノードのコレクション（≒リスト）
    node_to_get_connection = node_to_get_connection.union(select_node);
    for (let i=0; i<generations; i++){
        let class_name = is_ancestor ? "selected_ancestors" : "selected_descendants";
        class_name += Math.min(9, i);
        let next_node_to_get_connection = cy.collection();
        cy.$(node_to_get_connection).forEach(function(n){
            let connect_elements = is_ancestor ? n.outgoers() : n.incomers();
            connect_elements = connect_elements.difference(cy.$(connect_elements).filter(".highlight"));
            cy.$(connect_elements).addClass("highlight");
            cy.$(connect_elements).nodes().addClass(class_name);
            next_node_to_get_connection = next_node_to_get_connection.union(connect_elements.nodes());
        });
        node_to_get_connection = next_node_to_get_connection;
        if (node_to_get_connection.length === 0){
            break;
        }
    }
}


/**
 * 強調表示されていない(highlightクラスに属していない)ノード、エッジをfadedクラスに入れる。
 * @param {cytoscape object} cy cytoscapeグラフ本体
 * @return
**/
// convert style to fade
function fade_out_faded_elements(cy){  // change_style_to_fade_for_not_selected_elements
    let other = cy.elements();
    other = other.difference(cy.elements(".highlight"));
    cy.$(other).addClass("faded");
}


/**
 * nodes内からダミーノードを探し、ダミーでないノードまでたどる。
 * @param {cytoscape object} cy cytoscape.jsのグラフ本体
 * @param {cytoscape object} select_element 選択状態になった要素の集合
 * @param {boolean} is_target 祖先をたどるか
 * @return {cytoscape object} connect_node_collection 新たに強調表示になったノードの集合
**/
function search_not_dummy_node(cy, select_elements, is_targets) {
    let connect_node_collection = cy.collection();
    for (let node of Object.values(select_elements.nodes())){
        if(node.data){
            if(node.data("is_dummy")){
                let dummy_node_and_edge = (is_targets) ? node.outgoers() : node.incomers();
                cy.$(dummy_node_and_edge).addClass("selected");  // is_targetならselected_ancestorsに追加
                let dummy_node = dummy_node_and_edge.nodes();  // dummy_nodeって名前良くない
                while(dummy_node.data("is_dummy")){
                    dummy_node_and_edge = (is_targets) ? dummy_node.outgoers() : dummy_node.incomers();
                    cy.$(dummy_node_and_edge).addClass("selected");
                    dummy_node = dummy_node_and_edge.nodes();
                }
                connect_node_collection = connect_node_collection.union(dummy_node);
            }
            else{
                connect_node_collection = connect_node_collection.union(node);
            }
        }
    }
    return connect_node_collection;
}

/**
 * HTMLファイル内からlayoutを読み込み，対応したjsonファイル（グラフファイル）名を返す．
 * @param {cytoscape object} cy cytoscape.jsのグラフ本体
 * @param {cytoscape object} select_element 選択状態になった要素の集合
 * @param {boolean} is_target 祖先をたどるか
 * @return {cytoscape object} connect_node_collection 新たに強調表示になったノードの集合
**/
function select_layout() {
    let layout = document.getElementById("layout").value;
    console.log(layout)

    return layout
}
