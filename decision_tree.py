import sys_output
import generate_data
import pandas as pd
import numpy as np
import re
import os
from datetime import datetime

from NSGAII import file_name

from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics
from sklearn import preprocessing

#import for visualizatioin
import pydotplus
from sklearn.datasets import load_iris
from sklearn import tree
import collections
from create_xml_scenario import generate_xml_testcase, run_TC_DriveBuild, converse_result


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
    dist = list()
    speed = list()
    for ind in pop:
        #dist = generate_data.distance_two_Car(ind[0], ind[1])
        dist_tmp = ind[1][1]
        speed_tmp = ind[2]
        dist.append(dist_tmp)
        speed.append(speed_tmp)
    # generate TC with XML file
    generate_xml_testcase(len(pop), dist, speed)
    
    #change result to 0 or 1 base on the result returns from DriveBuidl 
    
    
    result = run_TC_DriveBuild(len(pop))
    biResult = converse_result(result)
    for i in rang(len(pop)):
        data.append((dist[i], speed[i],result[i]))
    return data





# def estimate_critical(dist, speed):
    # """ 
    # This function will calculate whether there is collision between two car1_pos_rot
    # There are two condition make the crash scenario
        # 1- Distance between two car smaller than 20 (or in range (10,30))
        # 2. Speed of second car is larger than 20km/h
    # """
    # if dist < 20 and speed > 20:
        # return 1
    # else:
        # return 0


# def pop_to_data_DT(pop):
    # """
    # The function calulates the critical event with input of populuation
    # each indiviual is list of [car1_pos_rot,car1_pos_rot, speed car2]
    # The function return a set of (distance, speed, label) of each individual
    # Return result a list of tuples(dist, speed, collistion_state): (5.520236587666433, 96, 1)
    # """
    # data = []

    # for ind in pop:
        # #dist = generate_data.distance_two_Car(ind[0], ind[1])
        # dist = ind[1][1]
        # speed = ind[2]
        # state_scenario = estimate_critical(dist, speed)
        # data.append((dist,speed,state_scenario))
    
    # return data

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


#dist_bw_20_30  dist_bw_30_40  dist_gt_40  dist_lt_20  speed_bw_20_40  speed_bw_40_60  speed_gt_60  state
   
def check_dataFrame(df):
           
    df1 = pd.DataFrame()
    data_frame = pd.DataFrame()
    list_missing_colum = []
    if 'dist_bw_20_30' not in df:
        list_missing_colum.append('dist_bw_20_30')
                       
    if 'dist_bw_30_40' not in df:
        list_missing_colum.append('dist_bw_30_40')
   
    if 'dist_gt_40' not in df:
        list_missing_colum.append('dist_gt_40')

    if 'dist_lt_20' not in df:
        list_missing_colum.append('dist_lt_20')
        # df1['dist_lt_20'] = np.zeros(len(df.index))
        # data_frame = pd.concat([df,df1['dist_lt_20']],axis=1,sort=False)

    if 'speed_bw_20_40' not in df:
        list_missing_colum.append('speed_bw_20_40')
    
    if 'speed_bw_40_60' not in df:
        list_missing_colum.append('speed_bw_40_60')
       

    if 'speed_gt_60' not in df:
        list_missing_colum.append('speed_gt_60')
     
    for colume in list_missing_colum:
        df1[colume] = np.zeros(df.shape[0])
    
    data_frame = pd.concat([df,df1],axis=1,sort=False)
    
    
    
    
    return data_frame

def file_name1():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    return filename

