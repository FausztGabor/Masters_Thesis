import pandas as pd

# Load the data
qam = pd.read_csv('Data3\\Logs\\64QAM_meas.csv', sep=';')
qpsk = pd.read_csv('Data2\\Logs\\1_2QPSK_meas.csv', sep=';')

# Create a DataFrame
Latency = pd.DataFrame({'QAM':qam['Latency'], 'QPSK':qpsk['Latency']})

# Calculate and print the mean latency for QAM and QPSK
print(f' QAM latency mean: {Latency["QAM"].mean()} \n QPSK latency: {Latency["QPSK"].mean()}')