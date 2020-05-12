import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# Enter the file name here
df = pd.read_csv('current.csv')
abbv = pd.read_csv('abbv.csv', index_col='State')
state_pop = pd.read_csv('population.csv', index_col='State')

state_tests = df[['state','total','positive']]
state_tests = state_tests.set_index('state')
state_pop = state_pop.join(abbv, on='State')
state_pop_abbv = state_pop[['Pop', 'Abbreviation']]
state_tests = state_tests.join(state_pop_abbv.set_index('Abbreviation'))
state_tests['tested_pop'] = state_tests['total']/state_tests['Pop']
state_tests['positive_tests'] = state_tests['positive']/state_tests['total']
state_tests = state_tests.sort_values('tested_pop', ascending=False).dropna()
state_tests = state_tests.drop(['PR'])

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('State')
ax1.set_ylabel('Population Tested (%)', color=color)
ax1.bar(state_tests.index.values, state_tests['tested_pop'], color=color, alpha=0.2)
ax1.tick_params(axis='y', labelcolor=color)
ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('Positive Results (%)', color=color)
ax2.plot(state_tests.index.values, state_tests['positive_tests'], color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.show()