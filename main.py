import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import statistics

def queueServerSimulation(numberOfRecords):

    uniformMinimum = 0
    uniformMaximum = 10
    gaussianMean = 10
    gaussianSigma = 5

    runningServiceTime = 0
    numberOfServers = 1

    simulationData = pd.DataFrame(columns=['interArrivalTime', 'arrivalTime', 'waitingTime', 'timeOfService', 'servingTime', 'departureTime', "queueLength"])

    for i in range(numberOfRecords):
        #1
        #simulationData.at[i, 'interArrivalTime'] = round(np.random.uniform(2, 8),2)
        #simulationData.at[i, 'servingTime'] = round(abs(np.random.uniform(0.05, 0.15)),3)

        #2
        simulationData.at[i, 'interArrivalTime'] = round(np.random.uniform(2, 8),2)
        simulationData.at[i, 'servingTime'] = round(abs(np.random.normal(5, 1.5)),2)

        #3
        #simulationData.at[i, 'interArrivalTime'] = round(np.random.uniform(2, 8),2)
        #simulationData.at[i, 'servingTime'] = round(abs(np.random.normal(5, 5)),2)
        
        #simulationData.at[i, 'interArrivalTime'] = round(np.random.uniform(uniformMinimum, uniformMaximum),2)
        #simulationData.at[i, 'servingTime'] = round(abs(np.random.normal(gaussianMean, gaussianSigma)),2)

        if(i>0):

            simulationData.at[i, 'arrivalTime'] = simulationData.loc[i-1]['arrivalTime'] + simulationData.loc[i]['interArrivalTime']
            simulationData.at[i, 'waitingTime'] = max(simulationData.loc[i - 1]['departureTime'] - simulationData.loc[i]['arrivalTime'],0)

        else:

            simulationData.at[i, 'arrivalTime'] = simulationData.loc[i]['interArrivalTime']
            simulationData.at[i, 'waitingTime'] = 0

        simulationData.at[i, 'timeOfService'] = simulationData.loc[i]['arrivalTime'] + simulationData.loc[i]['waitingTime']
        simulationData.at[i, 'departureTime'] = simulationData.loc[i]['timeOfService'] + simulationData.loc[i]['servingTime']

        lastCustomerDeparture = simulationData.loc[i]['departureTime']
        runningServiceTime += simulationData.loc[i]['servingTime']

        utilizationFactor = runningServiceTime/lastCustomerDeparture
        averageWaitingTime = round(simulationData['waitingTime'].mean(),2)
        averageTimeInSystem = round(statistics.mean(simulationData['departureTime'] - simulationData['arrivalTime']),2)


    # Calculating Queue length for each record
    for i in range(numberOfRecords):
        departureTime = simulationData.loc[i]['departureTime']
        queueLength = 0

        for j in range(i+1,numberOfRecords):
            if(simulationData.loc[j]['arrivalTime'] < departureTime):
                queueLength+=1

                # this.record = Last Record => Store Queue length
                if (j == numberOfRecords - 1):
                    simulationData.at[i, 'queueLength'] = queueLength
                    queueLength = 0

            else:
                simulationData.at[i, 'queueLength'] = queueLength
                break;

        averageQueueLength = round(simulationData['queueLength'].mean(),2)
        averageNumberSystem = averageQueueLength + numberOfServers


    simulationData.plot.line(y="queueLength");
    simulationData.plot.line(y="waitingTime");
    plot.show()

    #Print entire Dataframe
    print(simulationData.to_string())

    #Print Dataframe Summary
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(simulationData)

    print('\n\nUtilization Factor : \t\t\t', utilizationFactor)
    print('Average Number in Queue : \t\t', averageQueueLength)
    print('Average Number in the System : \t', averageNumberSystem)
    print('Average Waiting Time : \t\t\t', averageWaitingTime)
    print('Average Time in the System : \t', averageTimeInSystem)



queueServerSimulation(1000)

## List columns
## 0 - Inter Arrival Time
## 1 - Arrival Time = prevArrivalTime + interArrivalTime
## 2 - Waiting Time = prevDepartuteTime - arrivalTime
## 3 - Time of Service = arrivalTime + waitingTime
## 4 - Serving Time
## 5 - Departure Time = timeOfService  + servingTime
## 6 - Queue Length