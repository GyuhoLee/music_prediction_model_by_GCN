import numpy as np
import scipy.sparse as sp
import torch, csv
import pandas as pd
from sklearn import preprocessing

def sparse_mx_to_torch_sparse_tensor(sparse_mx):
    """Convert a scipy sparse matrix to a torch sparse tensor."""
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse.FloatTensor(indices, values, shape)

def load_data():
    x = []
    f = open('data/data_x.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        x.append(line)
    
    y = []
    f = open('data/data_y.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        y.append(line)

    raw_data = np.array(x, dtype=np.float32)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(raw_data)
    df = pd.DataFrame(x_scaled)
    x_data = np.array(df, dtype=np.float32)
    
    features = sp.csr_matrix(np.array(x_data), dtype=np.float32)
    labels = np.array(y, dtype=np.float32)
    labels = labels / 100

    edge_list = []
    f = open('data/data_edge.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        edge_list.append(line)
    edges_unordered =  np.array(edge_list, dtype=np.int32)

    idx_map = {i : i for i, j in enumerate(range(len(y)))}
    edges = np.array(list(map(idx_map.get, edges_unordered.flatten())),
                    dtype=np.int32).reshape(edges_unordered.shape)
    adj = sp.coo_matrix((np.ones(edges.shape[0]), (edges[:, 0], edges[:, 1])),
                    shape=(labels.shape[0], labels.shape[0]),
                    dtype=np.float32)
    # build symmetric adjacency matrix
    adj = adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)

    features = torch.FloatTensor(np.array(features.todense()))
    labels = torch.FloatTensor(np.array(labels))
    adj = sparse_mx_to_torch_sparse_tensor(adj)
    idx_train = [i for i in range(len(y)) if i % 10 != 0]
    idx_test = [i for i in range(len(y)) if i % 10 == 0]
    idx_train = torch.LongTensor(idx_train)
    idx_test = torch.LongTensor(idx_test)

    return adj, features, labels, idx_train, idx_test

def accuracy(output, labels):
    o = output.detach().numpy()
    l = labels.detach().numpy()
    o = [max(i, 0) for i in o]
    o = [min(i, 1) for i in o]
    correct = sum([abs(i - j) <= 0.1 for i, j in zip(o, l)])
    return correct / len(labels)

def accuracy_per(output, labels, num):
    o = output.detach().numpy()
    l = labels.detach().numpy()
    o = [max(i, 0) for i in o]
    o = [min(i, 1) for i in o]
    correct = sum([abs(i - j) <= num / 100 for i, j in zip(o, l)])
    return correct / len(labels)