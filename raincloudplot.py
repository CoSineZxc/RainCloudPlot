import numpy as np
import matplotlib.pyplot as plt

colors_lib = ['#F27970','#BB9727','#54B345','#32B897','#05B9E2','#8983BF',
              '#C76DA2','#934B43','#D76364','#EF7A6D','#F1D77E','#B1CE46',
              '#63E398','#9394E7','#5F97D2','#9DC3E7','#A1A9D0','#F0988C',
              '#B883D4','#9E9E9E','#CFEAF1','#C4A5DE','#F6CAE5','#96CCCB']

def Crt_normal_array(low, high, size):
    mean = (low + high) / 2  # Mean is at the center of the range
    std = (high - low) / 6  # 99.7% of data in range (mean ± 3*std)
    # Generate normally distributed values
    data = np.random.normal(mean, std, size)
    return data

def raincloudplot(data,label,fig_width=8,fig_height=4,color_map=colors_lib,
                  if_vert=True,box_alpha=0.3,scatter_size=1,scatter_alpha=0.8,
                  xlabel='group',ylabel='value',title="Raincloud plot",figname='',
                  show_mean=True,mean_color='red',y_lim=[]):
    if len(data)!=len(label):
        print("ERROR: data doesn't match label")
        return
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Create a list of colors for the boxplots based on the number of features you have
    boxplots_colors=color_map[0:len(data)]
    
    # Customize mean properties (marker style and color)
    mean_props = dict(marker='o', markerfacecolor=mean_color, markeredgecolor=mean_color, markersize=7)
    
    # Boxplot data
    bp = ax.boxplot(data, patch_artist = True, vert = if_vert,showmeans=show_mean,meanprops=mean_props)
    
    # Change to the desired color and add transparency
    for patch, color in zip(bp['boxes'], boxplots_colors):
        patch.set_facecolor(color)
        patch.set_alpha(box_alpha)
    
    # Create a list of colors for the violin plots based on the number of features you have
    violin_colors = color_map[0:len(data)]
    
    # Violinplot data
    vp = ax.violinplot(data, points=500, 
                   showmeans=False, showextrema=False, showmedians=False, vert=if_vert)
    
    for idx, b in enumerate(vp['bodies']):
        if if_vert==True:
            # Get the center of the plot
            m = np.mean(b.get_paths()[0].vertices[:, 1])
            # Modify it so we only see the upper half of the violin plot
            b.get_paths()[0].vertices[:, 0] = np.clip(b.get_paths()[0].vertices[:, 0], idx+1, idx+2)
        else:
            # Get the center of the plot
            m = np.mean(b.get_paths()[0].vertices[:, 0])
            # Modify it so we only see the upper half of the violin plot
            b.get_paths()[0].vertices[:, 1] = np.clip(b.get_paths()[0].vertices[:, 1], idx+1, idx+2)
        # Change to the desired color
        b.set_color(violin_colors[idx])
    
    # Create a list of colors for the scatter plots based on the number of features you have
    scatter_colors = color_map[0:len(data)]
    
    # Scatterplot data
    for idx, features in enumerate(data):
        # Add jitter effect so the features do not overlap on the y-axis
        x = np.full(len(features), idx + 1)
        idxs = np.arange(len(x))
        out = x.astype(float)
        out.flat[idxs] += np.random.uniform(low=-.05, high=.05, size=len(idxs))
        x = out
        if if_vert==True:
            plt.scatter(x,features, s=scatter_size, c=scatter_colors[idx],alpha=scatter_alpha)
        else:
            plt.scatter(features,x, s=scatter_size, c=scatter_colors[idx],alpha=scatter_alpha)
       
    if if_vert==True:
        plt.xticks(np.arange(1,len(label)+1,1), label)  # Set text labels.
    else:
        plt.yticks(np.arange(1,len(label)+1,1), label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if y_lim!=[]:
        plt.ylim(y_lim)
    if figname!='':
        plt.savefig(figname,dpi=600,format='svg',bbox_inches='tight')
    plt.show()

if __name__=='__main__':
    x1=Crt_normal_array(2,5,20)
    x2=Crt_normal_array(6,13,20)
    x3=Crt_normal_array(5,10,20)
    x4=Crt_normal_array(2,5,20)
    x5=Crt_normal_array(6,13,20)
    x6=Crt_normal_array(5,10,20)
    x7=Crt_normal_array(5,10,20)
    data_x = [x1, x2,x3,x4, x5,x6,x7]
    raincloudplot(data_x,['X1','X2','X3','X4','X5','X6','X7'],
                  fig_width=10,fig_height=5,scatter_size=10,figname='./output.svg')
    