import sys, os
ROOT_PATH = os.path.abspath(".")
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

import pathlib
#print(pathlib.Path(__file__).parent.absolute())
#print(pathlib.Path().absolute())

import warnings
# this disables a warning in sklearn for linear models:
# FutureWarning: The default value of multioutput 
# (not exposed in score method) will change from 
# 'variance_weighted' to 'uniform_average' in 0.23 
# to keep consistent with 'metrics.r2_score'. 
# To specify the default value manually and avoid the warning, 
# please either call 'metrics.r2_score' directly or make a 
# custom scorer with 'metrics.make_scorer' 
# (the built-in scorer 'r2' uses multioutput='uniform_average').
warnings.simplefilter(action='ignore', category=FutureWarning)

from keras.models import load_model
from keras.callbacks.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.utils import plot_model

from howiml.utils import plots
from howiml.utils import prints
import pickle
import numpy as np
import math
import random

def printModelSummary(model):
    # Prints the model summary of a machine learning model
    # The model summary is a list of structure and number of parameters

    if hasattr(model, "summary"):
        # Keras Model object
        print(model.summary())
    elif hasattr(model, "model"):
        # MachineLearningModel object
        if hasattr(model.model, "summary"):
            # MachineLearningModel.model will be a Keras Model object
            printModelSummary(model.model)
    elif hasattr(model, "models"):
        # EnsembleModel object
        print("Model is of type Ensemble Model")
        print("Sub model summaries will follow")
        print("-------------------------------")
        for mod in model.models:
            # EnsembleModel.models will be a list of MachineLearningModels
            printModelSummary(mod)
    else:
        print("Simple models have no summary")
    
def printModelWeights(model):
    # Prints the model weights of a machine learning model
    # The model weights combined with the model architecture is what calculates the output

    if hasattr(model, "summary"):
        # Keras Model object
        for layer in model.layers: print(layer.get_config(), layer.get_weights())
    elif hasattr(model, "model"):
        # MachineLearningModel object
        if hasattr(model.model, "summary"):
            # MachineLearningModel.model will be a Keras Model object
            printModelWeights(model.model)
    elif hasattr(model, "models"):
        # EnsembleModel object
        print("Model is of type Ensemble Model")
        print("Sub model summaries will follow")
        print("-------------------------------")
        for mod in model.models:
            # EnsembleModel.models will be a list of MachineLearningModels
            printModelWeights(mod)
    else:
        if hasattr(model, "get_params"):
            print(model.get_params())
        else:
            print("No weights found")

def plotKerasModel(model):
    # Plots models using the built-in Keras plotting function

    plot_model(model.model)

def getBasicCallbacks(monitor="val_loss", patience_es=200, patience_rlr=80):
    # Two callbacks are used by default for all models:
    # - EarlyStopping (stop training when validation loss increases)
    # - ReduceLROnPlateau (reduce learning rate to facilitate continued learning)

    return [
        EarlyStopping(
            monitor = monitor, min_delta = 0.00001, patience = patience_es, mode = 'auto', restore_best_weights=True
        ),
        ReduceLROnPlateau(
            monitor = monitor, factor = 0.5, patience = patience_rlr, verbose = 1, min_lr=5e-4,
        )
    ]

def getBasicHyperparams():
    # Some default hyperparameters used

    return {
        'activation': 'relu',
        'loss': 'mean_squared_error',
        'optimizer': 'adam',
        'metrics': ['mean_squared_error'],
    }

def trainModels(modelList, filename, targetColumns, retrain=False, save=True):
    # Trains or loads each model of a provided list of models

    if retrain:
        for mod in modelList:
            print("Training model " + mod.name)
            mod.train()
    else:
        for mod in modelList:
            if mod.modelType != "Ensemble":
                loadedModel, loadedHistory = loadModel(mod.name, filename, targetColumns)
                if loadedModel is not None:
                    print("Model " + mod.name + " was loaded from file")
                    mod.model = loadedModel
                    mod.history = loadedHistory
                else:
                    print("Training model " + mod.name)
                    mod.train()
            else:
                for model in mod.models:
                    loadedModel, loadedHistory = loadModel(model.name, filename, targetColumns, ensembleName=mod.name)
                    if loadedModel is not None:
                        print("Model " + mod.name + " was loaded from file")
                        model.model = loadedModel
                        model.history = loadedHistory
                    else:
                        print("Training submodel " + model.name + " of Ensemble " + mod.name)
                        model.train()

                mod.trainEnsemble()

    if save:
        saveModels(modelList, filename, targetColumns)

    trainingSummary = getTrainingSummary(modelList)
    if trainingSummary:
        prints.printTrainingSummary(trainingSummary)
        plots.plotTrainingSummary(trainingSummary)

