from howiml.utils import utilities
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

colors = list(utilities.getColorScheme().values())
sns.set(context='paper', style='whitegrid', palette=sns.color_palette(colors))

def correlationMatrix(df):
    # Calculates correlation matrix of a pandas dataframe

    if 'Date' in df.columns:
        df = df.drop('Date', axis=1, inplace=False)
    if 'Index' in df.columns:
        df = df.drop('Index', axis=1, inplace=False)

    X = df.values
    standardScaler = StandardScaler()
    X = standardScaler.fit_transform(X)
    covMat = np.cov(X.T)

    return covMat

def pca(df, numberOfComponents, relevantColumns=None, columnDescriptions=None):
    # Calculates Principal Component Analysis of a pandas dataframe

    if 'Date' in df.columns:
        df = df.drop('Date', axis=1, inplace=False)
    if 'Index' in df.columns:
        df = df.drop('Index', axis=1, inplace=False)

    X = df.values
    standardScaler = StandardScaler()
    X = standardScaler.fit_transform(X)

    if numberOfComponents < 1 or numberOfComponents > df.shape[1]:
        numberOfComponents = df.shape[1]

    pca = PCA(n_components=numberOfComponents)
    pca.fit(X)

    return pca

def pcaPlot(df, timestamps=None, plotTitle=None):
    # Calculates and plots a 2D Principal Component Analysis decomposition of a pandas dataframe

    if timestamps is not None:
        traintime, testtime, validtime = timestamps
        df_train, df_test = utilities.getTestTrainSplit(df, traintime, testtime)
        train_vals = df_train.values
    else:
        train_vals = df.values

    sc = StandardScaler()
    train_vals = sc.fit_transform(train_vals)
    
    numberOfComponents = 2

    pca = PCA(n_components=numberOfComponents)
    pca.fit(train_vals)

    X = df.values
    X = sc.transform(X)
    X = pca.transform(X)

    df_pca = pd.DataFrame(data = X, index=df.index, columns=['pca1', 'pca2'])
    if timestamps is not None:
        df_pca_train, df_pca_test = utilities.getTestTrainSplit(df_pca, traintime, testtime)
    else:
        df_pca_train, df_pca_test = None, df_pca

    fig = plt.figure(figsize = (8,4))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('PCA 1', fontsize=10)
    ax.set_ylabel('PCA 2', fontsize=10)
    ax.set_title(((plotTitle + '\n') if plotTitle is not None else '') + 'PCA plot', fontsize=12)
    cmap = sns.cubehelix_palette(as_cmap=True)
    indexx = list(range(df_pca_test.shape[0]))
    if df_pca_train is not None:
        ax.scatter(df_pca_train['pca1'], df_pca_train['pca2'], c = 'red')
    points = ax.scatter(df_pca_test['pca1'], df_pca_test['pca2'], c = indexx, cmap = cmap, alpha=0.7)
    fig.colorbar(points)
    plt.show()

