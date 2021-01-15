###########
# Imports #
###########

from random import randint

import simpy

##################
# Global Variables#
##################

hours = 0
days = []
months = 0
total_profit = []
total_profit_count = 0      # used as index for total profit list
require_profit = 400000     # The profit we simulate to reach
customer_count = 0          # The number of customers in all months
flag = False                # if we reach the require profit the flag gets TRUE, the the simulation terminates
customer_arrival = []       # this is a list of customers numbers over all the days
g = [0, 0, 0, 0, 0]         # this is a list for games load chart
number_of_simulation = 3


#########
# Games #
#########

Games = {
    0: {'name': 'Game1', 'capacity': 10, 'price': 2, 'time_to_finish': 10},
    1: {'name': 'Game2', 'capacity': 5, 'price': 3, 'time_to_finish': 15},
    2: {'name': 'Game3', 'capacity': 1, 'price': 8, 'time_to_finish': 20},
    3: {'name': 'Game4', 'capacity': 2, 'price': 5, 'time_to_finish': 15},
    4: {'name': 'Game5', 'capacity': 2, 'price': 4, 'time_to_finish': 30},
}

###############
# Monthly costs#
###############

Park_place_installment = 2000
Employees_monthly_salaries = 5000
Electricity_and_other_services = 3000
Tax = .14
Park_open_and_close = 12


###############
# Random Values#
###############

# This function generates the interarrival time
def get_Customers_next_interarrival():
    return randint(0, 10)


# This function generates a random number between 0 and 100, to help us in any percentage
def get_others_next_interarrival():
    return randint(0, 100)  # 0 and 100 are included


# This function determine the type of ticket according to the random number
def get_ticket_types():
    randN = get_others_next_interarrival()
    if randN <= 60:
        return "normal"
    else:
        return "special"


# This function returns number of Games the customer plays
def get_number_of_games():
    randN = get_others_next_interarrival()
    if randN <= 20:
        return 1
    elif randN <= 60:
        return 2
    elif randN <= 90:
        return 3
    else:
        return 4


# This function update the game load list and returns the a Game among the five Games
def get_game():
    global Games
    randN = get_others_next_interarrival()
    if randN <= 50:
        g[0] += 1
        return Games[0]
    elif randN <= 80:
        g[1] += 1
        return Games[1]
    elif randN <= 85:
        g[2] += 1
        return Games[2]
    elif randN <= 95:
        g[3] += 1
        return Games[3]
    else:
        g[4] += 1
        return Games[4]


# This function returns the priority number
def get_priority(cust):
    if cust.ticket_type == "normal":
        return 0  # 0 for lower priority
    else:
        return -1  # -1 for higher priority


##################
# Types of tickets#
##################

normal = 10
special = 30


#################
# Customers Class#
#################

class customer:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.interarrival = get_Customers_next_interarrival()
        self.number_of_games = get_number_of_games()
        self.ticket_type = get_ticket_types()
        self.games = {}

        # print(str(self.name) + " " + str(self.interarrival) + " " +str(self.number_of_games)+" " + str(self.ticket_type) )
        for i in range(self.number_of_games):
            self.games[i] = get_game()
        # print(self.games[i].name )


# Request the Game by priority and yield until the finish time
def game_process(cust, i, env):
    with cust.games[i]["available"].request(priority=get_priority(cust)) as req:
        yield req

        yield env.timeout(cust.games[i]["time_to_finish"])


# Check the total profit at the end of each month
def monthly_check(env):
    global total_profit, Tax, Park_place_installment, Employees_monthly_salaries, Electricity_and_other_services, require_profit, flag, total_profit_count

    while True:

        yield env.timeout(30 * 24 * 60)

        total_profit[total_profit_count] -= (Tax * total_profit[
            total_profit_count]) + Park_place_installment + Employees_monthly_salaries + Electricity_and_other_services
        if sum(total_profit) >= require_profit:
            flag = True
            break
        total_profit_count += 1
        total_profit.append(0)


def start(env):
    global total_profit, months, normal, special, customer_count, flag, days, hours, total_profit_count
    total_profit.append(0)
    months = int(env.now / (30 * 24 * 60))
    env.process(monthly_check(env))

    for i in range(len(Games)):
        Games[i]["available"] = simpy.PriorityResource(env, capacity=Games[i]["capacity"])
    i = 0           # used as a customer name
    c = 1           # counter for days list   days=[1, 2, 3, 4, ..]
    a = 1           # we multiply this factor to 12 to check if the day is end or not .. is >=12  .. >=36 and so on ..
    cusPerDay = 0   # number of customers per day
    while True:

        if flag:
            break

        cust = customer(env, i)
        if cust.ticket_type == "normal":
            total_profit[total_profit_count] += normal
        else:
            total_profit[total_profit_count] += special

        i += 1
        customer_count += 1
        cusPerDay += 1

        yield env.timeout(cust.interarrival)
        hours = env.now / 60

        if hours > 12 * a:  # check if the day is end
            yield env.timeout(60 * 12)
            days.append(c)
            customer_arrival.append(cusPerDay)
            cusPerDay = 0
            # print("customer_count %s" %(customer_count))
            # print("day %s customer per day %s" % (days[c-1],customer_arrival[c-1]))
            c += 1
            a += 2

        for g in range(cust.number_of_games):
            total_profit[total_profit_count] += cust.games[g]["price"]
            env.process(game_process(cust, g, env))

    months = int(env.now / (30 * 24 * 60))
    print('Total profit: %s$ in %s months with total customer %s' % (sum(total_profit), months, customer_count))
    total_profit.clear()
    flag = False
    customer_count = 0
    total_profit_count = 0


# Called by the GUI to start the simulation
def startSim(nOfSim, req_profit):
    global number_of_simulation, require_profit
    number_of_simulation = nOfSim
    require_profit = req_profit
    for i in range(number_of_simulation):
        env = simpy.Environment()
        env.process(start(env))
        env.run()
        print("========================")
