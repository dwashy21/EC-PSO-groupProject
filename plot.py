import matplotlib.pyplot as plt


def createPlot(max_fit, avg_fit):
    #max_fit = [1,2,4,4,5,6,7,8]
    #avg_fit = [1,2,2,2.5,5,4,5,5]
    plt.plot(max_fit,'b--')
    plt.plot(avg_fit,'r')
    plt.legend(['Max Fitness Overall','Average Fitness in Current Generation'], loc='upper left')
    plt.ylabel('Fitness Score')
    plt.xlabel('Generation Number')
    plt.title('Average and Maximum Fitness Score Over Generations')
    #plt.show()
    plt.savefig('plot.png')
