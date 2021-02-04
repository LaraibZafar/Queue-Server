import numpy as np
import pandas as pd
import statistics

def queueServerSimulation(numberOfRecords):

    uniformMinimum = 0
    uniformMaximum = 10
    gaussianMean = 10
    gaussianSigma = 5

    runningServiceTime = 0
    firstCustomerArrival = 0
    lastCustomerDeparture = 0


    simulationData = pd.DataFrame(columns=['interArrivalTime', 'arrivalTime', 'waitingTime', 'timeOfService', 'servingTime', 'departureTime', "queueLength"])

    for i in range(numberOfRecords):

        simulationData.at[i, 'interArrivalTime'] = np.random.uniform(uniformMinimum, uniformMaximum)
        simulationData.at[i, 'servingTime'] = abs(np.random.normal(gaussianMean, gaussianSigma))

        if(i>0):

            simulationData.at[i, 'arrivalTime'] = simulationData.loc[i-1]['arrivalTime'] + simulationData.loc[i]['interArrivalTime']
            simulationData.at[i, 'waitingTime'] = simulationData.loc[i - 1]['departureTime'] - simulationData.loc[i]['arrivalTime']

        else:

            simulationData.at[i, 'arrivalTime'] = simulationData.loc[i]['interArrivalTime']
            simulationData.at[i, 'waitingTime'] = 0
            firstCustomerArrival = simulationData.loc[i]['arrivalTime']

        simulationData.at[i, 'timeOfService'] = simulationData.loc[i]['arrivalTime'] + simulationData.loc[i]['waitingTime']
        simulationData.at[i, 'departureTime'] = simulationData.loc[i]['timeOfService'] + simulationData.loc[i]['servingTime']

        lastCustomerDeparture = simulationData.loc[i]['departureTime']
        runningServiceTime += simulationData.loc[i]['servingTime']

        utilizationFactor = runningServiceTime/(lastCustomerDeparture - firstCustomerArrival)
        averageWaitingTime = simulationData['waitingTime'].mean()
        averageTimeInSystem = statistics.mean(simulationData['departureTime'] - simulationData['arrivalTime'])


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

        averageQueueLength = simulationData['queueLength'].mean()
        averageNumberSystem = -1


    print(simulationData.to_string())
    print('\n\nUtilization Factor : ',utilizationFactor)
    print('Average Number in Queue : ', averageQueueLength)
    print('Average Number in the System : ', averageNumberSystem)
    print('Average Waiting Time : ', averageWaitingTime)
    print('Average Time in the System : ', averageTimeInSystem)



queueServerSimulation(100)

## List columns
## 0 - Inter Arrival Time
## 1 - Arrival Time = prevArrivalTime + interArrivalTime
## 2 - Waiting Time = prevDepartuteTime - arrivalTime
## 3 - Time of Service = arrivalTime + waitingTime
## 4 - Serving Time
## 5 - Departure Time = timeOfService  + servingTime
## 6 - Queue Length