def loadModel(modelname, filename, targetColumns, ensembleName=None):
    # Loads a single model based on a defined modelname-filename-targetColumns combination

    subdir = filename.split('/')[-2]
    datafile = filename.split('/')[-1].split('.')[0]
    joinedColumns = "_".join(targetColumns)
    
    modName = "_".join(modelname.split(' '))
    
    if ensembleName is None:
        directory = ROOT_PATH + '/howiml/ml/trained_models/' + subdir + '/' + datafile + '/' + modName + '_' + joinedColumns
    else:    
        ensName = "_".join(ensembleName.split(' '))
        directory = ROOT_PATH + '/howiml/ml/trained_models/' + subdir + '/' + datafile + '/' + ensName + '_' + joinedColumns + '/' + modName
    
    if os.path.isfile((directory + ".h5")) and os.path.isfile((directory + ".h5")):
        model = load_model(directory + ".h5")
        history = pickle.load(open(directory + ".pickle", "rb"))
    else:
        model = None
        history = None
    return [model, history]

def saveModels(modelList, filename, targetColumns):
    # Saves each model of a provided list of models

    subdir = filename.split('/')[-2]
    datafile = filename.split('/')[-1].split('.')[0]
    joinedColumns = "_".join(targetColumns)
    
    for model in modelList:
        modName = "_".join(model.name.split(' '))
        directory = ROOT_PATH + '/howiml/ml/trained_models/' + subdir + '/' + datafile + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        modelPath = directory
        modelName = modName + '_' + joinedColumns
        metricsPath = directory + modName + '_' + joinedColumns + ".txt"
        model.save(modelPath, modelName)

def getTrainingSummary(modelList):
    # Calculates relevant metrics such as validation loss, loss and length of model training

    loss_dict = {}
    modelNames = list(map(lambda mod: mod.name, modelList))
    for model in modelList:
        if model.modelType != "Ensemble":
            if model.history is not None:
                loss = model.history['loss']
                val_loss = model.history['val_loss']
                loss_best = np.amin(loss)
                loss_loc = np.where(loss == loss_best)[0]
                val_loss_best = np.amin(val_loss)
                val_loc = np.where(val_loss == val_loss_best)[0]
                loss_actual = loss[val_loc[0]]
                loss_dict[model.name] = {
                    'loss': loss,
                    'val_loss': val_loss,
                    'loss_final': loss_best,
                    'loss_loc': loss_loc,
                    'loss_actual': loss_actual,
                    'val_loss_final': val_loss_best,
                    'val_loss_loc': val_loc,
                    'length': len(loss),
                }
        else:
            for submodel in model.models:
                if submodel.history is not None and submodel.name not in modelNames:
                    loss = submodel.history['loss']
                    val_loss = submodel.history['val_loss']
                    loss_best = np.amin(loss)
                    loss_loc = np.where(loss == loss_best)[0]
                    val_loss_best = np.amin(val_loss)
                    val_loc = np.where(val_loss == val_loss_best)[0]
                    loss_actual = loss[val_loc[0]]
                    loss_dict[model.name + ", " + submodel.name] = {
                        'loss': loss,
                        'val_loss': val_loss,
                        'loss_final': loss_best,
                        'loss_loc': loss_loc,
                        'loss_actual': loss_actual,
                        'val_loss_final': val_loss_best,
                        'val_loss_loc': val_loc,
                        'length': len(loss),
                    }
    return loss_dict

def getRNNSplit(x_data, y_data, lookback, validation_split=0.2):
    # Splits a dataset into training and validation data for use in RNN networks
    # By default, 20% of data is used for validation

    num_x_signals = x_data.shape[1]
    num_y_signals = y_data.shape[1]

    num_x_samples = x_data.shape[0]
    num_y_samples = y_data.shape[0]

    length_valid = math.ceil(num_x_samples * validation_split)
    length_train = num_x_samples - length_valid

    x_shape_train = (length_train, lookback, num_x_signals)
    x_shape_val = (length_valid, lookback, num_x_signals)

    X = np.zeros(shape=x_shape_train, dtype=np.float16)
    X_val = np.zeros(shape=x_shape_val, dtype=np.float16)

    y_shape_train = (length_train, num_y_signals)
    y_shape_val = (length_valid, num_y_signals)

    Y = np.zeros(shape=y_shape_train, dtype=np.float16)
    Y_val = np.zeros(shape=y_shape_val, dtype=np.float16)

    train_samples = random.sample(range(num_x_samples-lookback), length_train)
    samples = list(range(num_x_samples-lookback))
    valid_samples = list(set(samples)-set(train_samples))    

    for i, sample in enumerate(train_samples):
        X[i] = x_data[sample:sample+lookback]
        Y[i] = y_data[sample+lookback]
    for i, sample in enumerate(valid_samples):
        X_val[i] = x_data[sample:sample+lookback]
        Y_val[i] = y_data[sample+lookback]

    return [X, X_val, Y, Y_val]