
import generate_data
import pandas as pd
import numpy as np
import re


from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics
from sklearn import preprocessing

#import for visualizatioin
import pydotplus
from sklearn.datasets import load_iris
from sklearn import tree
import collections


def estimate_critical(dist, speed):
    """ 
    This function will calculate whether there is collision between two car1_pos_rot
    There are two condition make the crash scenario
        1- Distance between two car smaller than 20 (or in range (10,30))
        2. Speed of second car is larger than 20km/h
    """
    if dist < 20 and speed > 20:
        return 1
    else:
        return 0


def pop_to_data_DT(pop):
    """
    The function calulates the critical event with input of populuation
    each indiviual is list of [car1_pos_rot,car1_pos_rot, speed car2]
    The function return a set of (distance, speed, label) of each individual
    Return result a list of tuples(dist, speed, collistion_state): (5.520236587666433, 96, 1)
    """
    data = []
    for ind in pop:
        dist = generate_data.distance_two_Car(ind[0], ind[1])
        speed = ind[2]
        state_scenario = estimate_critical(dist, speed)
        data.append((dist,speed,state_scenario))
    
    return data

def encode_dist(dist):
    """
    Distance encode for decision tree:
        dist_lt_20 in  [0,20]
        dist_bw_20_30 in  [20,30]
        dist_bw_30_40 in  [30,40]
        dist_gt_40 in  [40,.]
    """
    if dist < 20:
        return 'dist_lt_20'
    if 20<= dist < 30:
        return 'dist_bw_20_30'
    if 30<= dist < 40:
        return 'dist_bw_30_40'
    if dist >= 40:
        return 'dist_gt_40'

        
def encode_speed(speed):
    """
    Distance encode for decision tree:
        speed_lt_20 in  [0,20]
        speed_bw_20_40 in  [20,40]
        speed_bw_40_60 in  [40,60]
        speed_gt_60 in  [60,.]

    """
    if speed < 20:
        return 'speed_lt_20'
    if 20<= speed < 40:
        return 'speed_bw_20_40'
    if 40<= speed < 60:
        return 'speed_bw_40_60'
    if speed >= 60:
        return 'speed_gt_60'

def label_encode_distance(dist_list):
    le = preprocessing.LabelEncoder()
    le.fit(["dist_lt_20", "dist_bw_20_30","dist_bw_30_40","dist_gt_40"])
    return le.transform(dist_list) 


def label_encode_distance(speed_list):
    le = preprocessing.LabelEncoder()
    le.fit(["speed_lt_20", "speed_bw_20_40","speed_bw_40_60","speed_gt_60"])
    return le.transform(dist_list) 


def convert_dataFrame(pop):
    """
    This function convers data from population to dataFrame for decision tree
    this function return a table of data
    """
    #get data from population
    data = pop_to_data_DT(pop)
    data_dt = []
    
    #encode data 
    i = 0
    for item in data:
        dist =  encode_dist(item[0])
        speed = encode_speed(item[1])
        state = item[2]
        data_dt.append((dist,speed,state))

    #conver to dataFrame 
    dfObj_tmp = pd.DataFrame(data_dt) 
   
     #adding index for dataframe
    #dfObj.index = [i for i in range (1,len(pop)+1)]
  
    dfObj = dfObj_tmp.set_axis(['distance', 'speed', 'state'], axis=1, inplace=False)
 
    one_hot_data_dist = pd.get_dummies(dfObj['distance'])
    one_hot_data_speed = pd.get_dummies(dfObj['speed'])
    
    #data has format
    #dist_bw_20_30  dist_bw_30_40  dist_gt_40  dist_lt_20  speed_bw_20_40  speed_bw_40_60  speed_gt_60  state
    data_training_DT = pd.concat([one_hot_data_dist,one_hot_data_speed,dfObj['state']],axis=1,sort=False)
    # print("distance ",one_hot_data_dist.head(5))
    # print("speed ",one_hot_data_speed.head(5))
    # print("all ",data_training_dt.head(10))
    #id = [i for i in range (1,len(pop)+1)]
    return data_training_DT


def get_critical_sample_DT(df):
    var_df = "df"

    #split dataset in features and target variable
     
    feature_name = ['dist_bw_20_30', 'dist_bw_30_40', 'dist_gt_40', 'dist_lt_20', \
                   'speed_bw_20_40', 'speed_bw_40_60', 'speed_gt_60']
    feature_cols = feature_name
    X = df[feature_cols] # Features
    y = df['state'] # Target variable

    
    clf = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
                                 max_features=None, max_leaf_nodes=None,
                                 min_impurity_split=1e-07, min_samples_leaf=1,
                                 min_samples_split=2, min_weight_fraction_leaf=0.0,
                                 presort=False, random_state=None, splitter='best')

    # Train Decision Tree Classifer
    #clf = clf.fit(X_train,y_train)
    clf = clf.fit(X,y)
    visualize_data(clf,feature_name)
    
  
    n_nodes = clf.tree_.node_count
    rules, path_values = get_rules(clf,df)
    print("riles", rules)
    print("path",path_values)
    filter_index_df = [] 
    #get index of sample in collision node
    # path_value is a list of numpy array
    for  idx, path_value in  enumerate(path_values):
       
        if check_to_get_node_coll(path_value):
            items = eval(to_code(var_df,rules[idx]))
            for index,row in items.iterrows():
                filter_index_df.append(index)
    # return index of population
    return filter_index_df       
    
    #print("index ",filter_index_df)           
            
    
    # a,b = get_rules(clf,df)
    # for i in a:
        # #print( "encode :",   to_code("df",i))
        # v = eval(to_code("df",i))
        # list_index = []
        # for index,row in v.iterrows():
            # list_index.append(index)
        # #print(list_index)
       # # print(v)
        # #print("get rule ",i)
    # for i in b:
        # print("type",type(i))
        # print("value",i)
        # print("shape",i[0].shape)
        # print("item 1 ",i[0][:,0])
        # print("item 2 ",i[0][:,1])
        # #print("shape : ",  i.shape )
        
   
        
    
   
   
    

    
    