def pcaDuoPlot(df_1_train, df_1_test, df_2_test, plotTitle=None):
    # Calculates and plots a 2D Principal Component Analysis decomposition
    #   based on one training and two testing pandas dataframes

    train_vals = df_1_train.values

    sc = StandardScaler()
    train_vals = sc.fit_transform(train_vals)
    
    numberOfComponents = 2

    pca = PCA(n_components=numberOfComponents)
    pca.fit(train_vals)

    X_1_train = df_1_train.values
    X_1_train = sc.transform(X_1_train)
    X_1_train = pca.transform(X_1_train)
    df_train1 = pd.DataFrame(data = X_1_train, index=df_1_train.index, columns=['pca1', 'pca2'])
    df_train1 = df_train1.resample("180min").mean()

    X_1_test = df_1_test.values
    X_1_test = sc.transform(X_1_test)
    X_1_test = pca.transform(X_1_test)
    df_test1 = pd.DataFrame(data = X_1_test, index=df_1_test.index, columns=['pca1', 'pca2'])
    df_test1 = df_test1.resample("180min").mean()

    X_2_test = df_2_test.values
    X_2_test = sc.transform(X_2_test)
    X_2_test = pca.transform(X_2_test)
    df_test2 = pd.DataFrame(data = X_2_test, index=df_2_test.index, columns=['pca1', 'pca2'])
    df_test2 = df_test2.resample("180min").mean()

    fig,axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4), dpi=100)
    fig.tight_layout(w_pad=3.0)

    ax, ax2 = axs
    
    ax.set_xlabel('PCA 1', fontsize=10)
    ax.set_ylabel('PCA 2', fontsize=10)
    ax.set_title(((plotTitle + '\n') if plotTitle is not None else '') + 'PCA plot timeseries part 1', fontsize=12)
    cmap1 = sns.cubehelix_palette(reverse=False, as_cmap=True)
    cmap2 = sns.cubehelix_palette(reverse=False, start=50.0, rot=0.1, as_cmap=True)
    index1 = list(range(df_test1.shape[0]))
    index2 = list(range(df_test2.shape[0]))
    ax.scatter(df_train1['pca1'], df_train1['pca2'], c = 'red', alpha=0.3)
    points1 = ax.scatter(df_test1['pca1'], df_test1['pca2'], c = index1, cmap = cmap1, alpha=1.0)
    
    fig.colorbar(points1, ax=ax)

    ax2.set_xlabel('PCA 1', fontsize=10)
    ax2.set_ylabel('PCA 2', fontsize=10)
    ax2.set_title(((plotTitle + '\n') if plotTitle is not None else "") + 'PCA plot timeseries part 2', fontsize=12)
    cmap1 = sns.cubehelix_palette(reverse=False, as_cmap=True)
    cmap2 = sns.cubehelix_palette(reverse=False, start=50.0, rot=0.1, as_cmap=True)
    index1 = list(range(df_test1.shape[0]))
    index2 = list(range(df_test2.shape[0]))
    ax2.scatter(df_train1['pca1'], df_train1['pca2'], c = 'red', alpha=0.3)
    points2 = ax2.scatter(df_test2['pca1'], df_test2['pca2'], c = index2, cmap = cmap2, alpha=1.0)
    
    fig.colorbar(points2, ax=ax2)
    plt.show()

def pairplot(df):
    # Plots 2D pair plots of all columns in a pandas dataframe

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df.values)
    scaled_df = pd.DataFrame(scaled, index=df.index, columns=df.columns)
    
    if scaled_df.shape[0] > 1000:
        scaled_df = scaled_df.resample('H').mean()
    sns.pairplot(scaled_df, vars=scaled_df.columns, height=1.1)
    plt.show()

def scatterplot(df):
    # Plots 2D scatter plots of all columns in a pandas dataframe

    pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.show()

def correlationPlot(df, title="Correlation plot"):
    # Plots the correlation matrix of a pandas dataframe

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df.values)
    scaled_df = pd.DataFrame(scaled, index=df.index, columns=df.columns)

    corr = scaled_df.corr()

    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    f, ax = plt.subplots(figsize=(5,5), dpi=100)

    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    sns.heatmap(corr, mask=mask, cmap=cmap,
                square=True, linewidths=1, cbar_kws={"shrink": .6}, vmin=-1, vmax=1)

    ax.set_title(title)
    
    plt.show()

def correlationDuoPlot(df1, df2, title1="Correlation plot", title2="Correlation plot"):
    # Plots the correlation matrix of two pandas dataframes side by side

    scaler1 = StandardScaler()
    scaled1 = scaler1.fit_transform(df1.values)
    scaled_df1 = pd.DataFrame(scaled1, index=df1.index, columns=df1.columns)
    
    scaler2 = StandardScaler()
    scaled2 = scaler2.fit_transform(df2.values)
    scaled_df2 = pd.DataFrame(scaled2, index=df2.index, columns=df2.columns)

    corr1 = scaled_df1.corr()
    corr2 = scaled_df2.corr()

    mask = np.zeros_like(corr1, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    fig,axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), dpi=100)
    fig.tight_layout(w_pad=8.0)

    ax1, ax2 = axs

    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    sns.heatmap(corr1, ax=ax1, mask=mask, cmap=cmap,
                square=True, linewidths=1, cbar_kws={"shrink": .6}, vmin=-1, vmax=1)
    sns.heatmap(corr1, ax=ax2, mask=mask, cmap=cmap,
                square=True, linewidths=1, cbar_kws={"shrink": .6}, vmin=-1, vmax=1)

    ax1.set_title(title1)
    ax2.set_title(title2)
    
    plt.show()