def convert_dataFrame(pop):
    """
    This function convers data from population to dataFrame for decision tree
    this function return a table of data
    """
    #print ("population",pop)
    data = pop_to_data_DT(pop)
    
   # print ("pop to data",data)
    data_dt = []
    
    #encode data 
    i = 0
    
    print("\n\nEncode data from (car1_pos_rot, car2_pop_rot, speed) to (Distance_2cars, speed_behind_Car,state)")
          # \n when Distance < 20 and speed >20 could  lead a crash of two car \n")
    for item in data:
        dist =  encode_dist(item[0])
        speed = encode_speed(item[1])
        state = item[2]
        data_dt.append((dist,speed,state))
        print(item)
    
    #print data out
    print("a. Take population and convert it to distance and speed for calculation of DT  \n \n ")
    
    sys_output.print_collection(data_dt,len(data_dt))
   
    #conver to dataFrame 
    dfObj_tmp = pd.DataFrame(data_dt) 
   
  
    dfObj = dfObj_tmp.set_axis(['distance', 'speed', 'state'], axis=1, inplace=False)
 
    one_hot_data_dist = pd.get_dummies(dfObj['distance'])
    one_hot_data_speed = pd.get_dummies(dfObj['speed'])
    
    #data has format
    #dist_bw_20_30  dist_bw_30_40  dist_gt_40  dist_lt_20  speed_bw_20_40  speed_bw_40_60  speed_gt_60  state
    data_training_DT_temp = pd.concat([one_hot_data_dist,one_hot_data_speed,dfObj['state']],axis=1,sort=False)

    data_training_DT = check_dataFrame(data_training_DT_temp)
    print ("\n Convert data to dataframe to train DT \n", data_training_DT )
    
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
                                 min_impurity_decrease=1e-07, min_samples_leaf=1,
                                 min_samples_split=2, min_weight_fraction_leaf=0.0,
                                 presort=False, random_state=None, splitter='best')

    # Train Decision Tree Classifer
    #clf = clf.fit(X_train,y_train)
    
    clf = clf.fit(X,y)
    visualize_data(clf,feature_name)
    n_nodes = clf.tree_.node_count
   
    children_left = clf.tree_.children_left
    children_right = clf.tree_.children_right
    feature = clf.tree_.feature
    threshold = clf.tree_.threshold
    print ("**************************** DT *******************************")
    print("children_left : ", children_left)
    print("children_right : ", children_right)
    print("feature : ", feature)
    print("threshold : ", threshold)
       
    filter_index_df = [] 
    #consider 2 case: there are only one node and there are many nodes
    if n_nodes > 1: 
        rules, path_values = get_rules(clf,df)
        # print information about tree 
        print ("\n     Number node of Tree:", n_nodes)
        print ("\n     List of rules in the Tree:\n ")
        sys_output.print_collection(rules,len(rules))
        print("\n      Number [safety_scenario, critical_scenario] in each node of tree:\n")
        print(clf.tree_.value)
        
        #get index of sample in collision node
        # path_value is a list of numpy array
        print ("\n     Check nodes that critical events are larger than 50% on total Scenarios\n ")
        print ("\n     List of nodes is selected in Decision Tree:")
        counter = 0

        for  idx, path_value in  enumerate(path_values):
            
            if check_to_get_node_coll(path_value):
                counter += 1
                print ("     ", path_value[len(path_values) -1])
                items = eval(to_code(var_df,rules[idx]))
                print ("\n Select data from leaf node: \n %s" %items)
                for index,row in items.iterrows():
                    filter_index_df.append(index)
    else:
        sys_output.warning("There is only one node in decision tree. \
                \nThus, NSGAII could not explore critical events from Decision Tree ")
       
        filter_index_df = [i for i in range(df.shape[0])]
        print("\n Data frame \n")
        for i in df:
            print (i)
            
    # return index of population
    return filter_index_df       

    
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

    #save tree
    path_dir = os.getcwd()   
    now = datetime.now()    
    date_time = now.strftime("%m_%d_%Y__%H%M%S")
    
    graph.write_png(path_dir +"\store\\tree_" + date_time+".png")
    sys_output.print_sub_tit("The graph of tree is save in " + path_dir +"\store\\tree_" + date_time+".png" )

    
def get_rules(dtc, df):
    """
    This function takes rule from decision tree
    """
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
    
    print ("#########query",string_to_cod )
    return string_to_cod


def get_max_critical (tree_nodes):
    """
    The function will return the node which has max value of critical event (except root node)
    """
    _max = 0
    dim = tree_nodes.shape
    if (tree_nodes.size >1):
        list_critical = np.zeros(dim[0]-1)
    
        #don't get the first node from the tree
   
        for i in range(1, dim[0]):
            list_critical[i-1] = tree_nodes[i][0][1]
        
    _max = np.argmax(list_critical)
    return _max

def check_to_get_node_coll(path_list):
   
    
    last_id = len(path_list) -1
    value = path_list[last_id]
    
    #number of collision bigger than number of safe scenarios
    if value[0:1][0][0] < value[0:1][0][1]:
        return 1
    else:
        return 0


   