def visualize_data (clf,data_feature_names):
    # Visualize data
    
                                
                                
    dot_data = tree.export_graphviz(clf,
                                feature_names=data_feature_names,
                                out_file=None,
                                filled=True,
                                rounded=True)
    graph = pydotplus.graph_from_dot_data(dot_data)

    colors = ('turquoise', 'orange')
    edges = collections.defaultdict(list)

    for edge in graph.get_edge_list():
        edges[edge.get_source()].append(int(edge.get_destination()))

    for edge in edges:
        edges[edge].sort()
        for i in range(2):
            dest = graph.get_node(str(edges[edge][i]))[0]
            dest.set_fillcolor(colors[i])

    graph.write_png('tree.png')

    

def get_rules(dtc, df):
    rules_list = []
    values_path = []
    values = dtc.tree_.value

    def RevTraverseTree(tree, node, rules, pathValues):
        '''
        Traverase an skl decision tree from a node (presumably a leaf node)
        up to the top, building the decision rules. The rules should be
        input as an empty list, which will be modified in place. The result
        is a nested list of tuples: (feature, direction (left=-1), threshold).  
        The "tree" is a nested list of simplified tree attributes:
        [split feature, split threshold, left node, right node]
        '''
        # now find the node as either a left or right child of something
        # first try to find it as a left node            

        try:
            prevnode = tree[2].index(node)           
            leftright = '<='
            pathValues.append(values[prevnode])
        except ValueError:
            # failed, so find it as a right node - if this also causes an exception, something's really f'd up
            prevnode = tree[3].index(node)
            leftright = '>'
            pathValues.append(values[prevnode])

        # now let's get the rule that caused prevnode to -> node
        p1 = df.columns[tree[0][prevnode]]    
        p2 = tree[1][prevnode]    
        #rules.append(str(p1) + ' ' + leftright + ' ' + str(p2))
        rules.append((p1,leftright,p2))

        # if we've not yet reached the top, go up the tree one more step
        if prevnode != 0:
            RevTraverseTree(tree, prevnode, rules, pathValues)

    # get the nodes which are leaves
    leaves = dtc.tree_.children_left == -1
    leaves = np.arange(0,dtc.tree_.node_count)[leaves]

    # build a simpler tree as a nested list: [split feature, split threshold, left node, right node]
    thistree = [dtc.tree_.feature.tolist()]
    thistree.append(dtc.tree_.threshold.tolist())
    thistree.append(dtc.tree_.children_left.tolist())
    thistree.append(dtc.tree_.children_right.tolist())

    # get the decision rules for each leaf node & apply them
    for (ind,nod) in enumerate(leaves):

        # get the decision rules
        rules = []
        pathValues = []
        index_collision_list = []
        RevTraverseTree(thistree, nod, rules, pathValues)

        pathValues.insert(0, values[nod])      
        pathValues = list(reversed(pathValues))

        rules = list(reversed(rules))

        rules_list.append(rules)
        values_path.append(pathValues)
        #nodevalue = dtc.tree_.value[nod]

    return (rules_list, values_path)
    
    

    


    
    
def to_code (var_name_df, rules):
    """
    input: name of data_fram and rules of a node.
    data shoulc be have this format
    df[ (df["feature1"] > 40) & (df["feature2"] > 0) ] 
    """
    string_rule = ""
    string_to_cod = ""
    
        #there is only one rule
    if len(rules) == 1:
        feature, oper, value = rules[0]
        string_rule = "("+ var_name_df +'["' + str(feature) + '"] ' + str(oper) + ' ' + str(value) + " )"
    else:
        for counter, rule in enumerate(rules):
            if counter == 0:
                feature, oper, value = rule
                string_rule = "("+ var_name_df +'["' + str(feature) + '"] ' + str(oper) + ' ' + str(value) + " )"
            else:
                feature, oper, value = rule
                string_rule += " & ("+ var_name_df +'["' + str(feature) + '"] ' + str(oper) + ' ' + str(value) + " )"
    
    string_to_cod = var_name_df + '[ ' +string_rule + ']'
    return string_to_cod


def check_to_get_node_coll(path_list):
   
    
    last_id = len(path_list) -1
    value = path_list[last_id]

    # print("value shape", value.shape)
    # print(" check_to_get_node_coll value1",value[0:1][0][0])
    # print(" check_to_get_node_coll value2",value[0:1][0][1])
    
    #number of collision bigger than number of safe scenarios
    if value[0:1][0][0] < value[0:1][0][1]:
        return 1
    else:
        return 0




for i in range (10,70):
    pass
    #print (i, encode_speed(i), encode_dist(i))
    
   # print (a)


   
