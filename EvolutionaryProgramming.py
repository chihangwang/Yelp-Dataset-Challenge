import sys
import random
import math

class EvolutionaryProgramming:

    def __init__(self, seed, n, zone):

        random.seed(seed)

        self.n = n
        self.benchmark_size = 981
        self.zone = zone
        self.CROSS_VALIDATION_ZONE = 3
        self.zone_block = self.benchmark_size/self.CROSS_VALIDATION_ZONE
        self.model_coeffcient = []

        self.epsilon = 0.10
        self.q = 10
        self.alpha = 0.2
        self.tau = (1/math.sqrt(2*self.n))*2
        self.pools = [[]]*self.n
        self.offsprings = [[]]*self.n
        self.tournament_pool = []
        self.benchmark  = []
        self.training_set = []
        self.testing_set  = []

    def init(self):

        # populate the pool with n individuals
        for i in range(self.n):

            # 12 object variables, 12 strategy parameters
            chromosome = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0]
            for j in range(12):
                chromosome[j] = round(random.uniform(-5, 5), 8)
            for j in range(12, 24):
                chromosome[j] = 1

            self.pools[i] = chromosome

        # populate the benchmark
        benchmark_data = open('./parsed_data/benchmark.data', 'r')

        for line in benchmark_data:
            columns = line.strip().split(' ')
            data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(13):
                data[i] = float(columns[i+2])
            self.benchmark.append(data)

        benchmark_data.close()

        for i in range(self.CROSS_VALIDATION_ZONE):

            # populate the testing_set
            if i == self.zone:
                for j in range(i*self.zone_block, (i+1)*self.zone_block):
                    self.testing_set.append(self.benchmark[j])

            # populate the training_set
            else:
                for j in range(i*self.zone_block, (i+1)*self.zone_block):
                    self.training_set.append(self.benchmark[j])

    def deinit(self):
        self.pools = [[]]*self.n
        self.offsprings = [[]]*self.n
        self.tournament_pool = []
        self.benchmark  = []
        self.training_set = []
        self.testing_set  = []

    def mutate(self):
        # (Everyone breeds) Each individual creates one child by mutation!
        # => mutate the strategy parameters (sigma) first based on:
        # => sigma'(i) = sigma(i) * (1 + alpha * N(0, 1))
        cnt = 0
        for chromosome in self.pools:

            N = random.gauss(0, 1)
            child = list(chromosome)

            for i in range(12, 24):
                Ni = random.gauss(0, 1)
                sigma = child[i]*(1 + self.alpha * N)
                if sigma < self.epsilon:
                    sigma = self.epsilon
                child[i] = round(sigma, 8)

                # => then mutate the object variables based on:
                # => x'(i) = x(i) + sigma(i) * Ni(0, 1)
                x = child[i-12] + child[i]*Ni
                child[i-12] = round(x, 8)

            self.offsprings[cnt] = child
            cnt += 1

    def eval_root_error(self):

        # clear the tournament pool for next round!
        self.tournament_pool = []

        # evaluate every individuals in parent and offspring pool
        for parent in self.pools:

            squared_err_sum = 0
            cnt = 0

            for data in self.training_set:

                computed_star = 0
                ground_truth_star = data[0]

                # calculate the computed star
                for i in range(1, 13):
                    computed_star += parent[i-1] * data[i]

                # calculate the squarred error
                squared_err_sum += math.pow(computed_star - ground_truth_star, 2)
                cnt += 1

            squared_err_sum /= cnt

            # populate the tournament_pool with each individual with its Sqr_error
            self.tournament_pool.append([squared_err_sum, parent])

        # clear parent pool for next round
        self.pools = [[]]*self.n

        for child in self.offsprings:

            squared_err_sum = 0
            cnt = 0

            for data in self.training_set:

                computed_star = 0
                ground_truth_star = data[0]

                # calculate the computed star
                for i in range(1, 13):
                    computed_star += child[i-1] * data[i]

                # calculate the squarred error
                squared_err_sum += math.pow(computed_star - ground_truth_star, 2)
                cnt += 1

            squared_err_sum /= cnt

            # populate the tournament_pool with each individual with its Sqr_error
            self.tournament_pool.append([squared_err_sum, child])

        # clear child pool for next round
        self.offsprings = [[]]*self.n

    def select_by_tournament(self):
        tournament_result_pool = []

        # tournament begins
        for individual in self.tournament_pool:
            squared_err_sum = individual[0]
            body = individual[1]
            win = 0

            for i in range(self.q):
                opponent = random.choice(self.tournament_pool)
                if(squared_err_sum < opponent[0]):
                    win += 1

            tournament_result_pool.append([win, body])

        # sort the result_pool with how many wins
        def predicate(individual):
            return individual[0]

        rank = sorted(tournament_result_pool, key=predicate)
        rank.reverse()

        # select 40 individuals with most WINs as next generation
        for i in range(self.n):
            self.pools[i] = rank[i][1]

    def print_model_coefficient(self):
        def predicate(individual):
            return individual[0]

        rank = sorted(self.tournament_pool, key=predicate)
        self.model_coeffcient = rank[0][1]
        print "\n[MODEL]"
        print self.model_coeffcient

    def eval_testing_set(self):
        coefficients = list(self.model_coeffcient)
        print '=============== evaluate testing data ==================\n'

        for sample_data in [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 327]:
            squared_err_sum = 0
            cnt = 0
            for data in self.testing_set:

                ground_truth_star = data[0]
                computed_star = 0

                # calculate the computed star
                for i in range(1, 13):
                    computed_star += coefficients[i-1] * data[i]

                # calculate the squarred error
                squared_err_sum += math.pow(computed_star - ground_truth_star, 2)
                cnt += 1
                if cnt == sample_data:
                    break

            # print the mean squarred error of the generated model
            mean_squared_err = squared_err_sum / cnt
            print 'sample-data[' + str(sample_data) + '] mean_squared_err: ' + str(mean_squared_err)

    def print_best(self, ith_generation):
        def predicate(individual):
            return individual[0]
        rank = sorted(self.tournament_pool, key=predicate)

        # print the squarred error
        print str(ith_generation) + 'th MIN(ERR): ' + str(rank[0][0])

    def print_avg(self, ith_generation):
        sum = 0
        err_sum = 0
        for individual in self.tournament_pool:
            err_sum += individual[0]
            sum += 1
        print str(ith_generation) + 'th AVG(ERR): ' + str(err_sum/sum)

    def debug(self):
        print "\nPOOLS =====================================\n"
        for i in range(self.n):
            print self.pools[i]
        print "\nCHILD =====================================\n"
        for i in range(self.n):
            print self.offsprings[i]
        print "\nTRAIN =====================================\n"
        for i in range(self.zone_block*2):
            print self.training_set[i]
        print "\nTEST ======================================\n"
        for i in range(self.zone_block):
            print self.testing_set[i]
        print "\nTOURNAMENT =====================================\n"
        for individual in self.tournament_pool:
            print individual
        print "\nEND =======================================\n"

    def print_testing_data(self):
        print '[TESTING DATA]:'
        for data in self.testing_set:
            print '\t'.join(map(str, data))

    def print_training_data(self):
        print '[TRAINING DATA]:'
        for data in self.training_set:
            print '\t'.join(map(str, data))

def main():
    n = 40
    seed = 1234
    termination_generation_cnt = 300
    cross_validation_zones = 3
    DEBUG = False

    for i in range(cross_validation_zones):
        ep = EvolutionaryProgramming(seed, n, 1)
        ep.init()
        if DEBUG == True:
            ep.print_training_data()
            ep.print_testing_data()
        for j in range(termination_generation_cnt):
            ep.mutate()
            ep.eval_root_error()
            ep.select_by_tournament()
            if DEBUG == True:
                ep.print_best(j)
                ep.print_avg(j)
                ep.debug()
        ep.print_model_coefficient()
        ep.eval_testing_set()
        ep.deinit()

if __name__ == '__main__':
    main()