def correlationDifferencePlot(df1, df2, title="Correlation difference plot"):
    # Plots the correlation matrix difference between two pandas dataframes

    scaler1 = StandardScaler()
    scaled1 = scaler1.fit_transform(df1.values)
    scaled_df1 = pd.DataFrame(scaled1, index=df1.index, columns=df1.columns)
    scaler2 = StandardScaler()
    scaled2 = scaler2.fit_transform(df2.values)
    scaled_df2 = pd.DataFrame(scaled2, index=df2.index, columns=df2.columns)

    corr1 = scaled_df1.corr()
    corr2 = scaled_df2.corr()
    corr_diff = corr1.sub(corr2)

    mask = np.zeros_like(corr_diff, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    f, ax = plt.subplots(figsize=(5,5), dpi=100)

    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    sns.heatmap(corr_diff, mask=mask, cmap=cmap,
                square=True, linewidths=1, cbar_kws={"shrink": .6}, vmin=-1, vmax=1)

    ax.set_title(title)
    
    plt.show()

def valueDistributionSingle(df, traintime, testtime):
    # Plots values and value distributions for a pandas dataframe
    # NB: all plots are put in a single figure with n rows

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df.values)
    scaled_df = pd.DataFrame(scaled, index=df.index, columns=df.columns)

    df_train, df_test = utilities.getTestTrainSplit(scaled_df, traintime, testtime)    

    height = df_train.shape[-1]*5
    fig, axs = plt.subplots(nrows=df_train.shape[-1], ncols=2, figsize=(15,height), dpi=100)
    #fig.tight_layout()
    
    for k in range(df_train.shape[-1]):
        ax1, ax2 = axs[k, 0], axs[k, 1]
        
        trainEndStr=[item for sublist in traintime for item in sublist]
        for i, trainEndString in enumerate(trainEndStr):
            ax1.axvline(x=pd.to_datetime(trainEndString, dayfirst=True), color='black' if i % 2 == 0 else 'blue', label='start training' if i % 2 == 0 else 'end training')
    
        ax1.plot(df_train.iloc[:,k], label="train",
                marker="o", ms=1.5, lw=0)
        ax1.plot(df_test.iloc[:,k], label="test",
                marker="o", ms=1.5, lw=0)
        
        ax1.set_xticks(ax1.get_xticks()[3::3])
        ax1.set_ylabel(df_train.columns[k])
        
        sns.distplot(df_train.iloc[:,k], ax=ax2, label="train", kde=True, kde_kws={"lw":2.5})
        sns.distplot(df_test.iloc[:,k], ax=ax2, label="test", kde=True, kde_kws={"lw":2.5})
        
        ax2.set_xlim((-3,3))
        ax2.legend(loc="upper right")

    plt.show()

def valueDistribution(df, traintime, testtime, columnDescriptions, columnUnits):
    # Plots values and value distributions for a pandas dataframe
    # NB: all columns are plotted in separate figures

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df.values)
    scaled_df = pd.DataFrame(scaled, index=df.index, columns=df.columns)

    df_train, df_test = utilities.getTestTrainSplit(scaled_df, traintime, testtime)    

    for k, column in enumerate(df_train.columns):
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10,3.0), dpi=100)
        #fig.tight_layout()
        ax1, ax2 = axs[0], axs[1]
        
        fig.suptitle(column + " " + columnDescriptions[column])

        trainEndStr=[item for sublist in traintime for item in sublist]
        for i, trainEndString in enumerate(trainEndStr):
            ax1.axvline(x=pd.to_datetime(trainEndString, dayfirst=True), color='black' if i % 2 == 0 else 'blue', label='start training' if i % 2 == 0 else 'end training')
    

        ax1.plot(df_train.iloc[:,k], label="train",
                marker="o", ms=1.5, lw=0)
        ax1.plot(df_test.iloc[:,k], label="test",
                marker="o", ms=1.5, lw=0)
        
        ax1.set_xticks(ax1.get_xticks()[3::3])
        ax1.set_ylabel(columnUnits[column] + ", standardized")
        ax1.set_xlabel('Date')
        
        sns.distplot(df_train.iloc[:,k], ax=ax2, label="train", kde=True, kde_kws={"lw":2.5})
        sns.distplot(df_test.iloc[:,k], ax=ax2, label="test", kde=True, kde_kws={"lw":2.5})
        
        ax2.set_xlim((-3,3))
        ax2.legend(loc="upper right")
        ax2.set_ylabel('Ratio')
        ax2.set_xlabel(columnUnits[column] + ", standardized")

        plt.show()
